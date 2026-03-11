"""
Improved Training Script for Image Caption Generator
Trains on full dataset with better parameters and architecture.
"""

import os
import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding, Dropout, add, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import matplotlib.pyplot as plt
import gc


class ImprovedDataLoader:
    """Improved data loader with better preprocessing"""
    
    def __init__(self, captions_file, images_dir):
        self.captions_file = captions_file
        self.images_dir = images_dir
        self.data = None
        self.image_features = {}
        self.tokenizer = None
        self.max_caption_length = 40
        
    def load_captions(self):
        """Load captions from CSV"""
        print("Loading captions...")
        self.data = pd.read_csv(self.captions_file)
        print(f"Loaded {len(self.data)} captions for {self.data['image'].nunique()} unique images")
        return self.data
    
    def preprocess_captions(self, vocab_size=8000):
        """Clean and tokenize captions with better preprocessing"""
        print("Preprocessing captions...")
        
        # Better cleaning - keep punctuation for better captions
        import re
        def clean(text):
            text = text.lower().strip()
            # Keep alphanumeric and basic punctuation
            text = re.sub(r'[^a-z0-9\s\.\!\?\,]', '', text)
            # Add start/end tokens
            text = 'startseq ' + text + ' endseq'
            return ' '.join(text.split())
        
        self.data['caption'] = self.data['caption'].apply(clean)
        
        # Get caption lengths
        self.data['length'] = self.data['caption'].apply(lambda x: len(x.split()))
        
        # Filter very short or very long captions
        self.data = self.data[(self.data['length'] >= 3) & (self.data['length'] <= 35)]
        
        # Update max length
        self.max_caption_length = min(self.data['length'].max() + 1, 40)
        
        # Tokenize with larger vocabulary
        self.tokenizer = Tokenizer(num_words=vocab_size, oov_token='<unk>', 
                                   filters='!"#$%&()*+,-/:;<=>?@[\\]^_`{|}~\t\n')
        self.tokenizer.fit_on_texts(self.data['caption'].values)
        
        # Add special tokens
        word_counts = self.tokenizer.word_counts
        print(f"Vocabulary size: {len(self.tokenizer.word_index) + 1}")
        
        # Find actual max length
        self.max_caption_length = max(len(seq.split()) for seq in self.data['caption'].values)
        print(f"Max caption length: {self.max_caption_length}")
        
        return self.tokenizer
    
    def extract_features(self, model, batch_size=32):
        """Extract image features with batching for efficiency"""
        print("Extracting image features...")
        
        unique_imgs = self.data['image'].unique()
        n = len(unique_imgs)
        
        for i in range(0, n, batch_size):
            batch_imgs = unique_imgs[i:i+batch_size]
            
            for img_name in batch_imgs:
                path = os.path.join(self.images_dir, img_name)
                try:
                    img = keras_image.load_img(path, target_size=(299, 299))
                    img = keras_image.img_to_array(img)
                    img = np.expand_dims(img, axis=0)
                    img = preprocess_input(img)
                    
                    feat = model.predict(img, verbose=0)
                    self.image_features[img_name] = feat.reshape(-1)
                except Exception as e:
                    print(f"Error processing {img_name}: {e}")
                    continue
            
            if (i + batch_size) % 500 == 0 or i + batch_size >= n:
                print(f"  Processed {min(i + batch_size, n)}/{n} images")
        
        print(f"Extracted {len(self.image_features)} image features")
        return self.image_features


def create_sequences(tokenizer, max_length, image_features, data):
    """Create input-output sequences with proper padding"""
    X_img, X_cap, y = [], [], []
    
    for idx, row in data.iterrows():
        img_name = row['image']
        caption = row['caption']
        
        if img_name not in image_features:
            continue
            
        seq = tokenizer.texts_to_sequences([caption])[0]
        
        for i in range(1, len(seq)):
            in_seq = seq[:i]
            out_word = seq[i]
            
            in_seq = pad_sequences([in_seq], maxlen=max_length, padding='post')[0]
            
            X_img.append(image_features[img_name])
            X_cap.append(in_seq)
            y.append(out_word)
    
    return np.array(X_img), np.array(X_cap), np.array(y)


def build_improved_model(vocab_size, max_length, emb_dim=256, lstm_dim=512):
    """Build improved model with Bidirectional LSTM"""
    print("Building improved model...")
    
    # Image branch - stronger
    img_input = Input(shape=(2048,), name='img')
    img = Dense(512, activation='relu')(img_input)
    img = Dropout(0.4)(img)
    img = Dense(256, activation='relu')(img)
    img = Dropout(0.3)(img)
    
    # Caption branch - Bidirectional LSTM for better context
    cap_input = Input(shape=(max_length,), name='cap')
    cap = Embedding(vocab_size, emb_dim, mask_zero=True)(cap_input)
    cap = Bidirectional(LSTM(lstm_dim, return_sequences=True))(cap)
    cap = Dropout(0.3)(cap)
    cap = LSTM(lstm_dim // 2, return_sequences=False)(cap)
    cap = Dropout(0.3)(cap)
    
    # Merge with attention-like mechanism
    merged = add([img, cap])
    merged = Dense(512, activation='relu')(merged)
    merged = Dropout(0.3)(merged)
    merged = Dense(256, activation='relu')(merged)
    
    # Output
    out = Dense(vocab_size, activation='softmax')(merged)
    
    model = Model(inputs=[img_input, cap_input], outputs=out)
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=Adam(learning_rate=0.0005),
        metrics=['accuracy']
    )
    
    print(model.summary())
    return model


def train_model(data_path, images_path, epochs=20, batch_size=64):
    """Main training function"""
    print("="*70)
    print("IMPROVED IMAGE CAPTION GENERATOR - TRAINING")
    print("="*70)
    
    # Load data
    print("\n[1/6] Loading data...")
    loader = ImprovedDataLoader(data_path, images_path)
    loader.load_captions()
    tokenizer = loader.preprocess_captions(vocab_size=8000)
    
    # Load InceptionV3 for feature extraction
    print("\n[2/6] Loading InceptionV3...")
    inception = InceptionV3(weights='imagenet')
    feature_extractor = Model(inputs=inception.input, outputs=inception.layers[-2].output)
    
    # Extract features from ALL images
    print("\n[3/6] Extracting image features...")
    loader.extract_features(feature_extractor, batch_size=32)
    del inception
    gc.collect()
    
    # Create sequences
    print("\n[4/6] Creating training sequences...")
    vocab_size = min(len(tokenizer.word_index) + 1, 8000)
    max_length = loader.max_caption_length
    
    # Use full dataset
    X_img, X_cap, y = create_sequences(tokenizer, max_length, 
                                       loader.image_features, loader.data)
    
    print(f"Total training samples: {len(X_img)}")
    
    # Split data
    split = int(len(X_img) * 0.95)
    X_img_train, X_img_val = X_img[:split], X_img[split:]
    X_cap_train, X_cap_val = X_cap[:split], X_cap[split:]
    y_train, y_val = y[:split], y[split:]
    
    print(f"Training: {len(X_img_train)}, Validation: {len(X_img_val)}")
    
    # Build model
    print("\n[5/6] Building and training model...")
    model = build_improved_model(vocab_size, max_length)
    
    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6),
    ]
    
    # Train
    history = model.fit(
        [X_img_train, X_cap_train],
        y_train,
        validation_data=([X_img_val, X_cap_val], y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save
    print("\n[6/6] Saving model...")
    model.save('caption_model_improved.h5')
    
    with open('tokenizer_improved.pkl', 'wb') as f:
        pickle.dump({
            'tokenizer': tokenizer,
            'max_length': max_length
        }, f)
    
    print("✓ Model saved: caption_model_improved.h5")
    print("✓ Tokenizer saved: tokenizer_improved.pkl")
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Training & Validation Loss')
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Acc')
    plt.plot(history.history['val_accuracy'], label='Val Acc')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Training & Validation Accuracy')
    
    plt.tight_layout()
    plt.savefig('training_history_improved.png')
    plt.close()
    
    print("✓ Training history saved: training_history_improved.png")
    print("\n" + "="*70)
    print("Training complete!")
    print("="*70)
    
    return model, tokenizer


if __name__ == "__main__":
    data_path = 'dataset/captions.txt'
    images_path = 'dataset/Images'
    
    if not os.path.exists(data_path) or not os.path.exists(images_path):
        print("Error: dataset/captions.txt and dataset/Images required")
    else:
        train_model(data_path, images_path, epochs=20, batch_size=64)


"""
Advanced Caption Generator using Pre-trained Vision-Language Models
Uses BLIP (Bootstrapped Language-Image Pre-training) for high-quality captions.
"""

import os
import numpy as np
import pickle
from PIL import Image
import matplotlib.pyplot as plt
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch


class AdvancedCaptionGenerator:
    """Generate high-quality captions using BLIP model"""
    
    def __init__(self, model_type="base"):
        """
        Initialize BLIP model for caption generation
        
        Args:
            model_type: "base" or "large" - larger model gives better results but needs more memory
        """
        print(f"Loading BLIP-{model_type} model...")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load processor and model
        if model_type == "large":
            model_name = "Salesforce/blip-large-coco"
        else:
            model_name = "Salesforce/blip-base-coco"
        
        try:
            self.processor = BlipProcessor.from_pretrained(model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(model_name)
            self.model.to(self.device)
            print("✓ BLIP model loaded successfully!")
        except Exception as e:
            print(f"Error loading BLIP: {e}")
            print("Trying alternative model...")
            # Fallback to BLIP image captioning model
            model_name = "Salesforce/blip-image-captioning-base"
            self.processor = BlipProcessor.from_pretrained(model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(model_name)
            self.model.to(self.device)
            print("✓ BLIP captioning model loaded!")
        
        self.model_type = model_type
    
    def generate_caption(self, image_path, max_length=50, num_beams=5, 
                         do_sample=False, prompt=None):
        """
        Generate caption for an image
        
        Args:
            image_path: Path to the image file
            max_length: Maximum length of generated caption
            num_beams: Number of beams for beam search (higher = better quality)
            do_sample: Whether to use sampling (True = more creative, False = more accurate)
            prompt: Optional prompt to condition the generation
            
        Returns:
            Generated caption string
        """
        try:
            # Load and process image
            raw_image = Image.open(image_path).convert('RGB')
            
            # Prepare inputs
            if prompt:
                # Conditional captioning with prompt
                inputs = self.processor(raw_image, prompt, return_tensors="pt").to(self.device)
            else:
                # Unconditional captioning
                inputs = self.processor(raw_image, return_tensors="pt").to(self.device)
            
            # Generate
            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=num_beams,
                    do_sample=do_sample,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.2
                )
            
            # Decode
            caption = self.processor.decode(output[0], skip_special_tokens=True)
            
            return caption.strip()
            
        except Exception as e:
            print(f"Error generating caption: {e}")
            return "Could not generate caption"
    
    def generate_multiple(self, image_path, num_captions=3):
        """
        Generate multiple diverse captions for an image
        
        Args:
            image_path: Path to the image file
            num_captions: Number of captions to generate
            
        Returns:
            List of generated captions
        """
        captions = []
        
        # Different prompts for diversity
        prompts = [
            None,
            "a photo of",
            "an image showing",
            "this is"
        ]
        
        try:
            raw_image = Image.open(image_path).convert('RGB')
            
            for i in range(min(num_captions, len(prompts))):
                prompt = prompts[i]
                
                if prompt:
                    inputs = self.processor(raw_image, prompt, return_tensors="pt").to(self.device)
                else:
                    inputs = self.processor(raw_image, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    output = self.model.generate(
                        **inputs,
                        max_length=50,
                        num_beams=5,
                        do_sample=True,
                        top_p=0.9,
                        temperature=0.8,
                        repetition_penalty=1.1
                    )
                
                caption = self.processor.decode(output[0], skip_special_tokens=True)
                captions.append(caption.strip())
            
            return captions
            
        except Exception as e:
            print(f"Error generating multiple captions: {e}")
            return ["Could not generate captions"]
    
    def describe_detailed(self, image_path):
        """
        Generate a detailed description of the image
        
        Returns:
            Detailed caption with scene description
        """
        # Start with generic prompt for detailed description
        prompt = "a detailed photo of"
        
        caption = self.generate_caption(
            image_path, 
            max_length=75, 
            num_beams=7,
            prompt=prompt
        )
        
        return caption
    
    def show_caption(self, image_path):
        """Display image with generated caption"""
        caption = self.generate_caption(image_path)
        img = Image.open(image_path)
        
        plt.figure(figsize=(12, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"Caption: {caption}", fontsize=14, pad=20)
        plt.tight_layout()
        plt.show()
        
        return caption


def main():
    """Interactive demo"""
    print("="*60)
    print("ADVANCED IMAGE CAPTION GENERATOR (BLIP)")
    print("="*60)
    
    # Initialize
    try:
        generator = AdvancedCaptionGenerator(model_type="base")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return
    
    print("\n📸 Advanced Caption Generator Ready!")
    print("Enter image path to generate caption (or 'quit' to exit)\n")
    
    while True:
        path = input("Image path: ").strip()
        
        if path.lower() == 'quit':
            break
        
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
        
        print("\nGenerating caption...")
        
        # Single caption
        caption = generator.generate_caption(path, num_beams=5)
        print(f"\n📝 Caption: {caption}\n")
        
        # Show options
        show = input("Show image with caption? (y/n): ").lower()
        if show == 'y':
            generator.show_caption(path)
        
        # Multiple captions option
        multi = input("Generate multiple captions? (y/n): ").lower()
        if multi == 'y':
            captions = generator.generate_multiple(path, num_captions=3)
            print("\n📋 Multiple Captions:")
            for i, cap in enumerate(captions, 1):
                print(f"  {i}. {cap}")


if __name__ == "__main__":
    main()


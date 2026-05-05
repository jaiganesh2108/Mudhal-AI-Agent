import os
from augmentations import ( flip_left_right, to_grayscale, adjust_brightness, rotate_90, central_crop )
from pipeline import augment_image

from utils import load_image, save_image,visualize

def main():
    # Load the image
    image_path = "input_image.jpg"  # Replace with your image path
    image = load_image(image_path)

    # Define the augmentations to apply
    augmentations = [
        flip_left_right,
        to_grayscale,
        lambda img: adjust_brightness(img, factor=1.5),  # Example brightness adjustment
        rotate_90,
        lambda img: central_crop(img, crop_size=(200, 200))  # Example central crop
    ]

    # Apply the augmentations
    augmented_images = augment_image(image, augmentations)

    # Save and visualize the augmented images
    for idx, aug_img in enumerate(augmented_images):
        save_path = f"augmented_image_{idx}.jpg"
        save_image(aug_img, save_path)
        print(f"Saved augmented image: {save_path}")
        visualize(aug_img)
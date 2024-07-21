from PIL import Image, ImageDraw, ImageFont, ImageFilter


def create_image_with_text(image_path, text, output_path, height):
    # Load the image and get its original dimensions
    original_image = Image.open(image_path).convert("RGBA")
    original_width, original_height = original_image.size

    # Calculate aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate new width based on the provided height
    width = int(height * aspect_ratio)

    # Resize the image to maintain the aspect ratio
    image = original_image.resize((width, height), Image.Resampling.LANCZOS)

    # Create a new image with transparent background
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)  # Use an elegant font
    except IOError:
        font = ImageFont.load_default()  # Fallback if the font is not available

    dummy_image = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    border_margin = 20
    border_width = 1
    padding_right = 10
    new_image_width = 300
    new_image_height = max(height,
                           text_height + 2 * border_margin)  # Ensure the height accommodates both the image and text

    # Create a larger image for better antialiasing
    scale_factor = 4
    large_image_width = new_image_width * scale_factor
    large_image_height = new_image_height * scale_factor
    large_image = Image.new("RGBA", (large_image_width, large_image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(large_image)

    # Draw rounded border around the entire area
    border_radius = 20 * scale_factor
    overall_border_box = [0, 0, large_image_width, large_image_height]
    draw.rounded_rectangle(overall_border_box, radius=border_radius, outline="red", width=border_width * scale_factor)

    # Resize the image back down to the original size
    new_image = large_image.resize((new_image_width, new_image_height), Image.Resampling.LANCZOS)

    # Paste the resized image onto the new image with adjusted padding
    image_position = (1, (new_image_height - height) // 2)  # Align image vertically
    new_image.paste(image, image_position, image)

    # Create an image for the glowing effect
    glow_image = Image.new("RGBA", new_image.size, (255, 255, 255, 0))
    glow_draw = ImageDraw.Draw(glow_image)

    # Draw a larger rounded rectangle for the glow effect
    glow_radius = border_radius + 10  # Extend the radius for the glow
    glow_box = [0, 0, new_image_width, new_image_height]
    glow_draw.rounded_rectangle(glow_box, radius=glow_radius, outline=(255, 0, 0, 100), width=border_width + 10)

    # Apply a Gaussian Blur to the glow effect
    glow_image = glow_image.filter(ImageFilter.GaussianBlur(10))

    # Composite the glow effect with the main image
    new_image = Image.alpha_composite(new_image, glow_image)

    # Add luminance effect (glow) around the text
    text_glow_image = Image.new("RGBA", new_image.size, (255, 255, 255, 0))
    text_glow_draw = ImageDraw.Draw(text_glow_image)
    text_position = (width + 5, (new_image_height - text_height) // 2)  # Position text with padding
    text_glow_draw.text(text_position, text, font=font, fill=(255, 255, 255, 128))
    text_glow_image = text_glow_image.filter(ImageFilter.GaussianBlur(5))
    new_image = Image.alpha_composite(new_image, text_glow_image)

    # Add text to the image
    draw = ImageDraw.Draw(new_image)
    draw.text(text_position, text, font=font, fill=(255, 255, 255, 255))  # White text

    # Crop the image to fit within the border
    border_crop_box = (border_width, border_width, new_image_width - border_width, new_image_height - border_width)
    cropped_image = new_image.crop(border_crop_box)

    # Save the new image
    cropped_image.save(output_path, "PNG")


# Example usage
# image_path = "your_image.png"  # Replace with your image path
# text = "Your custom text goes here"
# output_path = "output_image.png"
# create_image_with_text(image_path, text, output_path)
image_path = "wimbledon-logo-removebg-preview.png"  # Replace with your image path
text = "Alcaraz beat Djokovic in straight\nsets to retain Wimbledon Title”"
output_path = "output_image.png"
create_image_with_text(image_path, text, output_path, 70)

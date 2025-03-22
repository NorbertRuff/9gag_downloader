"""
Generate a simple icon for the 9GAG Downloader application.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a transparent background
icon_size = 256
image = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Define colors
bg_color = (30, 30, 30, 255)  # Dark background
accent_color = (0, 200, 150, 255)  # Teal accent
text_color = (255, 255, 255, 255)  # White text

# Draw a rounded rectangle for background
draw.rounded_rectangle([(20, 20), (icon_size - 20, icon_size - 20)], 30, fill=bg_color)

# Draw download arrow
arrow_width = 80
arrow_height = 120
arrow_x = (icon_size - arrow_width) // 2
arrow_y = 65

# Arrow stem
draw.rectangle(
    [
        (arrow_x + arrow_width // 3, arrow_y),
        (arrow_x + 2 * arrow_width // 3, arrow_y + 2 * arrow_height // 3),
    ],
    fill=accent_color,
)

# Arrow head
draw.polygon(
    [
        (arrow_x, arrow_y + 2 * arrow_height // 3),  # Left point
        (arrow_x + arrow_width, arrow_y + 2 * arrow_height // 3),  # Right point
        (arrow_x + arrow_width // 2, arrow_y + arrow_height),  # Bottom point
    ],
    fill=accent_color,
)

# Add text "9GAG"
try:
    # Try to load a font if available
    font = ImageFont.truetype("arial.ttf", 36)
except IOError:
    # Fall back to default font
    font = ImageFont.load_default()

text = "9GAG"
text_width = draw.textlength(text, font=font)
text_x = (icon_size - text_width) // 2
text_y = arrow_y + arrow_height + 10
draw.text((text_x, text_y), text, font=font, fill=text_color)

# Save as PNG and ICO
image.save("icon.png")
image.save("icon.ico")

print(f"Icon created successfully at {os.path.abspath('icon.ico')}")

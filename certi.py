import csv
import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def generate_certificate(name, registration_number, template, font_file, font_size, vertical_position, output_folder):
    try:
        base = Image.open(template).convert("RGB")
        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype(font_file, font_size)
        bbox = font.getbbox(name)
        text_width = bbox[2] - bbox[0]
        image_width, _ = base.size
        center_x = (image_width - text_width) // 2
        draw.text((center_x, vertical_position), name, font=font, fill="black")
        output_filename = os.path.join(output_folder, f"{registration_number}.png")
        base.save(output_filename)
        print(f"Certificate for {name} saved as {output_filename}")
    except Exception as e:
        print(f"Error generating certificate for {name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate certificates from a PNG template and CSV data")
    parser.add_argument("--template", default="assets/wolf.png", help="Path to the certificate PNG template")
    parser.add_argument("--csv", default="data.csv", help="CSV file with 'Name' and 'Registration' fields")
    parser.add_argument("--font", default="assets/font.ttf", help="Path to the TTF font file")
    parser.add_argument("--size", type=int, default=72, help="Font size")
    parser.add_argument("--vertical", type=int, default=550, help="Vertical position for the text")
    parser.add_argument("--output", default="certificates2", help="Folder to store generated certificates")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    try:
        with open(args.csv, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get("Name")
                registration_number = row.get("Registration")
                if name and registration_number:
                    generate_certificate(name, registration_number, args.template, args.font, args.size, args.vertical, args.output)
                else:
                    print("Skipping row with missing name or registration number.")
    except FileNotFoundError:
        print(f"CSV file '{args.csv}' not found.")

if __name__ == "__main__":
    main()
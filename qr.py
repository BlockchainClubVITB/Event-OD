import qrcode
from PIL import Image
import pandas as pd
import os

def generate_qr_code(registration_number, first_name, last_name, logo_path, template_path, output_path, 
                     qr_size=1000, qr_x_offset=500, qr_y_offset=300):
    try:
        qr_data = f"{registration_number} {first_name} {last_name}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=25,  # Reduced box size for smaller QR
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
        # Make QR size configurable
        qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

        datas = qr_img.getdata()
        new_data = []
        for item in datas:
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        qr_img.putdata(new_data)

        qr_width, qr_height = qr_img.size
        print(f"QR Code dimensions: {qr_width}x{qr_height}")

        max_logo_width = qr_width * 0.3
        max_logo_height = qr_height * 0.3
        print(f"Recommended logo dimensions: {max_logo_width}x{max_logo_height}")

        # Check if logo file exists
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo file not found: {logo_path}")
        
        logo = Image.open(logo_path)

        logo_width, logo_height = logo.size
        print(f"Logo dimensions: {logo_width}x{logo_height}")
        
        # Just a warning if logo is large, but no automatic resizing
        if logo_width > max_logo_width or logo_height > max_logo_height:
            print(f"Note: Logo size ({logo_width}x{logo_height}) is larger than recommended ({max_logo_width:.0f}x{max_logo_height:.0f})")

        pos = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

        qr_img.paste(logo, pos, mask=logo)

        # Check if template file exists
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        # Use the template path parameter instead of hardcoded path
        pass_img = Image.open(template_path)

        pass_width, pass_height = pass_img.size
        print(f"Template dimensions: {pass_width}x{pass_height}")
        
        # Configurable positioning
        qr_x = pass_width - qr_width - qr_x_offset
        qr_y = (pass_height - qr_height) // 2 + qr_y_offset
        
        print(f"QR position: ({qr_x}, {qr_y})")

        pass_img.paste(qr_img, (qr_x, qr_y), qr_img)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pass_img.save(output_path)
        
    except Exception as e:
        print(f"Error generating QR code for {registration_number}: {str(e)}")
        raise

def process_csv(csv_file, logo_path, template_path, output_dir='output/tickets'):
    df = pd.read_csv(csv_file)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for index, row in df.iterrows():
        registration_number = row['Registration'].replace(" ", "").upper()
        
        # Split the name into first and last name
        full_name = row['Name'].strip()
        name_parts = full_name.split()
        
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:])  # Handle multiple last names
        else:
            first_name = full_name
            last_name = ""

        output_file = f"{output_dir}/{registration_number}.png"

        # You can customize these values for positioning:
        # qr_size: Size of QR code (default: 300)
        # qr_x_offset: Distance from right edge (default: 50) 
        # qr_y_offset: Vertical offset from center (default: 180)
        generate_qr_code(registration_number, first_name, last_name, logo_path, template_path, output_file,
                        qr_size=375, qr_x_offset=60, qr_y_offset=30)
        print(f"Generated: {output_file}")

csv_file = 'assets/data.csv'
logo_path = 'assets/logo.png'
template_path = 'assets/decrypt2win.png'

process_csv(csv_file, logo_path, template_path)
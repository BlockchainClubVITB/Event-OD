import qrcode
from PIL import Image
import pandas as pd
import os

def generate_qr_code(registration_number, name, logo_path, output_path):
    qr_data = f"{registration_number} {name}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=30,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((410, 410), Image.LANCZOS)

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

    logo = Image.open(logo_path)

    logo_width, logo_height = logo.size
    if logo_width > max_logo_width or logo_height > max_logo_height:
        raise ValueError("Logo size is too large to fit in the QR code")

    pos = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    qr_img.paste(logo, pos, mask=logo)

    pass_img = Image.open('assets/Pass.png')

    pass_width, pass_height = pass_img.size
    qr_x = pass_width - qr_width - 50
    qr_y = (pass_height - qr_height) // 2 + 180

    pass_img.paste(qr_img, (qr_x, qr_y), qr_img)

    pass_img.save(output_path)

def process_csv(csv_file, logo_path):
    df = pd.read_csv(csv_file)

    if not os.path.exists('tickets'):
        os.makedirs('tickets')

    for index, row in df.iterrows():
        registration_number = row['Registration'].replace(" ", "").upper()
        name = row['Name']

        output_file = f"tickets/{registration_number}.png"

        generate_qr_code(registration_number, name, logo_path, output_file)
        print(f"Generated: {output_file}")

csv_file = 'assets/data3.csv'
logo_path = 'assets/logo.png'

process_csv(csv_file, logo_path)
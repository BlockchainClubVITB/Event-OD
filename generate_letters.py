# -*- coding: utf-8 -*-
import os
import fitz 
import pandas as pd

def generate_pdf_certificates(csv_file, template_pdf, output_dir):
    """
    Generates personalized PDF certificates from a CSV file.
    
    Args:
        csv_file (str): Path to the input CSV file.
        template_pdf (str): Path to the blank PDF template.
        output_dir (str): Directory to save the generated PDFs.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # The content of the letter with placeholders
    # Using regular hyphens instead of em-dashes to avoid encoding issues
    letter_content = """Dear {name},

Welcome to the Blockchain Club at VIT Bhopal University! Just like a chain relies on its blocks, each member brings a unique spark to build a strong and lively network. You are now a key part of this journey as a {team} Team Core Member for the term 2025-2026. We are excited to have you with us.

Your enthusiasm, commitment, and passion really shone during the selection process. We believe you are ready to make a difference. Here, ideas turn into actions, challenges become opportunities, and every project is a step toward innovation. You will take part in practical initiatives, work with others, and help shape experiences that will improve your skills and the club's vision.

The Blockchain Club works like a living ecosystem. It is a place where teamwork sparks creativity, experimentation leads to discovery, and every contribution strengthens the chain that connects us. Your enthusiasm, perspective, and proactive approach will help move the club forward. Take every chance, share your ideas confidently, and lead when inspiration strikes.

Let’s start this journey together. We will create experiences and build a legacy that is meaningful, inspiring, and unforgettable. Your adventure with the Blockchain Club begins now, and we look forward to the amazing blocks you will add to our shared chain.

Warm regards,

Blockchain Club
VIT Bhopal University"""

    # Read the CSV file using pandas with UTF-8 encoding
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"CSV loaded successfully. Found {len(df)} records.")
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    # Check if required columns exist
    required_columns = ['Name', 'team']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: CSV must contain the columns: {required_columns}")
        print(f"Available columns: {list(df.columns)}")
        return

    # Process each row (core member)
    for index, row in df.iterrows():
        name = str(row['Name']).strip()
        team_name = str(row['team']).strip()
        
        print(f"Processing: {name} from {team_name}")
        
        # Format the letter content with the current row's data
        formatted_letter = letter_content.format(name=name, team=team_name)
        
        # Clean up any problematic characters
        formatted_letter = clean_text_for_pdf(formatted_letter)

        try:
            # Open the PDF template
            doc = fitz.open(template_pdf)
            page = doc[0]  # Get the first page

            # Get page dimensions
            page_width = page.rect.width
            page_height = page.rect.height
            print(f"Page dimensions: {page_width} x {page_height}")

            # Try multiple positioning strategies with better font handling
            positions_to_try = [
                # Strategy 1: Center area with black text using Times-Romanetica
                {
                    'rect': fitz.Rect(page_width * 0.1, page_height * 0.3, page_width * 0.9, page_height * 0.8),
                    'color': (1, 1, 1),  # Black
                    'fontsize': 12,
                    'fontname': "Times-Roman",  # Times-Romanetica - better Unicode support
                    'description': 'Printed'
                },
                # Strategy 2: Using Times-Roman with smaller area
                {
                    'rect': fitz.Rect(page_width * 0.15, page_height * 0.25, page_width * 0.85, page_height * 0.75),
                    'color': (0, 0, 0),  # Black
                    'fontsize': 11,
                    'fontname': "tiro",  # Times-Roman alternative
                    'description': 'Center area with Times font'
                },
                # Strategy 3: Fallback with basic font
                {
                    'rect': fitz.Rect(50, 100, page_width - 50, page_height - 100),
                    'color': (0, 0, 0),  # Black
                    'fontsize': 10,
                    'fontname': "Times-Roman",  # Times-Romanetica
                    'description': 'Full area with Times-Romanetica'
                }
            ]

            text_added = False
            for strategy in positions_to_try:
                try:
                    # Clear any previous content (create a fresh copy)
                    doc.close()
                    doc = fitz.open(template_pdf)
                    page = doc[0]
                    
                    print(f"Trying strategy: {strategy['description']}")
                    
                    # Insert text with current strategy
                    result = page.insert_textbox(
                        strategy['rect'],
                        formatted_letter,
                        fontsize=strategy['fontsize'],
                        fontname=strategy['fontname'],
                        align=fitz.TEXT_ALIGN_JUSTIFY,
                        color=strategy['color']
                    )
                    
                    # Check if text was inserted successfully
                    if result > 0:  # Positive value means some text was inserted
                        print(f"Success with {strategy['description']} - Text length: {result}")
                        text_added = True
                        break
                    else:
                        print(f"Failed with {strategy['description']} - Result: {result}")
                        
                except Exception as e:
                    print(f"Error with strategy '{strategy['description']}': {e}")
                    continue

            if not text_added:
                print(f"Warning: Could not add text for {name}. Creating PDF anyway.")

            # Define the output file name - sanitize filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_pdf_path = os.path.join(output_dir, f"Certificate_{safe_name.replace(' ', '_')}.pdf")

            # Save the new PDF
            doc.save(output_pdf_path)
            doc.close()
            print(f"Successfully generated PDF for {name} -> {output_pdf_path}")
            
        except FileNotFoundError as e:
            print(f"Error: Template PDF not found: {template_pdf}")
            print(e)
            return
        except Exception as e:
            print(f"An error occurred while processing PDF for {name}: {e}")
            continue  # Continue with next person instead of returning

    print("PDF generation completed!")

def clean_text_for_pdf(text):
    """
    Clean text to ensure proper encoding for PDF generation.
    Replace problematic Unicode characters with safer alternatives.
    """
    # Dictionary of character replacements
    char_replacements = {
        '\u2013': '-',  # en dash
        '\u2014': '-',  # em dash
        '\u2015': '-',  # horizontal bar
        '\u2010': '-',  # hyphen
        '\u2011': '-',  # non-breaking hyphen
        '\u2012': '-',  # figure dash
        '\u2018': "'",  # left single quotation mark
        '\u2019': "'",  # right single quotation mark
        '\u201C': '"',  # left double quotation mark
        '\u201D': '"',  # right double quotation mark
        '\u2026': '...',  # horizontal ellipsis
        '\u00A0': ' ',   # non-breaking space
    }
    
    # Apply replacements
    for unicode_char, replacement in char_replacements.items():
        text = text.replace(unicode_char, replacement)
    
    # Ensure the text is properly encoded as UTF-8
    try:
        # Encode to UTF-8 and then decode to ensure clean text
        text = text.encode('utf-8', errors='replace').decode('utf-8')
    except Exception as e:
        print(f"Warning: Text encoding issue: {e}")
    
    return text

# --- Enhanced debugging function ---
def debug_pdf_template(template_pdf):
    """
    Debug function to analyze the PDF template
    """
    try:
        doc = fitz.open(template_pdf)
        page = doc[0]
        
        print(f"PDF Template Analysis:")
        print(f"- Page count: {doc.page_count}")
        print(f"- Page size: {page.rect.width} x {page.rect.height}")
        print(f"- Page rotation: {page.rotation}")
        
        # Check if there are any existing text blocks
        text_dict = page.get_text("dict")
        print(f"- Existing text blocks: {len(text_dict.get('blocks', []))}")
        
        # Check if PDF is encrypted
        print(f"- Is encrypted: {doc.is_encrypted}")
        print(f"- Needs password: {doc.needs_pass}")
        
        # Test font availability
        print("\n- Testing font availability:")
        fonts_to_test = ["Times-Roman", "tiro", "times-roman", "cour"]
        for font in fonts_to_test:
            try:
                # Try to create a small text box with each font
                test_rect = fitz.Rect(0, 0, 100, 20)
                result = page.insert_textbox(test_rect, "Test", fontname=font, fontsize=10)
                print(f"  {font}: {'Available' if result > 0 else 'Not available'}")
            except Exception as e:
                print(f"  {font}: Error - {e}")
        
        doc.close()
        
    except Exception as e:
        print(f"Error analyzing PDF template: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    # Define file paths
    INPUT_PDF_TEMPLATE = r'C:\personal dg\github_repo\Event-OD\letters-template\LetterofAppointment.pdf'
    INPUT_CSV_FILE = r'C:\personal dg\github_repo\Event-OD\Letters-dataset\new-members\new.csv'
    OUTPUT_DIRECTORY = r'C:\personal dg\github_repo\Event-OD\Appointment-letters\new-recruitment'

    # Debug the template first
    print("=== DEBUGGING PDF TEMPLATE ===")
    debug_pdf_template(INPUT_PDF_TEMPLATE)
    
    print("\n=== GENERATING CERTIFICATES ===")
    # Run the PDF generation function
    generate_pdf_certificates(INPUT_CSV_FILE, INPUT_PDF_TEMPLATE, OUTPUT_DIRECTORY)
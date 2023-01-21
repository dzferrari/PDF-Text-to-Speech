#!/usr/bin/env python
import argparse
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

def parse_arguments():
    """
    Parse command-line arguments and return them as a namespace object.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # Input argument
    parser.add_argument('-i', '--input', required=True, help='The path to the input PDF file')
    
    # Output argument
    parser.add_argument('-o', '--output', required=False, default=None, help='The path to the output text file')
    
    # Remove Footnotes argument. Choose the style of the footnotes, if the number is followed by a dot, the value should be dot, and if there is no dot, only a number followed by a space, the value should be space.
    parser.add_argument('-f', '--footnote-style', required=False, default='dot', choices=['dot', 'space', 'both'], help='The style of footnotes to remove. If the number is followed by a dot and a space, the value should be dot, and if there is no dot, only a number followed by a space, the value should be space.')
    
    # Remove lines that are solely composed of numbers, like page number lines.
    parser.add_argument('-n', '--remove-number-only-lines', required=False, action='store_true', help='Remove lines that are solely composed of numbers')
    
    # LAParams arguments
    parser.add_argument('-a', '--all_texts', required=False, default=True, type=bool, help='If set to True, all text will be extracted, otherwise only text that appears in the main text layer will be extracted.')
    parser.add_argument('--line_margin', required=False, type=float, default=0.5, help='The minimum space between lines (measured in points).')
    parser.add_argument('-w', '--word_margin', required=False, type=float, default=0.1, help='The minimum space between words (measured in points).')
    parser.add_argument('--char_margin', required=False, type=float, default=2.0, help='The minimum space between characters (measured in points).')
    parser.add_argument('--boxes_flow', required=False, default='LR', choices=['LR', 'RL', 'TB'], type=str, help='The direction in which the text flows. The value can be LR for left-to-right, RL for right-to-left, or TB for top-to-bottom.')
    parser.add_argument('--boxes_flow_value', required=False, type=float, default=0.5, help='The value used to determine the flow direction')
    parser.add_argument('--detect_vertical', required=False, default=False, type=bool, help='If set to True, vertical text will be detected, otherwise it will be ignored.')
    parser.add_argument('--line_overlap', required=False, type=float, default=0.5, help='The maximum amount of overlap between two lines (measured in points).')
    parser.add_argument('--detect_italic', required=False, default=False, type=bool, help='If set to True, italic text will be detected,otherwise it will be ignored.')
    parser.add_argument('--char_threshold', required=False, default=None, type=float, help='The minimum height of characters (measured in points) that will be considered text.')
    parser.add_argument('--word_threshold', required=False, default=None, type=float, help='The minimum height of words (measured in points) that will be considered text.')
    parser.add_argument('--poly_flags', required=False, default=None, type=int, help='A set of flags that control the way text is extracted from polygons.')
    
    return parser.parse_args()

def extract_text_from_pdf(pdf_path, args):
    """
    Extract the text from a PDF file and return it as a string.
    """
    # Set parameters for analysis
    laparams = set_laparams(args)
    with open(pdf_path, 'rb') as fh:
       # Create a PDF resource manager object
        rsrcmgr = PDFResourceManager()

        # Create a StringIO object to receive PDF data.
        out_text = StringIO()

        # Create a PDF page aggregator object
        device = TextConverter(rsrcmgr, out_text, laparams=laparams)

       # Create a PDF interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Extract the text from each page
        for page in PDFPage.get_pages(fh, check_extractable=True):
            interpreter.process_page(page)

        # Get the text from the StringIO object
        text = out_text.getvalue()

        # Close the device
        device.close()

        return text
        
def set_laparams(args):
    laparams = LAParams()
    
    #  If set to True, all text will be extracted, otherwise only text that appears in the main text layer will be extracted.
    laparams.all_texts = args.all_texts
    
    # The minimum space between lines (measured in points).
    laparams.line_margin = args.line_margin
    
    # The minimum space between words (measured in points).
    laparams.word_margin = args.word_margin
    
    # The minimum space between characters (measured in points).
    laparams.char_margin = args.char_margin
    
    # The direction in which the text flows. The value can be 'LR' for left-to-right, 'RL' for right-to-left, or 'TB' for top-to-bottom. Maybe it will be necessary to set the type of values to use these.
    #laparams.boxes_flow = args.boxes_flow
    #laparams.boxes_flow_value = args.boxes_flow_value
    
    #  If set to True, vertical text will be detected, otherwise it will be ignored.
    laparams.detect_vertical = args.detect_vertical
    
    # The maximum amount of overlap between two lines (measured in points).
    laparams.line_overlap = args.line_overlap
    
    # Detect if italic with True or False. Default is False.
    laparams.detect_italic = args.detect_italic
    
    # Less used parameters
    laparams.char_threshold = args.char_threshold
    laparams.word_threshold = args.word_threshold
    laparams.poly_flags = args.poly_flags
    
    return laparams

def remove_lines_by_char(text, chars):
    """
    Remove lines or paragraphs from the text that start with any of the specified characters.
    """
    lines = text.split("\n")
    new_text = ""
    found_match = False
    for line in lines:
        # Remove lines according to the first character after the empty spaces
        if any(line.startswith(c) for c in chars):
            continue
        else:
            new_text += line + "\n"
    return new_text

def remove_footnotes(text, args):
    """
    Remove the entire paragraphs that start with a number followed by a dot and an empty space (footnotes).
    """
    lines = text.split("\n")
    new_text = ""
    found_match = False
    for line in lines:
        if args.footnote_style == 'dot' and line.split(".")[0].isdigit() and line.find(".")+1 == 1: # check if the first element is a number followed by a dot and a space
            found_match = True
            continue
        elif args.footnote_style == 'space' and line.split(" ")[0].isdigit() and line.find(" ")+1 == 1: # check if the first element is a number followed by a space
            found_match = True
            continue
        elif found_match and line.strip()=="":
            found_match = False
            continue
        elif found_match:
            continue
        else:
            new_text += line + "\n"
    return new_text
    
def remove_number_only_lines(text):
    """
    Remove lines that are solely composed of numbers, like page number lines.
    """
    lines = text.split("\n")
    new_text = ""
    for line in lines:
        if line.replace(".", "").replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").isdigit():
            continue
        else:
            new_text += line + "\n"
    return new_text

def main():
    try:
    	# Parse command-line arguments
        args = parse_arguments()
        
        # Set laparams
        laparams = set_laparams(args)
        
        # Extract from PDF
        text = extract_text_from_pdf(args.input, args)
        
        # Remove lines that start with specific characters
        chars = [""]
        text = remove_lines_by_char(text, chars)
       
        # Check the input and output arguments 
        if args.output is None:
            file_name = args.input.split(".")[0] + ".txt"
        else:
            file_name = args.output
            
        # Check for Remove Footnotes arguments
        if args.footnote_style:
            text = remove_footnotes(text, args) 
            
        # Check for Remove Number Lines arguments
        if args.remove_number_only_lines:
            text = remove_number_only_lines(text)
        
        # Write to file
        with open(file_name, "w") as fh:
            fh.write(text)
    
    except FileNotFoundError:
        print(f"Error: Input file {args.input} not found.")
    #except PdfReadError as e:
    #    print(f"Error: Failed to read PDF file {args.input}. Reason: {e}")
    except Exception as e:
        print("An error occurred: ", e)

if __name__ == "__main__":
    main()

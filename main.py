from config import *
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

def set_environment():
    """Clean up output directory."""

    # Delete all files in current output directory
    file_list = [file for file in os.listdir(OUTPUT_DIR) if file.endswith(".txt")]
    for file in file_list:
        os.remove(os.path.join(OUTPUT_DIR, file))


def convert_pdf_to_txt():
    """Convert all pdf files in input directory to txt files."""

    # Get all files in input directory
    file_list = [file for file in os.listdir(INPUT_DIR) if file.endswith(".pdf")]
    #print(len(file_list))
    
    for file in file_list:
        pdf_base_filename = file[:-4]
        #print(pdf_base_filename)

        # Open and read the pdf file in binary mode
        fp = open(os.path.join(INPUT_DIR, file), "rb")

        # Create parser object to parse the pdf content
        parser = PDFParser(fp)

        # Store the parsed content in PDFDocument object
        document = PDFDocument(parser)

        # Check if document is extractable, if not abort
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
            
        # Create PDFResourceManager object that stores shared resources such as fonts or images
        rsrcmgr = PDFResourceManager()

        # set parameters for analysis
        laparams = LAParams()

        # Create a PDFDevice object which translates interpreted information into desired format
        # Device needs to be connected to resource manager to store shared resources
        # device = PDFDevice(rsrcmgr)
        # Extract the decive to page aggregator to get LT object elements
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create interpreter object to process page content from PDFDocument
        # Interpreter needs to be connected to resource manager for shared resources and device 
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Ok now that we have everything to process a pdf document, lets process it page by page
        extracted_text = ""
        for page in PDFPage.create_pages(document):
            # As the interpreter processes the page stored in PDFDocument object
            interpreter.process_page(page)
            # The device renders the layout from interpreter
            layout = device.get_result()
            # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    extracted_text += lt_obj.get_text()
                    
        #close the pdf file
        fp.close()

        # print (extracted_text.encode("utf-8"))
        new_text_filename = "raw_" + pdf_base_filename + ".txt" 
        with open(os.path.join(OUTPUT_DIR, new_text_filename), "wb+") as my_log:
            my_log.write(extracted_text.encode("utf-8"))

def sanitize_output():
    """Sanitize output file by filtering unwanted lines."""

    file_list = [file for file in os.listdir(OUTPUT_DIR) if file.endswith(".txt")]
    for file in file_list:
        with open(os.path.join(OUTPUT_DIR, file), "rb") as input_file:
            with open(os.path.join(OUTPUT_DIR, file[4:]), "wb+") as output_file: 
                for line in input_file:
                    line = line.decode("utf-8")
                    if len(line) > 2:
                        try:
                            int(line.replace(",", ""))
                        except:
                            if "△" not in line:
                                line = line.replace("　", "")
                                output_file.write(line.encode("utf-8"))
                        #int(line.decode("utf-8").replace(",", ""))

    raw_file_list = [file for file in os.listdir(OUTPUT_DIR) if file.startswith("raw_") and file.endswith(".txt")]
    for file in raw_file_list:
        print(file)
        os.remove(os.path.join(OUTPUT_DIR, file))


def main():
    # Set up environment
    set_environment()

    # Convert PDF files to TXT files
    convert_pdf_to_txt()

    # Clean output file as much as possible
    sanitize_output()


if __name__ == "__main__":
    main()
import sys
import os
import comtypes.client

from PIL import Image
import subprocess
import img2pdf

import plistlib
from fpdf import FPDF
import pandas as pd
from docx2pdf import convert
#import win32com.client



from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table


def convert_tif_to_pdf(input_file_path, output_file_path):
    try:
        # Open the image file
        image = Image.open(input_file_path)

        # Create a new PDF file
        #pdf_path = output_file_path + ".pdf"
        pdf_path = output_file_path 


        # Convert image to PDF
        if image.mode == "RGBA":
            # Convert RGBA image to RGB
            image = image.convert("RGB")
        image.save(pdf_path, "PDF", resolution=100.0)
       

        print(f"File converted: {pdf_path}")

        # Delete the input file
        image.close()
        os.remove(input_file_path)

    except IOError:
        print(f"Failed to convert image to PDF: {input_file_path}")




def convert_image_to_pdf(input_file_path, output_file_path):
    try:
        # Open the image file
        image = Image.open(input_file_path)

        # Convert image to RGB mode
        image = image.convert("RGB")

        # Create a new PDF file
        pdf_path = output_file_path

        # Convert image to PDF
        image.save(pdf_path, "PDF", resolution=100.0)

        print(f"File converted: {pdf_path}")

        # Delete the input file
        os.remove(input_file_path)

    except IOError:
        print(f"Failed to convert image to PDF: {input_file_path}")



def convert_excel_to_pdf(input_file_path, output_file_path):
    xlFormatPDF = 0

    in_file = os.path.abspath(input_file_path)
    out_file = os.path.abspath(output_file_path)

    excel = comtypes.client.CreateObject('Excel.Application')
    excel.Visible = False  # Hide Excel application window
    workbook = excel.Workbooks.Open(in_file)
    workbook.ExportAsFixedFormat(xlFormatPDF, out_file)
    workbook.Close()
    excel.Quit()
    # Delete the input file
    os.remove(input_file_path)









def convert_docx_to_pdf(input_file_path, output_file_path):
    wdFormatPDF = 17

    in_file = os.path.abspath(input_file_path)
    out_file = os.path.abspath(output_file_path)

    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False  # Hide Word application window
    word.DisplayAlerts = False  # Disable application alerts
    word.AutomationSecurity = 3  # Disable macros

    doc = word.Documents.Open(in_file)
    doc.SaveAs2(out_file, FileFormat=wdFormatPDF)
    doc.Close()

    word.Quit()
    # Delete the input file
    os.remove(input_file_path)


def convert_pptx_to_pdf(input_file_path, output_file_path):
    pdfFormat = 32

    in_file = os.path.abspath(input_file_path)
    out_file = os.path.abspath(output_file_path)

    powerpoint = comtypes.client.CreateObject('PowerPoint.Application')
    #powerpoint.Visible = False  # Hide PowerPoint application window
    powerpoint.DisplayAlerts = False  # Disable application alerts
    presentation = powerpoint.Presentations.Open(in_file)
    presentation.ExportAsFixedFormat(out_file, pdfFormat)
    presentation.Close()
    os.remove(input_file_path)
    powerpoint.Quit()
    powerpoint.DisplayAlerts = True

    # Delete the input file
    #os.remove(input_file_path)
    


def convert_file_to_pdf(input_file_path, output_folder_path):
    _, file_extension = os.path.splitext(input_file_path)
    file_extension = file_extension.lower()

    if file_extension == '.xlsx' or file_extension == '.xlsb' or file_extension == '.csv' or file_extension == '.xls':
    #if file_extension in ['.xlsx','.xlsb','.csv','.xls']:
        output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        convert_excel_to_pdf(input_file_path, output_file_path)
        
    elif file_extension in ['.docx', '.doc', '.rtf', '.dotx', '.txt', '.ics', '.plist']:
        output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        convert_docx_to_pdf(input_file_path, output_file_path)
   
    elif file_extension == '.png' or file_extension == '.jpg':
        output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        convert_image_to_pdf(input_file_path, output_file_path)

   
    elif file_extension == '.tif' or file_extension == '.gif':
        output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        convert_tif_to_pdf(input_file_path, output_file_path)
        
    
    elif file_extension == '.iwa':
        output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        convert_iwa_to_pdf(input_file_path, output_file_path)
        
    elif file_extension == '.pptx' or file_extension == '.ppt':
        output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        convert_pptx_to_pdf(input_file_path, output_file_path)
        
    else:
        print(f"Unsupported file type: {file_extension}")

# Usage example
# input_file_path = input('Enter input file path: ')
# output_folder_path = input('Enter output folder path: ')
# convert_file_to_pdf(input_file_path, output_folder_path)

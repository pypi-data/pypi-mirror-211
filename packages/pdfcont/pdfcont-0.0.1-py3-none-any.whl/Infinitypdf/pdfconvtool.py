import os
import multiprocessing
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import urllib.request
from xhtml2pdf import pisa
import pdfkit
from support6 import *
import shutil



def convert_to_pdf(input_file, output_folder_path):
   
    _, file_extension = os.path.splitext(input_file)
    val = file_extension.lower()
    if val == '.mhtml' or val == '.html' or val == '.htm' or val == '.igs' or val == '.xml':
            url = f"file:///{os.path.abspath(input_file)}"

            # Download the content of the file
            response = urllib.request.urlopen(url)

            # Create a BeautifulSoup object to parse the content
            soup = BeautifulSoup(response.read(), "html.parser")

            # Find the elements you want to scrape
            data = soup.find_all()

            # Convert the scraped data to a PDF
            output_file_name = os.path.splitext(os.path.basename(input_file))[0] + ".pdf"
            output_file_path = os.path.join(output_folder_path, output_file_name)
            with open(output_file_path, "wb") as f:
                html = "<html><head><meta charset='UTF-8'></head><body>"
                for d in data:
                    html += str(d)
                html += "</body></html>"
                pisa.CreatePDF(html, dest=f)
            print(f"File converted: {output_file_path}")
            response.close()
            os.remove(input_file) 
            
    elif val == '.pdf':
        output_file_name = os.path.basename(input_file)
        output_file_path = os.path.join(output_folder_path, output_file_name)
        shutil.copyfile(input_file, output_file_path)
        os.remove(input_file)
           
    else:
         convert_file_to_pdf(input_file, output_folder_path)

         

      

def scrape_files( input_folder_path,output_folder_path):
    
    # Disable the button to prevent multiple clicks
    convert_button.config(state=tk.DISABLED)

    # Get a list of all files in the input folder
    input_files = [os.path.join(input_folder_path, f) for f in os.listdir(input_folder_path) if
                   os.path.isfile(os.path.join(input_folder_path, f))]


    # Create a process pool and convert each file to PDF using a separate process
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = []
        for input_file in input_files:
            try:
                results.append(pool.apply_async(convert_to_pdf, args=(input_file, output_folder_path)))
            except:
                continue
        for r in results:
            r.wait()

    # Enable the button after the conversion process is completed
    convert_button.config(state=tk.NORMAL)

    folder_input_1.delete(0, tk.END)
    folder_input_2.delete(0, tk.END)



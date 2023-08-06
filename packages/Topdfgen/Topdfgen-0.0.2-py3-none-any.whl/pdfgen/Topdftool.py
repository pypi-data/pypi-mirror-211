import os
import multiprocessing
from bs4 import BeautifulSoup
import urllib.request
from xhtml2pdf import pisa
import pdfkit
#from support6 import *
import shutil


import sys
import os
import comtypes.client

from PIL import Image
import subprocess
import img2pdf

import plistlib
from fpdf import FPDF
import pandas as pd





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
   
  


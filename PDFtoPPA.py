#Read PDF invoice into a dataframe and then convert it into a csv PPA 

import fitz #PyMuPDF
import pandas as pd
import re
import csv
from openpyxl import Workbook
from openpyxl import load_workbook
import shutil

particulars = {"invoice_number": "INVOICE NO.", "date" : "JOB DATES:"}

#REQUIRES CATEGORIES IN ORDER
table_categories = ['QUANTITY','DESCRIPTION','UNIT PRICE','TOTAL']
empty_PPA = "PPA Form.xlsx"
destination_folder = r"C:\Users\ethan.green\Desktop\PPA"

department = "IT Department"
ordered_by = "Nancy Ortega"

#returns pdf text in all uppercase
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.upper()

def parse_invoice_text(text):
  #get #, date, vendor, total
  data = {}
  invoice_vender = re.search(r'(^.+)',text)
  invoice_number = re.search(r'INVOICE NO.\s*(\S+)', text)
  invoice_date = re.search(r'INVOICE DATE\s*(\S+)', text)
  invoice_total = re.search(r'TOTAL DUE\s*(\S+)', text)
  if invoice_vender:
     data['Vendor'] = invoice_vender.group(1)
  if invoice_number:
    data['Invoice Number'] = invoice_number.group(1)
  if invoice_date:
    data['Date'] = invoice_date.group(1)
  if invoice_total:
     data['Total'] = invoice_total.group(1)
  #get line items
  #still working on thiS
  lines = text.splitlines()
  items = []
  
  for line in lines:
    continue

  
  return data 

#output dataframe with invoice data (invoice number, date, line items, subtotal, etc)
def read_invoice(invoice_path):
  #read the pdf
  rawtext = extract_text_from_pdf(invoice_path)
  #print rawtext to invoice.txt for testing 
  #with open("invoice.txt", "w") as f:
    #print(rawtext, file=f)
  #parse the text to find fields for ppa
  data = parse_invoice_text(rawtext)
  return data
  #return parse_invoice_text(extract_text_from_pdf(invoice_path))



#use dataframe to create ppa 
def create_ppa(invoice_path):
  data = read_invoice(invoice_path)
  new_ppa_name ="PPA Form -" + data["Vendor"] + data["Invoice Number"] + ".xlsx"
  #destination_file = destination_folder + r"/" + new_ppa_name
  destination_file = new_ppa_name
  #Create the file for ppa
  try:
    shutil.copy(empty_PPA, destination_file)
    print(f"'{empty_PPA}' copied to '{destination_file}' successfully.")
  except FileNotFoundError:
      print(f"Error: '{empty_PPA}' not found.")
  except Exception as e:
      print(f"An error occurred: {e}")
  #open file
  workbook = load_workbook(destination_file)
  sheet = workbook.active

  sheet["L13"] = data["Vendor"]
  sheet["B13"] = department
  sheet["G19"] = data["Invoice Number"]
  sheet["B23"] = 1
  sheet["N23"] = data["Total"]
  sheet["C24"] = "job date: " +data["Date"]
  sheet["D40"] = "PPA Prepared by " + ordered_by

  workbook.save(filename=destination_file)


  return
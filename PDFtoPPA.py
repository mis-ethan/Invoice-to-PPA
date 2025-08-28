#Read PDF invoice into a dataframe and then convert it into a csv PPA 

import fitz #PyMuPDF
import pandas
import re

particulars = {"invoice_number": "INVOICE NO.", "date" : "JOB DATES:"}

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
  invoice_number = re.search(r'INVOICE NO.\s*(\S+)', text)
  invoice_date = re.search(r'INVOICE DATE\s*(\S+)', text)
  if invoice_number:
    data['Invoice Number'] = invoice_number.group(1)
  if invoice_date:
    data['Date'] = invoice_date.group(1)
  #get line items
  lines = text.splitlines()
  items = []
  start = False
  for line in lines:
      if re.match(r'QUANTITY', line):
          start = True
          items.append("starting")
          continue
      if start:
          if line.strip() == "":
              continue
          if "SUBTOTAL" in line or "TAX" in line or "TOTAL" in line:
              items.append("ending")
              break
          item = re.search(line+r'\s*(\S+)')          
          if len(parts) == 4:
              item = {
                  'Description': parts[1],
                  'Quantity': parts[0],
                  'Unit Price': parts[2],
                  'Total': parts[3]
              }
              items.append(item)

  data['Items'] = items
  
  return data 

#output dataframe with invoice data (invoice number, date, line items, subtotal, etc)
def read_invoice(invoice_path):
  #read the pdf
  rawtext = extract_text_from_pdf(invoice_path)
  #print rawtext to invoice.txt for testing 
  with open("invoice.txt", "w") as f:
    print(rawtext, file=f)
  #parse the text to find fields for ppa
  data = parse_invoice_text(rawtext)
  return data
  #return parse_invoice_text(extract_text_from_pdf(invoice_path))

#use dataframe to create ppa 
def create_ppa(ppa_path):
  #do the thing
  return

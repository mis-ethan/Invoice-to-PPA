from PDFtoPPA import read_invoice, create_ppa, extract_text_from_pdf
import re
import os
from glob import glob

directory_path = r'C:\Users\ethan.green\Desktop\Joe invoices 7-25\*.pdf'
invoice_list = glob(directory_path)

for invoice in invoice_list:
    create_ppa(invoice)

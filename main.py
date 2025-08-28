from PDFtoPPA import read_invoice, create_ppa, extract_text_from_pdf
import re

text = extract_text_from_pdf(r"C:\Users\ethan.green\Desktop\Joe invoices 7-25\1308  JD070225.pdf")

# Normalize line endings
text = text.replace('\r\n', '\n').replace('\r', '\n')

# Updated regex to handle:
# - Required: qty + description + total
# - Optional: unit price
pattern = re.compile(r'''
(?P<qty>^\d+)\s*\n                                # Quantity
(?P<desc>(?:^(?!\$\d)[^\n]+\n)+?)                 # Description lines (not starting with $)
(?:^\$(?P<unit>[\d,]+\.\d{2})\s*\n)?               # Optional unit price
^\$(?P<total>[\d,]+\.\d{2})\s*                     # Total price
''', re.MULTILINE | re.VERBOSE)

# Parse matches
results = []
for match in pattern.finditer(text):
    qty = match.group('qty')
    desc = match.group('desc').strip().replace('\n', ' ')
    unit = match.group('unit') or ''  # Unit price may be missing
    total = match.group('total')

    results.append({
        'qty': qty,
        'desc': desc,
        'unit': unit,
        'total': total
    })

# Print results
for item in results:
    print(f"Quantity: {item['qty']}")
    print(f"Description: {item['desc']}")
    print(f"Unit Price: ${item['unit']}" if item['unit'] else "Unit Price: N/A")
    print(f"Total: ${item['total']}")
    print('-' * 50)

#with open("output.txt", "w") as f:
#    print(read_invoice(r"C:\Users\ethan.green\Desktop\Joe invoices 7-25\1308  JD070225.pdf"), file=f)
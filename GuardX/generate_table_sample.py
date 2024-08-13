from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table, TableStyle, colors
import json

# my_pdf = 'table.pdf'

# Reading the Json file
with open('data.json', 'r') as file:
    json_data = json.load(file)

# Initialize the header and the data list
header = ['ID', 'Test Type', 'Payload', 'Logistic', 'Imbalanced-Class', 'Balanced-Class']
data = [header]

# Transform the JSON content into the desired format which is a tuple
for item in json_data:
    data.append((
        item['id'],
        item['testType'],
        item['payload'],
        item['logistic'],
        item['imbalance'],
        item['balance']
    ))

# Assign to the variable
my_data = data

# my_doc = SimpleDocTemplate(my_pdf, pagesize=letter)
c_width = [0.4*inch, 0.8*inch, 2.5*inch, 0.8*inch, 1.3*inch, 1.3*inch]

test_table = Table(my_data, rowHeights=20, repeatRows=1, colWidths=c_width)
# Here the index is not row,col but it is col,row
# We are setting the background color as -1 means the last value. Means we are setting the color of first row
test_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    # ('BACKGROUND', (0, 2), (-1, 2), colors.yellow) # Highlight for a row.
]))
# Fontsize is applied to the whole table. And last is highlighting a row.
# The above format is ('Change', start, end, change_value)

# elements = []
# elements.append(t)
# my_doc.build(elements)

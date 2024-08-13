from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
# from reportlab.platypus import Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from train_data import metrics

# Define your PDF filename
# my_pdf = 'metrics_table.pdf'

# Your dictionary of metrics
metrics_data = metrics

# Initialize styles and document
# styles = getSampleStyleSheet()
# my_doc = SimpleDocTemplate(my_pdf, pagesize=letter)
elements = []

# Header and data initialization
header = ['Model', 'Accuracy', 'Category', 'Precision', 'Recall', 'F1-Score', 'Support']
data = [header]

# Process each model in metrics_data
for model, metrics in metrics_data.items():
    accuracy = metrics.get("Accuracy", "")
    best_params = metrics.get("Best Parameters", "")

    # Add model level row
    data.append([model, accuracy, '', '', '', '', ''])

    # Add metrics rows
    for metric in metrics.get("Metrics", []):
        data.append(['', '', metric["Category"], metric["Precision"], metric["Recall"], metric["F1-Score"], metric["Support"]])

# Create the table
table_log = Table(data, repeatRows=1)

# Define style for table
table_log.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
    ('BACKGROUND', (0, 1), (-1, 1), colors.yellow),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
]))

# Add table to elements list
# elements.append(t)

# Build the PDF
# my_doc.build(elements)

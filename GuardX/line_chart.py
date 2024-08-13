from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, String, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import json

# my_pdf = 'linechart.pdf'

find_line_chart = Drawing(710, 200) # width, height
lc = HorizontalLineChart()

# Read the JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Initialize counters
logistic_counts = {"xss": 0, "sql_injection": 0, "shell_code": 0, "normal": 0}
imbalance_counts = {"xss": 0, "sql_injection": 0, "shell_code": 0, "normal": 0}
balance_counts = {"xss": 0, "sql_injection": 0, "shell_code": 0, "normal": 0}

# Count occurrences
for entry in data:
    logistic_type = entry["logistic"]
    imbalance_type = entry["imbalance"]
    balance_type = entry["balance"]

    if logistic_type in logistic_counts:
        logistic_counts[logistic_type] += 1

    if imbalance_type in imbalance_counts:
        imbalance_counts[imbalance_type] += 1

    if balance_type in balance_counts:
        balance_counts[balance_type] += 1

# Create the output in the specified format
data = [
    (logistic_counts["xss"], logistic_counts["sql_injection"], logistic_counts["shell_code"], logistic_counts["normal"]),
    (imbalance_counts["xss"], imbalance_counts["sql_injection"], imbalance_counts["shell_code"], imbalance_counts["normal"]),
    (balance_counts["xss"], balance_counts["sql_injection"], balance_counts["shell_code"], balance_counts["normal"])
]

# Find the maximum value using a generator expression
max_value = max(item for sublist in data for item in sublist)

# Adjust the maximum value based on its parity
if max_value % 2 == 0:
    adjusted_max_value = max_value + 4
else:
    adjusted_max_value = max_value + 5

lc.x = 50 # horizontal position
lc.y = 50 # vertical position

lc.height = 125  # height of the chart area
lc.width = 300   # width of the chart area
lc.data = data

lc.lines[0].strokeWidth = 2 # Changing the width of the line
lc.lines[1].strokeWidth = 4
lc.lines[2].strokeWidth = 2

lc.lines[0].strokeColor = colors.blue  # Changing the color of the line
lc.lines[1].strokeColor = colors.red
lc.lines[2].strokeColor = colors.green

lc.valueAxis.valueMin = 0
lc.valueAxis.valueMax = adjusted_max_value
lc.valueAxis.valueStep = 2

lc.categoryAxis.labels.boxAnchor = 'ne'
lc.categoryAxis.labels.dx = 5
lc.categoryAxis.labels.dy = -2
lc.categoryAxis.labels.angle = 30

lc.categoryAxis.categoryNames = [
    'XSS', 'SQL-Injection', 'Shellcode', 'Normal'
]

find_line_chart.add(lc, '')

# Adding the Legend/text telling success or failure
legend_x = lc.x + lc.width - 50
legend_y = lc.y + lc.height - 20

# Legend for Logistic
find_line_chart.add(Rect(legend_x, legend_y, 20, 10, fillColor=colors.blue))
find_line_chart.add(String(legend_x + 25, legend_y, 'Logistic',  fontSize=10))

# Legend for Imbalance
find_line_chart.add(Rect(legend_x, legend_y - 20, 20, 10, fillColor=colors.red))
find_line_chart.add(String(legend_x + 25, legend_y - 20, 'Imbalance', fontSize=10))

# Legend for Balance
find_line_chart.add(Rect(legend_x, legend_y - 40, 20, 10, fillColor=colors.green))
find_line_chart.add(String(legend_x + 25, legend_y - 40, 'Balance', fontSize=10))

# renderPDF.drawToFile(d, my_pdf, '')


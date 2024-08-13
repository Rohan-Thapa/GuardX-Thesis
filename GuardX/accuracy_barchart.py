from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from train_data import metrics

draw_chart = Drawing(400, 200)

# Extracting accuracy values
logistic_regression_accuracy = metrics['Logistic Regression Model']['Accuracy'] * 100
class_imbalanced_accuracy = metrics['Random Forest Model Class-imbalanced']['Accuracy'] * 100
class_balanced_accuracy = metrics['Random Forest Model Class-Balanced']['Accuracy'] * 100

data = [
 (logistic_regression_accuracy, class_imbalanced_accuracy, class_balanced_accuracy)
]

bc = VerticalBarChart()

bc.x = 50
bc.y = 50

bc.height = 150
bc.width = 300

bc.data = data

bc.strokeColor = colors.black
bc.valueAxis.valueMin = 60
bc.valueAxis.valueMax = 100
bc.valueAxis.valueStep = 10
bc.bars[0].fillColor = colors.lightgreen
bc.bars[(0, 0)].fillColor = colors.red  # The one with less accuracy

bc.categoryAxis.labels.boxAnchor = 'ne'
bc.categoryAxis.labels.dx = 8
bc.categoryAxis.labels.dy = -2
bc.categoryAxis.labels.angle = 30

bc.categoryAxis.categoryNames = ['L-R', 'R-F-I', 'R-F-B']

draw_chart.add(bc, '')
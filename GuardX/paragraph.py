from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from accuracy_barchart import data

log_ac = data[0][0] # logistic accuracy out of 100% level
imb_ac = data[0][1] # Imbalance accuarcy out of 100% level
bal_ac = data[0][2] # Balance accuarcy out of 100% level

styles = getSampleStyleSheet()
styleBH = styles["BodyText"]

styleBH.alignment = TA_LEFT
styleBH.leading = 13

train_para = Paragraph(
    '''
The above given contents are related to the <b>Machine Learning</b> model datasets which determine the model effectiveness in short terms. <br />\
These terms are crucial in evaluating machine learning models. Model Accuracy indicates overall correctness, while Precision gauges \
accuracy of positive predictions, and Recall measures the model's ability to correctly identify positive instances. F1-Score harmonizes \
Precision and Recall, offering a balanced assessment, especially useful in uneven class distributions. Support denotes how frequently \
each class appears in the dataset, providing context. In your data snippet, these metrics assess the performance of Logistic Regression \
and Random Forest models across classes like '<i>normal</i>', '<i>shell_code</i>', '<i>sql_injection</i>', and '<i>xss</i>', highlighting which model \
better predicts each class and their overall effectiveness. Here's a simplified explanation of each terms:<br />\
<b>Model Accuray</b>: This tells you how often the model makes correct predictions overall. It's a basic measure of how well the model performs. <br />\
<b>Precision</b>: Precision measures how accurate the model is when it predicts a positive outcome. It's about how many of the predicted positive results are actually true positives. <br />\
<b>Recall</b>: Recall measures how well the model captures all positive instances. It's about how many of the actual positive results the model identifies correctly. <br />\
<b>F1-Score</b>: The F1-Score combines precision and recall into a single metric. It's useful when you want to balance both precision and recall, especially if you have an uneven distribution of classes. <br />\
<b>Support</b>: Support simply tells you how many times each class appears in your dataset. It gives context to the performance metrics by showing the distribution of classes. <br />\
In my data, these metrics are used to evaluate how well different models classify different types of data. The metrics help us to understand which model performs better for each class overall.<br />\
    ''', styleBH
)

bar_chart_legend = Paragraph(
    f'''
<b><i>Note</i>:</b><br />> L-R: Logistic Regression (accuracy: <i>{log_ac}%</i>)<br />> R-F-I: Random Forest Imbalance (accuracy: <i>{imb_ac}%</i>) \
<br />> R-F-B: Random Forest Balanced (accuracy: <i>{bal_ac}%</i>)<br /><br />*Red Bar-Chart: Accuracy not adequet<br />*Lighgreen Bar-Chart: Acceptable accuracy
    ''', styleBH
)

bar_para = Paragraph(
    '''
As we can see above that the <b>Bar-Chart</b> has been created with the values of accuracy which the models possesses. Since we all know <i>Logistic Regression</i> \
models are not suitable for the kind of task which I have done but just to prove the concept that these models works very bad with them and works perfectly with \
<i>Random Forest</i> models especally with <b><i>N-Gram Algorithms</i></b>.<br />These models are just a proof of concept which I want to present through this project. \
As in this project I have used multiple models which is helpful for understanding the deeper concepts about how each models works and why in one project one has \
benifits and not others.
    ''', styleBH
)

line_para = Paragraph(
    '''
In this project we do have three different models perdecting any <i>malicious</i> payloads for the web applications. While the thing I want to show in the above \
<b>Line-Chart</b> is how many labels have been provided to the inputs provided for the test. As both the <i>Balanced</i> and <i>Imbalanced</i> Random Foreset models \
are similar in nature so their labelling are also similar so I have make one line thicker than other so it can be easily detected and sperated as most of the time \
they do overlap.
    ''', styleBH
)

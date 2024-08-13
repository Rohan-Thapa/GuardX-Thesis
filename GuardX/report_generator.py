from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import datetime
# import importlib

# Importing your custom modules
from generate_table_sample import test_table
from log_table import table_log
from paragraph import train_para, bar_chart_legend, bar_para, line_para
from accuracy_barchart import draw_chart
from line_chart import find_line_chart

def gen_rep():
    pdf_path = "./static/report.pdf"
    logo_path = "./static/image/report_logo.png"
    logo_text = "GuardX Sentinel"

    current_date = datetime.now().date()

    # importlib.reload(test_table)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.translate(inch, inch)  # margin 1 inch on each side

    page_width, page_height = letter  # 612.0 792.0 this is the pixel size of the page.
    middle_top_x = page_width / 2
    middle_top_y = page_height - inch

    # putting the image
    logo_width = 1.5 * inch
    logo_height = 1.5 * inch
    c.drawImage(logo_path, middle_top_x - 1.55 * inch, middle_top_y - 1.55 * inch, width=logo_width, height=logo_height)  # (image, x, y)

    # Place the text below the logo on top
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(0.180, 0.180, 0.255)  # main color of the site is #2E2E41 which is set here.
    text_width = c.stringWidth(logo_text)
    c.drawString(middle_top_x - text_width / 2 - 0.8 * inch, middle_top_y - 1.75 * inch, logo_text)

    # Top line
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.line(-40, 585, 510, 585)

    # Bottom line
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.line(-40, -10, 510, -10)

    # Bottom text
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.3, 0.3, 0.3)  # Bottom text color
    c.drawString(-30, -25, "Page 1 | GuardX Sentinel by Ineffable Inc. || Designed by Rohan Thapa ||")

    # putting the watermark on the pdf file
    c.rotate(45)  # here we are rotating our canvas with the degree value and we need to again rotate with negative same value if we want to add something later on the canvas.
    c.setFillColorCMYK(0, 0, 0, 0.1)  # a very faint color for watermark
    c.setFont('Helvetica', 100)  # giving bigger font size
    c.drawString(2 * inch, 1 * inch, 'GUARDX')  # Watermark string
    c.rotate(-45)  # restoring the canvas again.

    # Adding the log data table
    table_log.wrapOn(c, page_width, page_height)
    table_log.drawOn(c, -0.2 * inch, 4.5 * inch)

    # Top text with title
    c.setFont("Helvetica", 22)
    c.setFillColorRGB(0.4, 0.8, 1)  # Value of #66CCFF
    c.drawString(-0.1 * inch, 7.7 * inch, "Model Trained Value Details")

    # Train Data Note Note text
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2627, 0.2627, 0.329)  # Value of #434354
    c.drawString(-0.1 * inch, 4 * inch, "*Note: The YELLOW Highlight is for accuracy less than 0.9")

    # Adding a paragraph
    train_para.wrapOn(c, 500, 600)
    train_para.drawOn(c, -0.15 * inch, 0.05 * inch)

    c.showPage()

    # -----------------------------------------------------------page break----------------------------------------

    # Second Page
    # Name of the Logo
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(0.180, 0.180, 0.255)  # main color of the site is #2E2E41 which is set here.
    text_width = c.stringWidth(logo_text)
    c.drawString(40, 10.05 * inch, logo_text)

    # Top line
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.line(33, 715, 580, 715)

    # Bottom line
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.line(33, 40, 580, 40)

    # Bottom text
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.3, 0.3, 0.3)  # Bottom text color
    c.drawString(45, 23, f"Page 2 | GuardX Sentinel by Ineffable Inc. || Designed by Rohan Thapa ||")

    # putting the watermark on the pdf file
    c.rotate(45)  # rotating the canvas for watermark
    c.setFillColorCMYK(0, 0, 0, 0.1)  # a very faint color for watermark
    c.setFont('Helvetica', 100)  # giving bigger font size
    c.drawString(4.5 * inch, 0.6 * inch, 'GUARDX')  # Watermark string
    c.rotate(-45)  # restoring the canvas

    draw_chart.wrapOn(c, 400, 400)
    draw_chart.drawOn(c, 3 * inch + 10, 6.5 * inch)  # vertical bar chart

    # Adding a Legend barchart
    bar_chart_legend.wrapOn(c, 220, 200)
    bar_chart_legend.drawOn(c, 0.5 * inch, 7.5 * inch)

    # Accuracy Chart Text
    c.setFont("Helvetica", 19)
    c.setFillColorRGB(0.2627, 0.2627, 0.329)  # Value of #434354
    c.drawString(1.9 * inch, 9.6 * inch, "Different Models Accuracy In Bar-Chart")

    find_line_chart.wrapOn(c, 810, 200)
    find_line_chart.drawOn(c, 1.5 * inch, 2 * inch)

    # Adding Paragraph between bar-chart and line-chart
    bar_para.wrapOn(c, 500, 600)
    bar_para.drawOn(c, 0.8 * inch, 5.25 * inch)

    # Bar-Chart Note text
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2627, 0.2627, 0.329)  # Value of #434354
    c.drawString(0.9 * inch, 6.7 * inch, "*Note: The Logistic Regression is not useful here.")

    # Line-Chart Note text
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2627, 0.2627, 0.329)  # Value of #434354
    c.drawString(0.9 * inch, 1.8 * inch, "*Note: Due to same value sometimes line do overlap each other.")

    # No. of Detection Text
    c.setFont("Helvetica", 19)
    c.setFillColorRGB(0.2627, 0.2627, 0.329)  # Value of #434354
    c.drawString(1.9 * inch, 4.8 * inch, "No. of Detection done by Models")

    # Adding Paragraph below line-chart
    line_para.wrapOn(c, 500, 600)
    line_para.drawOn(c, 0.8 * inch, 0.7 * inch)

    c.showPage()

    # -----------------------------------------------------------page break----------------------------------------

    # Third Page
    # Name of the Logo
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(0.180, 0.180, 0.255)  # main color of the site is #2E2E41 which is set here.
    text_width = c.stringWidth(logo_text)
    c.drawString(40, 10.05 * inch, logo_text)

    # Top line
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.line(33, 715, 580, 715)

    # Bottom line
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.line(33, 40, 580, 40)

    # Bottom text
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.3, 0.3, 0.3)  # Bottom text color
    c.drawString(45, 23, f"Page 3 | GuardX Sentinel by Ineffable Inc. || Designed by Rohan Thapa ||")

    # putting the watermark on the pdf file
    c.rotate(45)  # rotating the canvas for watermark
    c.setFillColorCMYK(0, 0, 0, 0.1)  # a very faint color for watermark
    c.setFont('Helvetica', 100)  # giving bigger font size
    c.drawString(4.5 * inch, 0.6 * inch, 'GUARDX')  # Watermark string
    c.rotate(-45)  # restoring the canvas

    # Adding the test results in 2nd page
    test_table.wrapOn(c, page_width, page_height)
    test_table.drawOn(c, 0.7 * inch, 1.5 * inch)

    # Getting current date
    formatted_date = current_date.strftime('%Y-%m-%d')

    # Result Text
    c.setFont("Helvetica", 22)
    c.setFillColorRGB(0.2627, 0.2627, 0.329)  # Value of #434354
    c.drawString(2 * inch, 9.6 * inch, f"Result on the Test ({formatted_date})")

    # Result Table Note text
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2627, 0.2627, 0.329)  # Value of #434354
    c.drawString(0.9 * inch, 9.3 * inch, "*Note: This is the same data as website, and table grows from bottom so it is below.")

    c.showPage()

    c.save()

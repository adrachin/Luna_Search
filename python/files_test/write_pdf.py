from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from urllib.parse import quote
import os

def validate_path(path):
    return os.path.exists(path)

def create_pdf(input_file, output_file):
    # Seitenmaße für Querformat anpassen
    width, height = letter[1], letter[0]
    c = canvas.Canvas(output_file, pagesize=(width, height))

    with open(input_file, 'r', encoding='utf-8') as file:
        y_position = height - 40  # Start etwas unterhalb des oberen Randes
        for line in file:
            line = line.strip()
            if validate_path(line):
                volume = line.split('/')[2]
                project_name = line.split('/')[-1]
                finder_link = f"file://{quote(line)}"
                luna_link = f"luna://{quote(line)}"

                # Text und Links hinzufügen
                c.drawString(50, y_position, f"Projekt: {project_name}  Volume: {volume}")
                c.linkURL(finder_link, (50, y_position-10, width-50, y_position+10), relative=1)
                c.drawString(50, y_position - 20, "Im Finder öffnen (Link)")
                c.linkURL(luna_link, (50, y_position - 30, width-50, y_position - 10), relative=1)
                c.drawString(50, y_position - 40, "In Luna öffnen (Link)")
                y_position -= 60  # Abstand zwischen den Einträgen erhöhen
                if y_position < 40:  # Neue Seite beginnen, wenn der untere Rand erreicht ist
                    c.showPage()
                    y_position = height - 40

    c.save()

# Pfad zur Textdatei und zum PDF
text_file_path = '/Users/thomas/_python/MyApps/Luna_Search/templates/treffer.txt'
pdf_output_path = '/Users/thomas/_python/MyApps/Luna_Search/templates/Luna_projects.pdf'
create_pdf(text_file_path, pdf_output_path)

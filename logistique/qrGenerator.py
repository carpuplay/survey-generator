import qrcode
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Dossier de sortie et fichier PDF
output_folder = "qr_codes"
os.makedirs(output_folder, exist_ok=True)
pdf_filename = os.path.join(output_folder, "qr_codes_with_labels.pdf")

# Liste des zones de rangement
zones = [
    "A - 1", "A - 2", "A - 3", "A - 4", "A - 5", "A - 6", "A - 7", "A - 8",
    "B - 1", "B - 2", "B - 3", "B - 4", "B - 5", "B - 6", "B - 7", "B - 8", "B - 9",
    "C - 1", "C - 2", "C - 3", "C - 4", "C - 5", "C - 6", "C - 7", "C - 8", "C - 9"
]

# Dimensions PDF
c = canvas.Canvas(pdf_filename, pagesize=A4)
page_width, page_height = A4

# Configuration des marges et des tailles
margin = 50
qr_size = 150
label_height = 30
row_spacing = 50  # Espacement vertical entre les QR codes
col_spacing = 50  # Espacement horizontal entre les QR codes

# Calcul du nombre de QR codes par ligne et par colonne
usable_width = page_width - 2 * margin
usable_height = page_height - 2 * margin
qr_per_row = usable_width // (qr_size + col_spacing)
qr_per_col = usable_height // (qr_size + label_height + row_spacing)

# Centrage horizontal et vertical
horizontal_padding = (usable_width - qr_per_row * (qr_size + col_spacing)) / 2 + margin
vertical_padding = (usable_height - qr_per_col * (qr_size + label_height + row_spacing)) / 2 + margin

# Coordonnées de départ
x_start = horizontal_padding
y_start = page_height - vertical_padding - qr_size

x, y = x_start, y_start

# Génération des QR codes et ajout au PDF
for zone in zones:
    # Générer QR code
    qr = qrcode.make(zone)
    qr_file = os.path.join(output_folder, f"{zone.replace(' ', '_')}.png")
    qr.save(qr_file)

    # Ajouter QR code au PDF
    c.drawImage(qr_file, x, y, width=qr_size, height=qr_size)

    # Ajouter le texte sous le QR code
    text_x = x + (qr_size / 2)  # Centrer le texte sous le QR code
    text_y = y - 10
    c.setFont("Helvetica-Bold", 14)  # Police plus grande et plus visible
    c.drawCentredString(text_x, text_y, zone)

    # Supprimer le fichier .png après utilisation
    os.remove(qr_file)

    # Mise à jour des coordonnées
    x += qr_size + col_spacing
    if x + qr_size > page_width - margin:
        x = x_start
        y -= qr_size + label_height + row_spacing
        if y < margin + label_height:
            c.showPage()
            x, y = x_start, y_start

# Sauvegarde du PDF
c.save()
print(f"QR codes avec étiquettes enregistrés dans : {pdf_filename}")

import uuid
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PIL import Image
import os

def draw_boxes(c, x, y, label, box_count, box_size, spacing):
    """Dessine une ligne de cases pour chaque lettre."""
    c.drawString(x, y, label)  # Étiquette de la ligne
    x_position = x  # Position initiale des cases
    for _ in range(box_count):
        c.rect(x_position, y, 3/4 * box_size, box_size)  # Dessiner une case
        x_position += spacing  # Espace entre les cases  

def drawLines(c, x, y, length, count, spacing):
    """Dessine des lignes rouges horizontales."""
    c.setStrokeColorRGB(1, 0, 0)  # Couleur rouge
    for i in range(count):
        c.line(x, y - i * spacing, x + length, y - i * spacing)

def draw_targets(c, positions, size=5):
    """Dessine des cibles (petits cercles) aux positions spécifiées."""
    for (x, y) in positions:
        c.rect(x, y, size, size, fill=1)

def draw_grid(c, top_left, bottom_right, x_spacing=1*cm, y_spacing=1*cm):
    """Dessine une grille alignée avec les cibles."""
    x_start, y_start = top_left
    x_end, y_end = bottom_right

    # Lignes verticales
    x = x_start
    while x <= x_end:
        c.line(x, y_start, x, y_end)
        x += x_spacing

    # Lignes horizontales
    y = y_start
    while y >= y_end:
        c.line(x_start, y, x_end, y)
        y -= y_spacing

def generate_qr_code(data, fileName):
    """Génère un QR code pour les données et enregistre l'image dans un fichier."""
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(fileName)
    return fileName  # Retourner le chemin du fichier

def enqueteIDGenerator():
    return str(uuid.uuid4())[:4]

def header(c, enqueteID, qrCodeImage, title):
    '''Contenu : Nom, Prenom, Date de naissance, Sexe, identifiant numerique, qr code, cibles'''

    # Positions des cibles en haut
    positions = [
        (1 * cm, A4[1] - 1 * cm),  # Coin supérieur gauche
        (1 * cm, A4[1] - A4[1] / 4 + 1 * cm),  # Bas gauche de la section en-tête
        (A4[0] - 1 * cm, A4[1] - A4[1] / 4 + 1 * cm),  # Bas droite de la section en-tête
        (A4[0] - 1 * cm, A4[1] - 1 * cm)  # Coin supérieur droit
    ]
    draw_targets(c, positions)

    # Dessiner la grille en utilisant les positions de cibles pour délimiter les coins
    top_left = (1 * cm, A4[1] - 1 * cm)
    bottom_right = (A4[0] - 1 * cm, A4[1] - A4[1] / 4)
    #draw_grid(c, top_left, bottom_right)

    # QR code en haut à droite
    qr_code_size = 2 * cm
    c.drawImage(qrCodeImage, A4[0] - qr_code_size - 1 * cm, A4[1] - qr_code_size - 1 * cm, width=qr_code_size, height=qr_code_size)
    
    c.setFont("Helvetica", 8)
    c.drawString(1 * cm, A4[1] - A4[1] / 4 + 0.5 * cm, f" {enqueteID}")
    c.drawString(10 * cm, A4[1] - A4[1] / 4 + 0.5 * cm, "(Veuillez détacher cette partie)")

    # Ligne de découpe
    c.setDash(1, 2)  # Ligne pointillée
    c.line(0.5 * cm, A4[1] - A4[1] / 4, A4[0] - 0.5 * cm, A4[1] - A4[1] / 4)
    c.setDash()

    # Titre centré
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(A4[0] / 2, A4[1] - 1 * cm, title)

    # Champs Nom et Prénom dans la grille
    c.setFont("Helvetica", 8)
    c.drawString(3.25 * cm, A4[1] - 2.25 * cm, "(Écrivez uniquement dans les cases)")

    c.setFont("Helvetica", 12)
    c.drawString(1 * cm, A4[1] - 3.5 * cm, "Nom:")
    draw_boxes(c, 3 * cm, A4[1] - 3.5 * cm, "", box_count=12, box_size=1 * cm, spacing=0.75 * cm)

    c.drawString(1 * cm, A4[1] - 4.75 * cm, "Prénom:")
    draw_boxes(c, 3 * cm, A4[1] - 4.75 * cm, "", box_count=12, box_size=1 * cm, spacing=0.75 * cm)

    # Champ Sexe
    c.drawString(1 * cm, A4[1] - 5.5 * cm, "Sexe:")
    c.drawString(2.5 * cm, A4[1] - 5.5 * cm, "H")
    c.rect(3 * cm, A4[1] - 5.5 * cm, 0.5 * cm, 0.5 * cm)  # Case H
    c.drawString(4 * cm, A4[1] - 5.5 * cm, "F")
    c.rect(4.5 * cm, A4[1] - 5.5 * cm, 0.5 * cm, 0.5 * cm)  # Case F
    c.drawString(5.25 * cm, A4[1] - 5.5 * cm, "Autre:")
    c.rect(6.5 * cm, A4[1] - 5.5 * cm, 0.5 * cm, 0.5 * cm)  # Case Autre

    # Champ Date de naissance
    c.setFont("Helvetica", 8)
    c.drawString(13 * cm, A4[1] - 4.25 * cm, "( JJ / MM / AAAA )")

    c.setFont("Helvetica", 12)
    c.drawString(9 * cm, A4[1] - 5.5 * cm, "Date de naissance:")
    draw_boxes(c, 13 * cm, A4[1] - 5.5 * cm, "", box_count=8, box_size=1 * cm, spacing=0.75 * cm)



    return

def versoHeader(c, enqueteID):
    '''Ne pas remplir'''
    # Texte "Ne pas remplir cette partie"
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(A4[0] / 2, A4[1] - 1 * cm, "Ne pas remplir cette partie")
    c.drawCentredString(A4[0] / 2, A4[1] - 6 * cm, "Ne pas remplir cette partie")

    # Lignes diagonales
    c.setLineWidth(1)
    c.line(1 * cm, A4[1] - 1 * cm, A4[0] - 1 * cm, A4[1] - A4[1] / 4 + 1 * cm)
    c.line(1 * cm, A4[1] - A4[1] / 4 + 1 * cm, A4[0] - 1 * cm, A4[1] - 1 * cm)

    c.setDash(1, 2)  # Ligne pointillée
    c.line(0.5 * cm, A4[1] - A4[1] / 4, A4[0] - 0.5 * cm, A4[1] - A4[1] / 4)
    c.setDash()

    c.setFont("Helvetica", 8)
    c.drawString(1 * cm, A4[1] - A4[1] / 4 + 0.5 * cm, f" {enqueteID}")

    return

def survey(c, enqueteID, qrCodeImagePath, fileId):
    '''Contenu : Identifiant numerique, qr code, cibles, questionaire'''
    print(f"\033[93m{fileId}\033[0m")
    positions = [
        (1 * cm, A4[1] - A4[1] / 4 - 1 * cm),  # Top-left of the survey area
        (A4[0] - 1 * cm, A4[1] - A4[1] / 4 - 1 * cm),  # Skip top-right for QR code
        (1 * cm, 1 * cm),                      # Bottom-left
        (A4[0] - 1 * cm, 1 * cm)               # Bottom-right
    ]

    draw_targets(c, positions)

    # Grille pour la partie inférieure
    top_left = (1 * cm, A4[1] - A4[1] / 4 - 1 * cm)
    bottom_right = (A4[0] - 1 * cm, 1 * cm)
    draw_grid(c, top_left, bottom_right)

    # QR code en haut à droite
    qr_code_size = 1 * cm  
    top_right_position = (A4[0] - 1 * cm, A4[1] - A4[1] / 4 - 1 * cm)
    c.drawImage(qrCodeImagePath, top_right_position[0] - qr_code_size, top_right_position[1] - qr_code_size, width=qr_code_size, height=qr_code_size)

    # QR code gauche
    fileIdQrCodeImagePath = generate_qr_code(fileId, f"fileId_{fileId}.png")
    c.drawImage(fileIdQrCodeImagePath, top_right_position[0] - 1.5 * qr_code_size - 0.5 * cm, top_right_position[1] - qr_code_size, width=qr_code_size, height=qr_code_size)

    if os.path.exists(fileIdQrCodeImagePath):
        os.remove(fileIdQrCodeImagePath)
        print(fileIdQrCodeImagePath, "remooved")

    c.setFont("Helvetica", 8)
    c.drawString(1 * cm, 0.5 * cm, f"{enqueteID}")

    return

def generateFile(fileName, title, enqueteID):
    c = canvas.Canvas(fileName, pagesize=A4)

    
    qrCodeImagePath = generate_qr_code(enqueteID, "enqueteId.png")

    fileId = enqueteIDGenerator()
    
    header(c, enqueteID, qrCodeImagePath, title)
    survey(c, enqueteID, qrCodeImagePath, fileId + str(c.getPageNumber()))
    
    c.showPage()  # Commence une nouvelle page
    versoHeader(c, enqueteID)
    survey(c, enqueteID, qrCodeImagePath, fileId + str(c.getPageNumber()))

    c.save()
    print(f"\033[92mQuestionnaire saved as {fileName} with ID {enqueteID}\033[0m")
    print(f"\033[92mThe file has {c.getPageNumber()-1} pages\033[0m")


for i in range(10):
    generateFile("mamadou" + str(i) + ".pdf", "Enquête sur l'Amélioration des Services", "dc9c")

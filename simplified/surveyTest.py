import uuid
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PIL import Image


def draw_boxes(c, x, y, label, box_count=20, box_size=12, spacing=15):
    """Dessine une ligne de cases pour chaque lettre."""
    c.drawString(x, y, label)  # Étiquette de la ligne
    x_position = x + 100  # Position initiale des cases
    for _ in range(box_count):
        c.rect(x_position, y - box_size + 2, box_size, box_size)  # Dessiner une case
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



def generate_qr_code(data):
    """Génère un QR code pour les données et enregistre l'image dans un fichier."""
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save("qrcode.png")
    return "qrcode.png"  # Retourner le chemin du fichier

def uniqueIdGenerator():
    return str(uuid.uuid4())


def header(c, uniqueId, qrCodeImage):
    '''Contenu : Nom, Prenom, Date de naissance, Sexe, identifiant numerique, qr code, cibles'''
    positions = [
        (1 * cm, A4[1] - 1 * cm),  # Coin supérieur gauche
        (1 * cm, A4[1] - A4[1] / 4 + 1 * cm),  # Bas gauche de la section en-tête
        (A4[0] - 1 * cm, A4[1] - A4[1] / 4 + 1 * cm)  # Bas droite de la section en-tête
    ]
    draw_targets(c, positions)

    # Ajouter le QR code en haut à droite de la feuille
    qr_code_size = 2 * cm  # Taille du QR code
    c.drawImage(qrCodeImage, A4[0] - qr_code_size - 1 * cm, A4[1] - qr_code_size - 1 * cm, width=qr_code_size, height=qr_code_size)
    
    c.setFont("Helvetica", 8)
    c.drawString(1 * cm, A4[1] - A4[1] / 4 + 0.5 * cm, f"Identifiant unique : {uniqueId}")

    # Ajouter une ligne de découpe à 1/4 de la feuille A4
    c.setDash(1, 2)  # Définir le style de ligne pointillée
    c.line(0.5 * cm, A4[1] - A4[1] / 4, A4[0] - 0.5 * cm, A4[1] - A4[1] / 4)
    c.setDash()  # Réinitialiser le style de ligne

    return


def survey(c, uniqueId, qrCodeImagePath):
    '''Contenu : Identifiant numerique, qr code, cibles, questionaire'''

    positions = [
        (1 * cm, A4[1] - A4[1] / 4 - 1 * cm),  # Top-left of the survey area
        # (A4[0] - 1 * cm, A4[1] - A4[1] / 4 - 1 * cm),  # Skip top-right for QR code
        (1 * cm, 1 * cm),                      # Bottom-left
        (A4[0] - 1 * cm, 1 * cm)               # Bottom-right
    ]

    draw_targets(c, positions)

    qr_code_size = 2 * cm  
    top_right_position = (A4[0] - 1 * cm, A4[1] - A4[1] / 4 - 1 * cm)
    c.drawImage(qrCodeImagePath, top_right_position[0] - qr_code_size, top_right_position[1] - qr_code_size, width=qr_code_size, height=qr_code_size)

    c.setFont("Helvetica", 8)
    c.drawString(1 * cm, 0.5 * cm, f"Identifiant unique : {uniqueId}")
    return


def generateFile(fileName):
    c = canvas.Canvas(fileName, pagesize=A4)
    uniqueId = uniqueIdGenerator()

   
    qrCodeImagePath = generate_qr_code(uniqueId)

    
    header(c, uniqueId, qrCodeImagePath)
    survey(c, uniqueId, qrCodeImagePath)

    c.save()
    print(f"\033[92mQuestionnaire saved as {fileName} with ID {uniqueId}\033[0m")

generateFile("mamadou.pdf")

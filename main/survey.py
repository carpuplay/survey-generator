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

def draw_target(c, position, size=2):
    """Dessine un points aux positions spécifiées"""
    
    

def draw_targets(c, positions, size=2):
    """Dessine des cibles (petits cercles) aux positions spécifiées."""
    for (x, y) in positions:
        c.circle(x, y, size, fill=1)  # Rempli la cible pour une meilleure détection

def generate_qr_code(data):
    """Génère un QR code pour les données et retourne l'image du QR code."""
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

def generate_detachable_survey_with_qr(filename, questions):
    # Générer un identifiant unique pour la feuille
    unique_id = str(uuid.uuid4())

    # Générer le QR code pour l'identifiant unique
    qr_code_image = generate_qr_code(unique_id)
    qr_code_image.save("qr_code.png")

    # Création du document PDF
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Ajouter l'en-tête de type H1
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 30, "Enquête statistique : Amélioration des services du FabLab")

    # Ajouter des cibles dans les coins de la partie supérieure (détachable)
    top_target_positions = [(20, height - 20), (width - 20, height - 20), (20, height - 180), (width - 20, height - 180)]
    draw_targets(c, top_target_positions)

    # Partie supérieure (détachable) avec informations personnelles en cases
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 50, "Informations personnelles (à détacher)")
    draw_boxes(c, 50, height - 70, "Nom :", box_count=15)
    draw_boxes(c, 50, height - 90, "Prénom :", box_count=15)
    draw_boxes(c, 50, height - 110, "Date de naissance (JJ/MM/AAAA) :", box_count=10, spacing=15)

    # Sexe (cases spécifiques)
    c.drawString(50, height - 130, "Sexe :")
    c.rect(100, height - 140, 12, 12)  # Case pour M
    c.drawString(115, height - 140, "M")
    c.rect(150, height - 140, 12, 12)  # Case pour F
    c.drawString(165, height - 140, "F")

    # Identifiant unique de la feuille
    c.drawString(50, height - 160, f"Identifiant de feuille : {unique_id}")

    # Ajouter le QR code en haut à droite de la partie détachable
    c.drawImage("qr_code.png", width - 3*cm, height - 3*cm, width=1.5*cm, height=1.5*cm)

    # Ligne de séparation pour indiquer le découpage
    c.line(50, height - 170, width - 50, height - 170)
    c.drawString(50, height - 180, "(Détacher cette partie supérieure et la conserver séparément)")

    # Partie inférieure : uniquement l'identifiant de feuille et le questionnaire
    c.drawString(50, height - 220, f"Identifiant de feuille : {unique_id}")

    # Ajouter des cibles dans les coins de la partie inférieure
    bottom_target_positions = [(20, 50), (width - 20, 50), (20, height - 220), (width - 20, height - 220)]
    draw_targets(c, bottom_target_positions)

    # Ajouter le QR code en haut à droite de la partie inférieure
    c.drawImage("qr_code.png", width - 3*cm, height - 230, width=2*cm, height=2*cm)

    # Ajouter les questions
    y_position = height - 250
    for idx, question in enumerate(questions):
        c.drawString(50, y_position, f"{idx+1}. {question}")
        y_position -= 30

    # Enregistrer le PDF
    c.save()
    print(f"Questionnaire saved as {filename} with ID {unique_id}")



def uniqueIdGenerator():
    return str(uuid.uuid1())

def header(c, uniqueId, qrCodeImage):
    '''Contenu : Nom, Prenom, Date de naissance, Sexe, identifiant numerique, qr code, cibles'''


    return 0

def survey(c, uniqueId, qrCodeImage):
    '''Contenu : Identifiant numerique, qr code, cibles, questionaire'''

    return 0

def generateFile(fileName):

    c = canvas.Canvas(fileName, pagesize=A4)
    uniqueId = uniqueIdGenerator()

    qrCodeImage = generate_qr_code(uniqueId)
    qrCodeImage.save("qr_code.png")

    header(c, uniqueId)
    survey(c, uniqueId)

    c.save()
    print(f"Questionnaire saved as {fileName} with ID {uniqueId}")



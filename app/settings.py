import argparse

DEBUG_MODE = True
HEADLESS_MODE = True
IMPORT_LINKS = True
REFRESH_EXISTING = False    # Check existing Cons against portal.


# Initialize parser
parser = argparse.ArgumentParser()


# Add arguments
parser.add_argument('--level', type=str, required=False, help='debug for more verbose output.')
parser.add_argument('--links', type=str, required=False, help='import to use already saved links.')
parser.add_argument('--found', type=str, required=False, help='refresh to refresh existing items.')


# Parse arguments
args = parser.parse_args()
DEBUG_MODE = args.level.lower() == 'debug'
IMPORT_LINKS = args.links.lower() == "import"
REFRESH_EXISTING = args.found.lower() == "refresh"


LINES_PER_PAGE = "500"
SITE_ROOT = "https://www.marchespublics.gov.ma/"
SITE_INDEX = "https://www.marchespublics.gov.ma/index.php"
LINK_PREFIX = 'https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseDetailConsultation&refConsultation='
LINK_STITCH = '&orgAcronyme='

PORTAL_DDL_PAST_DAYS = 1 
PORTAL_DDL_FUTURE_DAYS = 365 * 5
PORTAL_PUB_PAST_DAYS = 365 * 2
PORTAL_PUB_FUTURE_DAYS = 0

LOADING_TIMEOUT = 1000 * 91
REQ_TIMEOUT = 90
DLD_TIMEOUT = 600

LOG_TIME_FORMAT = '%d/%m-%H:%M:%S'

DB_SERVER = '94.72.98.224'
DB_PORT = 46191
DB_NAME = "emarches"
DB_USER = "archer"
DB_PASS = "Ori9imChannay#wan"


PUDATE = "Date Publication"
DDLINE = "Deadline"
REFERE = "Reference"
CATEGC = "Categorie Consultation"
NUMBLO = "Nombre Lots"
OBJETC = "Objet Consultation"
LIEUEX = "Lieu Execution"
ACHETE = "Acheteur Public"
TYPEAN = "Type Annonce"
PROCED = "Procedure Annonce"
MODEPA = "Mode Passation"
REPONS = "Reponse Electronique"
LOTSSS = "Lots"
PRIXPL = "Prix Plans"
DOMAIN = "Domaines Activite"
RETDOS = "Adresse Retrait Dossiers"
DEPOFF = "Adresse Dépot Offres"
LIEOUV = "Lieu Ouverture Plis"
CONTNM = "Nom Contact"
CONTML = "Email Contact"
CONTTL = "Tel. Contact"
CONTFX = "Fax Contact"
IDENTI = "Identifiant"
LINKKK = "Lien Portail"
PORTID = "ID Portail"
ACRONY = "Acronyme"
LOTNMB = "Lot Numero"
OBJETL = "Objet Lot"
CATEGL = "Categorie Lot"
DESCRI = "Description"
ESTIMA = "Estimation"
CAUTIO = "Caution Provisoire"
RESPME = "Reservé PME"
QUALIF = "Qualifications"
AGREME = "Agrements"
ECHANT = "Echantillons"
REUNIO = "Reunions"
VISITS = "Visites des Lieux"
VARIAN = "Variante"
DCESIZ = "Taille DCE"

ECHAND = "Date_Echantillons"
ECHANA = "Adresse_Echantillons"
REUNID = "Date_Reunion"
REUNIA = "Adresse_Reunion"
VISITD = "Date_Visite_Lieux"
VISITA = "Adresse_Visite_Lieux"

CANCEL = "Annulee"

RVDATE = 'Date'
RVLIEU = 'Lieu'

NA_PLH = ''
TRUNCA = 32

# WORKING_DIR = '/var/opt/emarches'
MEDIA_ROOT  = '/var/opt/emarches/media'
SELENO_LOGS_DIR = '/var/opt/seleno/logs'
SELENO_DIR = '/var/opt/seleno'
DL_PATH_PREFIX = 'DCE-'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    # 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    # 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
]

DCE_CREDS = [
#    {'fname': 'Yassine', 'lname': 'Majdi', 'email': 'majidiyas81@gmail.com'},
    {'fname': 'Zouhir', 'lname': 'Ferdakou', 'email': 'ferdakouzou@yahoo.fr'},
    {'fname': 'Najat', 'lname': 'Ouihlane', 'email': 'n.ouihlane@gmail.com'},
    {'fname': 'LaPalme', 'lname': 'DuSahara', 'email': 'lapalmedusaharasarl@gmail.com'},
    {'fname': 'Mohammed', 'lname': 'Ait Rahou', 'email': 'med73aitrahou@gmail.com'},
    {'fname': 'Mohamed', 'lname': 'Bouenzar', 'email': 'm.bouenzar.sarl@yahoo.com'},
    {'fname': 'Khadija', 'lname': 'Laamiri', 'email': 'kh.laamiri.kh@gmail.com'},
    {'fname': 'Majid', 'lname': 'Oulad Elhajj', 'email': 'fauconsauvage.1987@gmail.com'},
    {'fname': 'Nadia', 'lname': 'Asserdoun', 'email': 'asserdounadia.tech@gmail.com'},
    {'fname': 'M. Amine', 'lname': 'Boulaadoul', 'email': 'boulaadoulmedamine@laperlenoire.ma'},
]


DCE_CLEANING_DAY = 7        # 1 to 28 (just to be sure)
CLEAN_DCE_AFTER_DAYS = 30
CLEAN_CONS_AFTER_DAYS = 10*400

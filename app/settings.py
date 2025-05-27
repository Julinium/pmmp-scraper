import os, argparse, json
from dotenv import load_dotenv
from pathlib import Path


# Load the .env file from parent directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


# More verbose output
DEBUG_MODE = True 

# Instead of scraping the target website for items links, use those previously saved in imports/links.csv
IMPORT_LINKS = True

# Check existing items against portal for changes.
REFRESH_EXISTING = False

# Skip downloading DCE files.
SKIP_DCE = True


# Initialize parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--level', type=str, required=False, help='debug for more verbose output.')
parser.add_argument('--links', type=str, required=False, help='import to use already saved links.')
parser.add_argument('--found', type=str, required=False, help='refresh to refresh existing items.')
parser.add_argument('--dce', type=str, required=False, help='DCE files download.')


# Parse arguments
args = parser.parse_args()
if args.level: DEBUG_MODE = args.level.lower() == 'debug'
if args.links: IMPORT_LINKS = args.links.lower() == "import"
if args.found: REFRESH_EXISTING = args.found.lower() == "refresh"
if args.dce: SKIP_DCE = args.dce.lower() != "download"


# Use Chromium without GUI. Set to True if running on a non-GUI system
HEADLESS_MODE = True

# Number of pages to get links from: 0 = all.
ONLY_N_PAGES = 2

# Target website. Held for privacy
SITE_ROOT = os.getenv("SITE_ROOT")
SITE_INDEX = os.getenv("SITE_INDEX")
LINK_PREFIX = os.getenv("LINK_PREFIX")
LINK_STITCH = os.getenv("LINK_STITCH")

# Database credentials. Held for security
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Directories to save media files and logs
MEDIA_ROOT = os.getenv("MEDIA_ROOT")
SELENO_LOGS_DIR = os.getenv("SELENO_LOGS_DIR")
SELENO_DIR = os.getenv("SELENO_DIR")

# User agents and user credentials to use randomly to avoid blacklisting
# Example: USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', ...]
# DCE_CREDS = [{'fname': 'john', 'lname': 'Doe', 'email': 'johndoe@fakemail.com'}, ...]
ua_json = Path(__file__).resolve().parent.parent / '.env.ua.json'
with open(ua_json) as f:
    USER_AGENTS = json.load(f)
creds_json = Path(__file__).resolve().parent.parent / '.env.creds.json'
with open(ua_json) as g:
    DCE_CREDS = json.load(g)


LINES_PER_PAGE = "500"
PORTAL_DDL_PAST_DAYS = 1 
PORTAL_DDL_FUTURE_DAYS = 365 * 5
PORTAL_PUB_PAST_DAYS = 365 * 2
PORTAL_PUB_FUTURE_DAYS = 0

LOADING_TIMEOUT = 1000 * 91
REQ_TIMEOUT = 90
DLD_TIMEOUT = 600

LOG_TIME_FORMAT = '%d/%m-%H:%M:%S'

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

DL_PATH_PREFIX = 'DCE-'

DCE_CLEANING_DAY = 7        # 1 to 28 (just to be sure)
CLEAN_DCE_AFTER_DAYS = 30
CLEAN_CONS_AFTER_DAYS = 10*400

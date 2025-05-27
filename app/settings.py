import os, argparse
from dotenv import load_dotenv
from pathlib import Path

# Go up one directory to load the .env file from project/
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


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


SITE_ROOT = os.getenv("SITE_ROOT")
SITE_INDEX = os.getenv("SITE_INDEX")
LINK_PREFIX = os.getenv("LINK_PREFIX")
LINK_STITCH = os.getenv("LINK_STITCH")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("SITE_ROOT")
MEDIA_ROOT = os.getenv("MEDIA_ROOT")
SELENO_LOGS_DIR = os.getenv("SELENO_LOGS_DIR")
SELENO_DIR = os.getenv("SELENO_DIR")
USER_AGENTS = os.getenv("USER_AGENTS")
DCE_CREDS = os.getenv("DCE_CREDS")

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

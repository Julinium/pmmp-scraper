import os, csv, random, time, pytz, zipfile, re, unicodedata
from datetime import datetime, timezone

from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings as C
import helper


def printMessage(level='INFO', raiser='', message='!!! Empty Message !!!'):
    """
    # Synopsis:
    Prints a message to the stdout, tagged with a level and current datetime.
    Messages with level=DEBUG are printed only if C.DEBUG_MODE is true.

    # Params:
        # level:    Level of the message.
        # message:  Text to print.

    # Return: nothing
    """

    if C.DEBUG_MODE or level != 'DEBUG':
        print(f'[{datetime.now(timezone.utc).strftime(C.LOG_TIME_FORMAT)}][{level}][{raiser}] {message}')


def money2Float(texte):
    """
    # Synopsis:
    Converts a string (supposedly) containing an amount of money to a float number.

    # Params:
        # texte: The text containing the amount of money.
    
    # Return:
        -1 if something went wrong, 0 or a float otherwise.
    """

    if texte.strip() == '' or texte == '-':
        return 0
    if texte.find('--') != -1:
        return 0
    try:
        f = texte.replace(" ", "")
        f = f.replace("DH", "")
        f = f.replace("MAD", "")
        f = f.replace('TTC', '')
        if '/' in f:
            f = f.split('/')[0]
        if '.' in f and ',' in f:
            if f.find(',') > f.find('.'):
                f = f.replace(".", "")
        f = f.replace(",", ".")
        f = f.replace('\u202f', '')
        return float(f)
    except Exception as x:
        printMessage('ERROR', 'helper.money2Float', f'Something went wrong while converting string ({texte}) to float. Amount is set to 0')
        printMessage('ERROR', 'helper.money2Float', str(x))
        return -1


def text2Alphanum(text, allCapps=True, dash='-', minLen=8, firstAlpha='M', fillerChar='0'):
    # Normalize unicode to closest ASCII
    normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()

    # Replace anything that's not A-Z, a-z, or 0-9 with a dash
    cleaned = re.sub(r'[^A-Za-z0-9]', '-', normalized)

    # Collapse multiple dashes into one
    cleaned = re.sub(r'-+', '-', cleaned)

    # Remove leading/trailing dashes
    cleaned = cleaned.strip('-')

    # Uppercase everything
    cleaned = cleaned.upper()

    # Ensure at least minLen characters, padding with 'fillerChar' if necessary
    if len(cleaned) < minLen:
        cleaned = cleaned.ljust(minLen, fillerChar)

    # Ensure the first character is [A-Z]
    if not cleaned[0].isalpha():
        cleaned = firstAlpha + cleaned[1:]

    return cleaned


def getDateTime(datetime_str):
    """
    # Synopsis:
    Extracts a datetime object from a string.

    # Params:
        # datetime_str: The string containing the datetime.
        Accepted formats: '19/09/2031 13:55' or '19/09/2031'

    # Return: None or a datetime object. Time may be set to 00:00 if not present.

    """

    if len(datetime_str) == 16:
        return datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')
    if len(datetime_str) == 10:
        return datetime.strptime(datetime_str, '%d/%m/%Y')
    return None


def reading2LocalTime(reading, zonens="Africa/Casablanca"):
    if reading == None: return datetime.now()
    naive_datetime = getDateTime(reading) if reading != None else None
    local_tz = pytz.timezone(zonens)
    localized_datetime = local_tz.localize(naive_datetime)
    return localized_datetime.astimezone(pytz.UTC)


def get_total_folder_size(folder_path):
    total_size_bytes = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                if os.path.isfile(file_path):
                    total_size_bytes += os.path.getsize(file_path)
            except (OSError, PermissionError):
                pass  # Skip files that can't be accessed

    return total_size_bytes


def parseSize(size_str):
    mille = 1024
    # Replace comma with dot for decimal conversion
    size_str = size_str.replace(',', '.').strip()
    
    # Separate the number and unit
    parts = size_str.split()
    if len(parts) != 2: raise ValueError(f"Invalid format: {size_str}")
    
    number, unit = parts
    number = float(number)
    
    # Convert to bytes
    if unit.upper() == 'K':
        return int(number * mille)
    elif unit.upper() == 'M':
        return int(number * mille * mille)
    else:
        raise ValueError(f"Unknown unit: {unit}")


def getDriver(url=''):
    """
    # Synopsis:
        Opens a web browser page, goes to the portal website and submits search form.
    # Params:
        url: The address to retrieve before returning. 
    # Return:
        None or the opened browser page. That is an instance of webdriver.
    """
    helper.printMessage('DEBUG', 'helper.getDriver',
                        'Setting options for Chromium browser ...')
    options = webdriver.ChromeOptions()
    helper.printMessage('DEBUG', 'helper.getDriver',
                        f'\tSetting headless mode to {C.HEADLESS_MODE}')
    if C.HEADLESS_MODE:
        options.add_argument('--headless')
    options.timeouts = {'pageLoad': C.LOADING_TIMEOUT, 'implicit': 60000}
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--remote-debugging-port=9222")  # Added this line for TinyKVM instance
    helper.printMessage('DEBUG', 'helper.getDriver',
                        'Launching instance of Chromium browser ...')
    driver = webdriver.Chrome(options=options)
    if not C.HEADLESS_MODE:
        driver.maximize_window()
    if url == '' or url == None:
        return driver
    helper.printMessage('DEBUG', 'helper.getDriver',
                        f'Going to web address: {url}')
    driver.get(url)
    helper.printMessage('DEBUG', 'helper.getDriver',
                        'Chromium driver instance is setup and ready.')
    return driver


def getEngine_Local():
    """
    # Synopsis:
        Connects to local database engine.
    # Params:
        None.
    # Return:
        Engine: Instance of SQLAlchemy databse engine, which can receive connexions.
    """
    engine = None
    try:
        printMessage('DEBUG', 'helper.getEngine_Local', f'Connecting to loacl database engine {C.DB_NAME}... ')
        engine = create_engine(f'postgresql://{C.DB_USER}:{C.DB_PASS}@{C.DB_SERVER}:{C.DB_PORT}/{C.DB_NAME}')
        printMessage('INFO', 'helper.getEngine_Local', f'=== Connected to local database {C.DB_NAME}\n\n')
    except Exception as x:
        printMessage('ERROR', 'getEngine_Local', f'Exception while connecting to local database engine: {str(x)}\n\n')
    return engine


def getSession(engine=None):
    """
    # Synopsis:
        Opens a database session on a database engine.
    # Params:
        engine: Database engine to use for connexion. Created by function getEngine_Local()
    # Return:
        Session: an instance of a database session on the given engine.
    """
    if engine == None: engine = getEngine_Local()
    session = None
    try:
        printMessage('DEBUG', 'helper.getSession', 'Opening a session on database engine ... ')
        Session = sessionmaker(bind=engine)
        session = Session()
        printMessage('INFO', 'helper.getSession', '=== Opened a session on database engine.')
    except Exception as x:
        printMessage('ERROR', 'getSession', f'Exception while opening a session on database engine: {str(x)}')
    return session


def importLinks(file=f'{C.SELENO_DIR}/exports/links.csv'):
    """
    # Synopsis:
        Imports a list of links from csv file.
    # Params:
        file: The file containing the links. 
    # Return:
        Links: List of the links contained in the file.
    """
    links = []
    try:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                links.append(row)
    except Exception as x:
        printMessage('ERROR', 'helper.importLinks', f'Exception while importing file: {str(x)}')
    return links


def printBanner():
    print("""
    #############################################################
    #############################################################
    ##                                                         ##
    ##   ##     ##   ####   ####    #####  ##### ##### #####   ##
    ##   ###   ###  ##  ##  ##  ##  ##        ##    ##    ##   ##
    ##   ## ### ##  ##  ##  ##  ##  ####     ##    ##    ##    ##
    ##   ##  #  ##  ##  ##  ##  ##  ##      ##    ##    ##     ##
    ##   ##     ##   ####   ####    #####   ##    ##    ##     ##
    ##                                                         ##
    ########################  (C)2024-2025 - WWW.MODE-777.COM  ##
    #############################################################
    """)


def getDcePath(link_item):
    """
    # Synopsys:
        Construct a canonical path for a given Consultation. No files or folders are created.
    # Params:
        - link_item: An item representing a Consultation instance. It's a list of 3 values : [ID, ORG, PUB_DATE]
    # Reurn:
        String representing the full path of the directory for the Consultation.
    """
    return os.path.join(C.MEDIA_ROOT, f'dce/{C.DL_PATH_PREFIX}{link_item[0]}')


def getUa():
    rua = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    if len(C.USER_AGENTS) > 0 : rua = C.USER_AGENTS[random.randint(0, len(C.USER_AGENTS)-1)]
    return rua


def sleepRandom(Fm=15, To=45):
    rint = random.randint(Fm, To)
    helper.printMessage('DEBUG', 'helper.sleepRandom', f'ZZZZZZZZZZZZZZZZZZZZZZZZZZZ. Sleeping for a ({rint}s) while.\n\n')
    time.sleep(rint)
    return 0


def cleanEmptyDceFiles(dry_run=True, base_folder=''):
    if base_folder == '': base_folder = f'{C.MEDIA_ROOT}/dce'

    nf, nd = 0, 0
    helper.printMessage('INFO', 'helper.cleanEmptyDceFiles', f"Deleting empty files from: {base_folder}")
    # Iterate through all items in the base folder
    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        # Check if the item is a subfolder and matches the pattern "DCE-{id}"
        if os.path.isdir(subfolder_path) and subfolder.startswith("DCE-"):
            nd += 1
            # helper.printMessage('DEBUG', 'helper.cleanEmptyDceFiles', f"Browsing folder: {subfolder_path}")

            # Iterate through files in the subfolder
            for file_name in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file_name)

                # Check if the item is a file and its size is 0 bytes
                if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                    # print(f"Deleting empty file: {file_path}")
                    if dry_run: 
                        helper.printMessage('DEBUG', 'helper.cleanEmptyDceFiles', f"DRY-RUN = empty file: {file_path}")
                    else:   
                        helper.printMessage('DEBUG', 'helper.cleanEmptyDceFiles', f"Deleting empty file: {file_path}")
                        os.remove(file_path)
                    nf += 1
    helper.printMessage('INFO', 'helper.cleanEmptyDceFiles', f"Subfolders scanned: {nd}, Files affected: {nf}")


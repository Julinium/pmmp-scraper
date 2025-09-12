import os, random, re, requests
from bs4 import BeautifulSoup
from slugify import slugify

import helper
import settings as C
from dbaser import getCurrentCons


FILE_PREFIX =  'eMarches.com-' # '[eMarches.com]_'
SLEEP_4XX_MIN = 377
SLEEP_4XX_MAX = 777

def getDCE(link_item):
    if not os.path.exists(C.MEDIA_ROOT): 
        helper.printMessage('ERROR', 'dnlder.getDCE', f'Could not read media directory {C.MEDIA_ROOT}.')
        return 1
    if not link_item : 
        helper.printMessage('ERROR', 'dnlder.getDCE', f'Incorrect parameter was received.')
        return 1

    con_path = os.path.join(C.MEDIA_ROOT, f'dce/{C.DL_PATH_PREFIX}{link_item[0]}')
    if not os.path.exists(con_path): os.makedirs(con_path)
    if not os.path.exists(con_path):
        helper.printMessage('ERROR', 'dnlder.getDCE', f'Could not find DCE directory {con_path}.')
        return 1


    def make_link(link_item, type=None):
        # f'{C.SITE_INDEX}?page=entreprise.EntrepriseDownloadReglement&reference=ODkxNjE4&orgAcronyme={link_item[1]}'
        # f'{C.SITE_INDEX}?page=entreprise.EntrepriseDownloadCompleteDce&reference={link_item[0]}&orgAcronym={link_item[1]}'
        # f'{C.SITE_INDEX}?page=entreprise.EntrepriseDemandeTelechargementDce&refConsultation={link_item[0]}&orgAcronyme={link_item[1]}'
        if type == 'query': return f'{C.SITE_INDEX}?page=entreprise.EntrepriseDemandeTelechargementDce&refConsultation={link_item[0]}&orgAcronyme={link_item[1]}'
        if type == 'file': return f'{C.SITE_INDEX}?page=entreprise.EntrepriseDownloadCompleteDce&reference={link_item[0]}&orgAcronym={link_item[1]}'
        return f'{C.SITE_INDEX}?page=entreprise.EntrepriseDetailsConsultation&refConsultation={link_item[0]}&orgAcronyme={link_item[1]}'

    def get_filename(cd):
        if not cd: return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0: return None
        return fname[0]


    if len(C.USER_AGENTS) == 0 : 
        DEFAULT_UA = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        helper.printMessage('DEBUG', 'dnlder.getDCE', f'UA list was empty. Using default: {DEFAULT_UA}.')
        headino = {"User-Agent": DEFAULT_UA}
    else :
        rua = C.USER_AGENTS[random.randint(0, len(C.USER_AGENTS)-1)]
        rua_label = "Random"
        try:
            start_delimiter = "Mozilla/5.0 ("
            end_delimiter = "; "
            start_index = rua.index(start_delimiter) + len(start_delimiter)
            end_index = rua.index(end_delimiter, start_index)
            rua_label = rua[start_index:end_index]
        except ValueError as ve:
            helper.printMessage('ERROR', 'dnlder.getDCE', f'Error trimming UA: {str(ve)}')

        helper.printMessage('DEBUG', 'dnlder.getDCE', f'Using random UA: {rua_label}.')
        headino = {"User-Agent":  rua}

    sessiono = requests.Session()

    url_query = make_link(link_item, 'query')
    url_form = url_query
    url_file = make_link(link_item, 'file')
    
    helper.printMessage('DEBUG', 'dnlder.getDCE', f'Cons link : {url_query.replace(C.SITE_INDEX, '')}')
    helper.printMessage('DEBUG', 'dnlder.getDCE', f'Form link : {url_form.replace(C.SITE_INDEX, '')}')
    helper.printMessage('DEBUG', 'dnlder.getDCE', f'File link : {url_file.replace(C.SITE_INDEX,'')}')

    try: request_query = sessiono.get(url_query, headers=headino, timeout=C.REQ_TIMEOUT)
    except Exception as xc: 
        helper.printMessage('ERROR', 'dnlder.getDCE', str(xc))
        return 1

    soup = BeautifulSoup(request_query.content, 'html.parser')
    
    if request_query.status_code != 200 : 
        helper.printMessage('ERROR', 'objeer.getDCE', f'Download query: Response Status Code: {request_file.status_code} !')
        helper.printMessage('ERROR', 'objeer.getDCE', f'\n\n\n===========\n{soup}\n===========\n\n')
        
        helper.sleepRandom(SLEEP_4XX_MIN, SLEEP_4XX_MAX)
        return request_query.status_code
    else:
        helper.printMessage('DEBUG', 'dnlder.getDCE', f'Download query: Successful.')

    prado_page_state = None
    try: prado_page_state = soup.find(id="PRADO_PAGESTATE")['value']
    except: pass

    prado_pbk_target = None
    try: prado_pbk_target = soup.find(id="PRADO_POSTBACK_TARGET")['value']
    except: pass

    prado_pbk_parame = None
    try: prado_pbk_parame = soup.find(id="PRADO_POSTBACK_PARAMETER")['value']
    except: pass

    datano = {
        'ctl0$menuGaucheEntreprise$quickSearch': 'Recherche rapide',
        'ctl0$CONTENU_PAGE$ctl5$idReferentielZoneText$RepeaterReferentielZoneText$ctl0$modeRecherche': '1',
        'ctl0$CONTENU_PAGE$ctl5$idReferentielZoneText$RepeaterReferentielZoneText$ctl0$typeData': 'montant',
        'ctl0$CONTENU_PAGE$ctl5$idRefRadio$RepeaterReferentielRadio$ctl0$ClientIdsRadio': 'ctl0_CONTENU_PAGE_ctl5_idRefRadio_RepeaterReferentielRadio_ctl0_OptionOui#ctl0_CONTENU_PAGE_ctl5_idRefRadio_RepeaterReferentielRadio_ctl0_OptionNon',
        'ctl0$CONTENU_PAGE$ctl5$idRefRadio$RepeaterReferentielRadio$ctl0$modeRecherche': '1',
        'ctl0$CONTENU_PAGE$ctl5$idAtexoRefDomaineActivites$defineCodePrincipal': '(Code principal)',
        'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$RadioGroup': 'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$choixTelechargement',
        'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$accepterConditions': 'on',
        'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$clientId': 'ctl0_CONTENU_PAGE_EntrepriseFormulaireDemande', 
        'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$etablissementEntreprise': 'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$france',
        'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$pays': '0',
    }

    creds = {'fname': 'Hamid', 'lname': 'ZAHIRI', 'email': 'h.zahir.pro@menara.ma'}
    if len(C.DCE_CREDS) > 0:
        creds = C.DCE_CREDS[random.randint(0, len(C.DCE_CREDS)-1)]
        helper.printMessage('DEBUG', 'dnlder.getDCE', f'Using Credentials for: {creds.get("fname")} {creds.get("lname")}.')
    else: helper.printMessage('DEBUG', 'dnlder.getDCE', f'Using Credentials for: {creds.get("fname")} {creds.get("lname")}.')

    datano['ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$prenom'] = creds.get('fname', 'Mourad')
    datano['ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$nom'] = creds.get('lname', 'Mountassir')
    datano['ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$email'] = creds.get('email', 'mmountassirsky@caramail.com')

    if prado_page_state: datano['PRADO_PAGESTATE'] = prado_page_state
    if prado_pbk_target: datano['PRADO_POSTBACK_TARGET'] = prado_pbk_target
    if prado_pbk_parame: datano['PRADO_POSTBACK_PARAMETER'] = prado_pbk_parame
    
    try: request_form = sessiono.post(url_form, headers=headino, data=datano, timeout=C.REQ_TIMEOUT)
    except Exception as xc: 
        helper.printMessage('ERROR', 'dnlder.getDCE', 'Exception raised while submitting form.')
        helper.printMessage('ERROR', 'dnlder.getDCE', str(xc)) 
        return 1
    
    if request_form.status_code != 200 :
        helper.printMessage('ERROR', 'objeer.getDCE', f'Form submission: Response Status Code: {request_form.status_code} !')
        helper.sleepRandom(SLEEP_4XX_MIN, SLEEP_4XX_MAX)
        return request_form.status_code
    else: helper.printMessage('DEBUG', 'dnlder.getDCE', f'Form submission: Successful')

    try:
        helper.printMessage('DEBUG', 'dnlder.getDCE', f'Requesting file at : {url_file.replace(C.SITE_INDEX,'')}')
        request_file = sessiono.get(url_file, headers=headino, timeout=C.DLD_TIMEOUT)
    except requests.exceptions.Timeout:
        helper.printMessage('ERROR', 'dnlder.getDCE', "Request timed out! Exception message: " + str(xc))
    except Exception as xc: 
        helper.printMessage('ERROR', 'dnlder.getDCE', str(xc))
        return 1
    
    if request_file.status_code != 200 :
        helper.printMessage('ERROR', 'objeer.getDCE', f'Getting file: Response Status Code: {request_file.status_code} !')
        helper.sleepRandom(SLEEP_4XX_MIN, SLEEP_4XX_MAX)
        return request_file.status_code
    else: helper.printMessage('DEBUG', 'dnlder.getDCE', f'Getting file: Successful')

    try:
        filename_cd = get_filename(request_file.headers.get('content-disposition'))
        filename_cd = filename_cd.lower().replace('zip', '')
        filename_cd = helper.text2Alphanum(filename_cd, allCapps=True, dash='-', minLen=8, firstAlpha='M', fillerChar='0')
    except Exception as xc:
        helper.printMessage('DEBUG', 'dnlder.getDCE', 'Could not get file name from portal.')
        helper.printMessage('DEBUG', 'dnlder.getDCE', str(xc))
        filename_cd = f"CONS-{link_item[0]}"
        # return 1

    filename_base = f'{FILE_PREFIX}-{link_item[0]}-{filename_cd}.zip'
    filename = os.path.join(con_path, filename_base)
    helper.printMessage('DEBUG', 'dnlder.getDCE', f'Writing file content to {filename_base} ... ')


    try:
        with open(filename, 'wb') as file:
            bytes_written = file.write(request_file.content)
            helper.printMessage('DEBUG', 'dnlder.getDCE', f'### Bytes written: {bytes_written}/{len(request_file.content)}.')

        # Verify the file size
        if bytes_written != len(request_file.content): raise IOError("File size mismatch: Not all content was written.")
        if os.path.getsize(filename) == 0: raise IOError("File was created but is empty. Go and know why!")
    except Exception as e:
        helper.printMessage('ERROR', 'dnlder.getDCE', f"Error writing data to file: {e}")
        return 1

    return 0


def getMissingDCE(session):
    rlc = 0
    errors, checked, skipped, corrected, failed = 0, 0, 0, 0, 0
    current_cons = getCurrentCons(session)
    helper.printMessage('INFO', 'dnlder.getMissingDCE', f'Found items to check files for = {len(current_cons)}.')

    if len(current_cons) > 0:

        for con in current_cons:
            checked += 1
            if rlc > 10 :
                helper.sleepRandom()
                rlc = 0
            helper.printMessage('DEBUG', 'dnlder.getMissingDCE', f'Checking DCE for id = {con.portal_id} ... ')
            dce_path = os.path.join(C.MEDIA_ROOT, f'dce/{C.DL_PATH_PREFIX}{con.portal_id}')
            
            dce_files = []
            if os.path.exists(dce_path) :
                helper.printMessage('DEBUG', 'dnlder.getMissingDCE', f'=== DCE folder found for id = {con.portal_id} ... ')
                dce_files = os.listdir(dce_path)
            else:
                helper.printMessage('DEBUG', 'dnlder.getMissingDCE', f'=== No DCE folder was found for id = {con.portal_id} ... ')
            

            if len(dce_files) == 0:
                rlc += 1
                l = (con.portal_id, con.portal_link[:3], con.date_publication)
                if getDCE(l) == 0:
                    corrected += 1
                    helper.printMessage('INFO', 'worker', f'===== DCE download complete successfully for id = {con.portal_id}.\n\n')
                else:
                    failed += 1 
                    helper.printMessage('ERROR', 'worker', f'===== Something went wrong while downloading DCE for id = {con.portal_id}.\n\n')
                
            else: 
                skipped += 1
                helper.printMessage('DEBUG', 'dnlder.getMissingDCE', '===== DCE files are already there. Skipping.\n\n')

        return [errors, checked, skipped, corrected, failed]

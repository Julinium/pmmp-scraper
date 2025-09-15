import os, time, random, shutil
from datetime import datetime

import settings as C
import linker, helper, objeer, dnlder, dbaser, cleaner

started_at = datetime.now()


####################### BRAND #######################
helper.printBanner()
helper.printMessage('INFO', 'worker', f'Application started with arguments: DEBUG={C.DEBUG_MODE} IMPORT={C.IMPORT_LINKS} REFRESH={C.REFRESH_EXISTING}\n\n\n')

####################### LINKS #######################
links = []
if C.IMPORT_LINKS:
    helper.printMessage('INFO', 'worker', '########## 01. Importing links from local file ...')
    links = helper.importLinks()
else:
    helper.printMessage('INFO', 'worker', '########## 01. Getting links from portal website ...')
    links = linker.getLinks()
    helper.printMessage('DEBUG', 'worker', f'===== Got {len(links)} links from portal website ...')
    if len(links) > 0:
        helper.printMessage('INFO', 'worker', '############### 01.01. Exporting links list to local file ...')
        links_file = linker.exportLinks(links)
        if links_file == '': helper.printMessage('ERROR', 'worker', '====== Something went wrong when exporting links.')
        else: helper.printMessage('INFO', 'worker', f'================== Links exported to csv file.')
if len(links) == 0:
    helper.printMessage('ERROR', 'worker', 'Links list was empty. Aborting.')
    exit(1)
helper.printMessage('INFO', 'worker', f'========== Links count : {len(links)}. \n\n')


####################### DBASE & FILES #######################
helper.printMessage('INFO', 'worker', '########## 02. Reading data and saving Records ...')

illacha = 0
links_count = len(links)
helper.printMessage('INFO', 'worker', '##### 02.01. Connecting to database ...')
session = helper.getSession(helper.getEngine_Local())
if session: helper.printMessage('INFO', 'worker', '===== Successfully connected to database.')
else:
    helper.printMessage('ERROR', 'worker', '===== Error connecting to database.')
    exit('XXXXXXXXXX Exiting: Error connecting to database XXXXXXXXXX')


helper.sleepRandom(10, 30)
rlc = 0
count_cons, count_dce = 0, 0
for i, l in enumerate(links, start=1):
    if rlc > 10 :
        helper.sleepRandom()
        rlc = 0

    portal_number = l[0]
    print("\n\n")
    helper.printMessage('INFO', 'worker', f'##### Working on link {i:04}/{links_count}: id = {portal_number} ...')


    consino = dbaser.consExists(session, portal_number)
    dce_path = helper.getDcePath(l)
    
    
    if consino:
        helper.printMessage('DEBUG', 'worker', f'Found item with id = {portal_number}.')
        if C.REFRESH_EXISTING:
            helper.printMessage('DEBUG', 'worker', f'Checking existing item for change, id = {portal_number}.')
            try:
                cons_dict = objeer.getConsObject(l)
                if cons_dict:
                    if dbaser.hasChanged(cons_dict, consino, session) == 1:
                        helper.printMessage('INFO', 'worker', f'Changes detected for id = {portal_number}. To refresh.')
                        if dbaser.deleteCons(portal_number, session) == 0:
                            helper.printMessage('DEBUG', 'worker', f'Successfully deleted related objects for id = {portal_number}.')
                            consino = None
                        helper.printMessage('DEBUG', 'worker', f'Item files needs update. Deleting id = {portal_number} and files ...')
                        folder_path = os.path.join(C.MEDIA_ROOT, f'dce/{C.DL_PATH_PREFIX}{portal_number}')
                        if os.path.exists(folder_path):
                            try:
                                shutil.rmtree(folder_path)
                                helper.printMessage('DEBUG', 'worker', f'Folder successfully removed {C.DL_PATH_PREFIX}{portal_number}.')
                            except Exception as sx:
                                helper.printMessage('ERROR', 'worker', f'{str(sx)}')
                    else: helper.printMessage('INFO', 'worker', f'No changes were detected for id = {portal_number}. Skipping.')
            except Exception as xc:
                helper.printMessage('ERROR', 'worker', f'{str(xc)}')
    

    if consino == None:
        helper.printMessage('DEBUG', 'worker', f'Reading objects for link {i:04}/{links_count}: id = {portal_number} ...')
        try:
            cons_dict = objeer.getConsObject(l)
            rlc += 1
            if cons_dict:
                helper.printMessage('DEBUG', 'worker', 'Successfully read objects for link. Saving to database ... ')
                if dbaser.writeData(cons_dict, session) == 0: 
                    count_cons += 1
                    helper.printMessage('INFO', 'worker', '===== Objects saved successfully for link.')
                else: helper.printMessage('ERROR', 'worker', f'===== Errors occurred while saving objects for link {i:04}/{links_count}: id = {portal_number} ...')
            else:
                illacha += 1
                helper.printMessage('ERROR', 'worker', ' Something went wrong while reading objects.')
        except Exception as xc:
            helper.printMessage('ERROR', 'worker', f'{str(xc)}')
    else:
        helper.printMessage('INFO', 'worker', '===== Object already on database. Skipping link.')

    if C.SKIP_DCE:
        helper.printMessage('DEBUG', 'worker', f'Settings: Skip DCE for item {i:04}/{links_count}, id = {portal_number} ... ')
    else:
        helper.printMessage('DEBUG', 'worker', f'Downloading DCE for item {i:04}/{links_count}: id = {portal_number} ... ')
        dce_files = []
        if os.path.exists(dce_path) : dce_files = os.listdir(dce_path)

        if len(dce_files) == 0:
            try:
                rlc += 1
                downloaded = dnlder.getDCE(l, session)
                if downloaded == 0:
                    # consino.size_bytes = downloaded
                    count_dce += 1
                    helper.printMessage('INFO', 'worker', f'===== DCE download complete successfully for item {i:04}/{links_count}: id = {portal_number}.')
                else: helper.printMessage('ERROR', 'worker', f'===== Something went wrong while downloading DCE for item {i:04}/{links_count}: id = {portal_number}.')
            except Exception as xc: helper.printMessage('ERROR', 'worker', f'{str(xc)}')
        else: helper.printMessage('INFO', 'worker', '===== DCE files are already there. Skipping.')


if illacha == 0:
    print("\n\n\n")
    helper.printMessage('INFO', 'worker', '========== Successfully saved objects.')
    dbaser.updateUpdateTime(session)
else:
    helper.printMessage('ERROR', 'worker', '========== Something went wrong while saving objects to database.')


######################## MISSING FILES ########################
print("\n\n\n")
if C.SKIP_DCE:
    helper.printMessage('INFO', 'worker', 'Settings: Skip missing DCE files...')
else:
    helper.printMessage('INFO', 'worker', 'Getting missing DCE files...')
    cor = dnlder.getMissingDCE(session)
    count_dce += cor[3]
    # if cor[0] != 0: helper.printMessage('ERROR', 'worker', '========== Something went wrong when getting missing DCE.')
    helper.printMessage('INFO', 'worker', f'=== Missing files: Checked={cor[0]}, Skipped={cor[1]}, Corrected={cor[2]}, Failed={cor[3]}.\n')


# TODO: What about an item with more than one file ?


######################## HOUSEKEEPING ########################
# Once a month, delete the DCE files for Items expired more than CLEAN_DCE_AFTER_DAYS days ago (default=60):
dce_cleaner_started = False
dce_cleaned = 0
if started_at.day == C.DCE_CLEANING_DAY:
    dce_cleaner_started = True
    try: dce_cleaned = cleaner.removeOldDce(session)
    except Exception as x: helper.printMessage('ERROR', 'worker', str(x))
    print('\n\n')

# TODO: Other cleaning ...
# Searches - 


######################## CLOSE DB ########################
if session != None: 
    helper.printMessage('DEBUG', 'worker', 'Disconnecting from database ...\n')
    session.close()

######################## SOME STATS ########################
finished_at = datetime.now()
duration = finished_at - started_at
total_seconds = int(duration.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"

helper.printMessage('INFO', 'worker', f'##### Consultations created ##### : {count_cons:06}.')
helper.printMessage('INFO', 'worker', f'##### DCE files downloaded  ##### : {count_dce:06}.')
if dce_cleaner_started : helper.printMessage('INFO', 'worker', f'##### DCE folders deleted   ##### : {dce_cleaned:06}.')
helper.printMessage('INFO', 'worker', f'##### Operation finished in ##### : {formatted_duration}.\n\n')


import os, shutil
from datetime import datetime as dt
from datetime import timedelta as td


import settings as C
import helper
from dbaser import getObsoleteDce

age = C.CLEAN_DCE_AFTER_DAYS
if not age: age = 60
dry_run = False

def removeOldDce(session, dry_run=dry_run):
    helper.printMessage('INFO', 'cleaner.removeOldDce', f'Removing files for obsolete items ({age} days or more) items...')
    if dry_run : helper.printMessage('INFO', 'cleaner.removeOldDce', '---------=== DRY RUN ===---------')
    cons = getObsoleteDce(session, age)
    cl = len(cons)
    helper.printMessage('INFO', 'cleaner.removeOldDce', f'=== Found obsolete items: {cl}\n\n')
    if cl == 0 : return 0
    
    dl, el, sl, i = 0, 0, 0, 0

    for c in cons:
        i = i + 1
        folder_name = f'dce/{C.DL_PATH_PREFIX}{c.portal_id}'
        dce_directory_path = os.path.join(C.MEDIA_ROOT, folder_name)
        helper.printMessage('DEBUG', 'cleaner.removeOldDce', f'--- Examining element {i:05}/{cl:05}: id = {c.portal_id}')
        if os.path.isdir(dce_directory_path):
            if not dry_run :
                try:
                    shutil.rmtree(dce_directory_path)
                    dl += 1
                    helper.printMessage('DEBUG', 'cleaner.removeOldDce', f'--- Successfully removed: {folder_name}')
                except FileNotFoundError:
                    helper.printMessage('DEBUG', 'cleaner.removeOldDce', f'--- Directory not find: {folder_name}')
                    el += 1
                except PermissionError:
                    helper.printMessage('ERROR', 'cleaner.removeOldDce', f'--- Permission denied for: {folder_name}')
                    el += 1
                except OSError as e:
                    helper.printMessage('ERROR', 'cleaner.removeOldDce', f'--- OS error occurred for: {folder_name}')
                    helper.printMessage('ERROR', 'cleaner.removeOldDce', f'--- OS error details: {e}')
                    el += 1
            else:
                helper.printMessage('DEBUG', 'cleaner.removeOldDce', f'--- DRY-RUN removed: {folder_name}')
        else:
            helper.printMessage('DEBUG', 'cleaner.removeOldDce', f'### Path may not be a valid directory: {folder_name}')
            sl += 1
    print("\n\n")
    helper.printMessage('INFO', 'cleaner.removeOldDce', f'### Obsolete items: Deleted={dl}, Skipped={sl}, Failures={el}')
    if el > 0 : helper.printMessage('ERROR', 'cleaner.removeOldDce', f'###### Removing files for obsolete items was not successful!')
    return dl

# TODO: Delete orphan Downloads, Favs, ... 

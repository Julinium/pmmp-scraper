import os, csv, random, json
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import settings as C
import helper


def fillSearchForm(driver, back_days=C.PORTAL_DDL_PAST_DAYS):
    assa = date.today()
    # dt_pub_start = assa - timedelta(days=C.PORTAL_PUB_PAST_DAYS)
    # dt_pub_end   = assa + timedelta(days=C.PORTAL_PUB_FUTURE_DAYS)
    dt_ddl_start = assa - timedelta(days=back_days)
    # dt_ddl_end   = assa + timedelta(days=C.PORTAL_DDL_FUTURE_DAYS)

    # date_pub_start = dt_pub_start.strftime("%d/%m/%Y")
    # date_pub_end   = dt_pub_end.strftime("%d/%m/%Y")
    date_ddl_start = dt_ddl_start.strftime("%d/%m/%Y")
    # date_ddl_end   = dt_ddl_end.strftime("%d/%m/%Y")

    helper.printMessage('DEBUG', 'linker.fillSearchForm', 'Submitting search form with default dates and empty terms ...')
    try:
        el_ddl_start = driver.find_element("id", "ctl0_CONTENU_PAGE_AdvancedSearch_dateMiseEnLigneStart")
        el_ddl_start.clear()
        el_ddl_start.send_keys(date_ddl_start)
        
    except Exception as xc: 
        helper.printMessage('ERROR', 'linker.fillSearchForm', 'Could not find date field:')
        helper.printMessage('ERROR', 'linker.fillSearchForm', str(xc))
        

def page2Links(driver, page_number):
    """
    # Synopsis:
        Get a list of available Consultations from a given page.
    # Params:
        driver: An instance of Chrome Webdriver object. That is a web browser window.
        page_number : Page number to scrape.
    # Return:
        List of extremely abbriged Consultations visible on the page.
        Each element represents [portal id, organism acronym, published date] of a Consultation.
        The first two values can be used to obtain a working link to the Consultaion on the portal.
    """
    links = []    # lict = {}
    try:
        i = 1
        details_btn_xpath = '/html/body/form/div[3]/div[2]/div/div[5]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[6]/div/a[1]'
        details_btn = driver.find_element(By.XPATH, details_btn_xpath)
        while details_btn != None:
            pub_date_xpath = details_btn_xpath.replace('td[6]/div/a[1]', 'td[2]/div[4]')
            pub_date_element = driver.find_element(By.XPATH, pub_date_xpath)
            drat = details_btn.get_attribute("href").replace(C.LINK_PREFIX, '') #### 825152&orgAcronyme=q9t
            portal_id_text = drat.split(C.LINK_STITCH)[0]
            organism_text = drat.split(C.LINK_STITCH)[1]
            helper.printMessage('DEBUG', 'linker.page2Links', f'### Getting link {i:03} from page {page_number:03}: id={portal_id_text}')
            links.append([portal_id_text, organism_text, pub_date_element.get_attribute("innerText")])
            i = 1 + i
            details_btn_xpath = '/html/body/form/div[3]/div[2]/div/div[5]/div[1]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[6]/div/a[1]'
            try: details_btn = driver.find_element(By.XPATH, details_btn_xpath)
            except: details_btn = None
    except Exception as exc:
        helper.printMessage('ERROR', 'linker.page2Links', f'Exception while getting data: {str(exc)}')
    return links


def exportLinks(links):
    """
    # Synopsis:
        Exports links to a csv file. File is placed under {SELENO_DIR/exports} and named links.csv.
    # Params:
        links: List of links to export.
    # Return:
        full path to the exported csv file.
    """
    
    file = ''
    if len(links) > 0 :
        try:
            expo_dir = f'{C.SELENO_DIR}/exports'
            if not os.path.exists(expo_dir) : os.mkdir(expo_dir)
            file = f'{expo_dir}/links.csv'
            with open(file, 'w', newline='') as linkscsv:
                linkwriter = csv.writer(linkscsv)
                for l in links:
                    linkwriter.writerow(l)
        except Exception as e :
            helper.printMessage('ERROR', 'linker.exportLinks', f'Something went wrong while exporting links: {str(e)}')
            return ''
    return file


def getLinks(back_days=C.PORTAL_DDL_PAST_DAYS):
    """
    # Synopsis:
        Get a list of available Consultations on Portal.
    # Params:
        None.
    # Return:
        List of extremely abbriged Consultations.
        Each element represents [portal id, organism acronym, published date] of a Consultation.
        The first two values can be used to obtain a working link to the Consultaion on the portal.
    """
    url = "https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&searchAnnCons"
    driver = helper.getDriver(url)
    
    links = []
    pages = 0
    count = 0
    if driver == None: return links
    
    fillSearchForm(driver, back_days)
    
    try:
        helper.printMessage('DEBUG', 'linker.getLinks', 'Submitting search form with default dates and empty terms ...')
        org_search_field = driver.find_element("id", "ctl0_CONTENU_PAGE_AdvancedSearch_orgName")
        org_search_field.send_keys(Keys.ENTER)
    except Exception as e :
        helper.printMessage('ERROR', 'linker.getLinks', f'Something went wrong while submitting search form: {str(e)}')
        if driver: driver.quit()
        return links
    try:
        helper.printMessage('DEBUG', 'linker.getLinks', 'Finding page size element ...')
        page_size = Select(driver.find_element("id", "ctl0_CONTENU_PAGE_resultSearch_listePageSizeTop"))
        helper.printMessage('DEBUG', 'linker.getLinks', f'Selecting page size { C.LINES_PER_PAGE }')
        page_size.select_by_visible_text(C.LINES_PER_PAGE)
    except Exception as e :
        helper.printMessage('ERROR', 'linker.getLinks', f'Something went wrong while changing page size: {str(e)}')
        if driver: driver.quit()
        return links
    
    try:
        helper.printMessage('DEBUG', 'linker.getLinks', 'Reading page count and number of results ...')
        pages_field = driver.find_element("id", "ctl0_CONTENU_PAGE_resultSearch_nombrePageTop")
        pages = int(pages_field.get_attribute("innerText").strip())
        count_field = driver.find_element("id", "ctl0_CONTENU_PAGE_resultSearch_nombreElement")
        count = count_field.get_attribute("innerText").strip()
        helper.printMessage('INFO', 'linker.getLinks', f'Number of items: {count:04}. Number of pages: {pages:03}')
    except Exception as e :
        helper.printMessage('ERROR', 'linker.getLinks', f'Something went wrong while getting links and pages counts: {str(e)}')
        if driver: driver.quit()
        return links

    i = 1
    helper.printMessage('INFO', 'linker.getLinks', f'Reading links from page {i:03}/{pages:03} ... ')
    links = page2Links(driver, i)
    try: next_page_button = driver.find_element(By.ID, "ctl0_CONTENU_PAGE_resultSearch_PagerTop_ctl2")
    except: next_page_button = None
    while next_page_button != None:
        next_page_button.click()
        i += 1
        helper.printMessage('INFO', 'linker.getLinks', f'Reading links from page {i:03}/{pages:03} ... ')
        links += page2Links(driver, i)
        try : next_page_button = driver.find_element(By.ID, "ctl0_CONTENU_PAGE_resultSearch_PagerTop_ctl2")
        except: next_page_button = None
    if driver: driver.quit()
    
    if len(links) != int(count):
        helper.printMessage('ERROR', 'linker.getLinks', f'Discrepancy between links count {len(links):04} and items number {count:04}. Links list was emptied: ')
        links = []
    
    return links


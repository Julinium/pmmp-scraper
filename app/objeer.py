import re, random, time
# from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup, Comment, Tag

import helper
import settings as C


def getLotsObject(lots_href):
    helper.printMessage('DEBUG', 'objeer.getJson', 'Item is multi-lot. Reading lots ... ')
    lots_link = C.SITE_INDEX + lots_href.replace("javascript:popUp('index.php", "").replace("%27,%27yes%27)", "")

    rua = helper.getUa()
    helper.printMessage('DEBUG', 'objeer.getObject', f'Using UA: {rua}.')
    headino = {"User-Agent": rua }

    sessiono = requests.Session()

    try: request_lots = sessiono.get(lots_link, headers=headino, timeout=C.REQ_TIMEOUT)  # driver.get(lots_link)
    except Exception as x:
        helper.printMessage('ERROR', 'objeer.getObject', f'Exception raised while getting lots at {str(lots_link)}: {str(x)}')
        return None
    helper.printMessage('DEBUG', 'objeer.getObject', f'Getting Lots page : {request_lots}')
    if request_lots.status_code != 200 :
        helper.printMessage('ERROR', 'objeer.getObject', f'Request to Lots page returned a {request_lots.status_code} status code.')
        if request_lots.status_code == 429:
            helper.printMessage('ERROR', 'objeer.getObject', f'Too many Requests, said the server: {request_lots.status_code} !')
            helper.sleepRandom(300, 600)
        return None

    bowl = BeautifulSoup(request_lots.text, 'html.parser')

    soup = bowl.find(class_='content')

    lots = []

    def iscomment(elem):
        return isinstance(elem, Comment)
    separator = soup.find('div', class_='separator')
    comments = soup.find_all(string=iscomment)
    i = 0
    for comment in comments:
        if "Debut Lot 1" in comment :
            current_lot = {}

            # Number
            number_elem = comment.find_next_sibling("div", class_="intitule-bloc intitule-150")
            number_span = number_elem.find(class_='blue bold')
            number = number_span.get_text().strip('Lot').strip(':').strip() if number_span else ""

            # Title
            title_elem = number_elem.find_next_sibling("div", class_="content-bloc bloc-600")
            title = title_elem.get_text().strip() if title_elem else ""

            # Category
            category_elem = title_elem.find_next_sibling("div", class_="content-bloc bloc-600")
            category = category_elem.get_text().strip() if category_elem else ""

            # Extract Description
            description_elem = category_elem.find_next_sibling("div", class_="content-bloc bloc-600")
            description = description_elem.get_text().strip() if description_elem else ""

            # Estimation
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idReferentielZoneTextLot_RepeaterReferentielZoneText_ctl0_panelReferentielZoneText'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idReferentielZoneTextLot_RepeaterReferentielZoneText_ctl0_labelReferentielZoneText'
            estimation_div  = description_elem.find_next_sibling("div", id=div_id)
            estimation_span = estimation_div.find('span', id=span_id)
            estimation = estimation_span.get_text().strip() if estimation_span else ""

            # Caution Provisoire
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelCautionProvisoire'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_cautionProvisoire'
            caution_div  = estimation_div.find_next_sibling("div", id=div_id)
            caution_span = caution_div.find('span', id=span_id)
            caution = caution_span.get_text().strip() if caution_span else ""


            # Qualifications
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelQualification'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_qualification'
            qualifs_div  = caution_div.find_next_sibling("div", id=div_id)
            qualifs_span = qualifs_div.find('span', id=span_id)
            qualifs_lis = qualifs_span.find_all('li')
            qualifs = []
            for qualifs_li in qualifs_lis :
                qualif = qualifs_li.get_text().strip() if qualifs_li else ""
                if qualif != '' : qualifs.append(qualif)

            # Agrements
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelAgrements'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_agrements'
            agrements_div  = qualifs_div.find_next_sibling("div", id=div_id)
            agrements_span = agrements_div.find('span', id=span_id)
            agrements_lis = agrements_span.find_all('li')
            agrements = []
            for agrements_li in agrements_lis :
                agrement = agrements_li.get_text().strip() if agrements_li else ""
                if agrement != '' : agrements.append(agrement)

            # Samples
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelEchantillons'
            samples_div  = agrements_div.find_next_sibling("div", id=div_id)
            samples_lis = samples_div.find_all('li')
            samples = []
            for samples_li in samples_lis :
                span_d_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_Echantillons'
                span_l_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_Echantillons'
                sample_spans = samples_li.find_all('span')
                if len(sample_spans) > 1 :
                    sample_date = sample_spans[0].get_text().strip() if sample_spans[0] else ""
                    sample_lieu = sample_spans[1].get_text().strip() if sample_spans[1] else ""
                    sample = {
                        C.RVDATE: re.sub(r'\s+', ' ', sample_date).strip(),
                        C.RVLIEU: re.sub(r'\s+', ' ', sample_lieu).strip(),
                        }
                samples.append(sample)

            # Meetings
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelReunion'
            span_id_d = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_dateReunion'
            span_id_a = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_adresseReunion'
            meeting_div  = samples_div.find_next_sibling("div", id=div_id)
            meeting_span_d = meeting_div.find('span', id=span_id)
            meeting_span_a = meeting_div.find('span', id=span_id)
            meeting_d = meeting_span_d.get_text().strip() if meeting_span_d else ""
            meeting_a = meeting_span_a.get_text().strip() if meeting_span_a else ""
            meeting = []
            if len(meeting_d) > 3 or len(meeting_a) > 3 : meeting.append({C.RVDATE: meeting_d, C.RVLIEU: meeting_a})

            # In-site Visits
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelVisitesLieux'
            # span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelRepeaterVisitesLieux'
            visits_div  = meeting_div.find_next_sibling("div", id=div_id)
            visits_lis = visits_div.find_all('li')
            visits = []
            for visits_li in visits_lis :
                span_d_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_dateVisites'
                span_l_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_dateVisites'
                visit_spans = visits_li.find_all('span')
                if len(visit_spans) > 1 :
                    visit_date = visit_spans[0].get_text().strip() if visit_spans[0] else ""
                    visit_lieu = visit_spans[1].get_text().strip() if visit_spans[1] else ""
                    visit = {
                        C.RVDATE: re.sub(r'\s+', ' ', visit_date).strip(),
                        C.RVLIEU: re.sub(r'\s+', ' ', visit_lieu).strip(),
                        }
                visits.append(visit)


            # Variante
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelVariante'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_varianteValeur'
            variante_div  = visits_div.find_next_sibling("div", id=div_id)
            variante_span = variante_div.find("div", class_="content-bloc bloc-600")
            variante = variante_span.get_text().strip() if variante_span else ""


            # ReservePME
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idRefRadio_RepeaterReferentielRadio_ctl0_panelReferentielRadio'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idRefRadio_RepeaterReferentielRadio_ctl0_labelReferentielRadio'
            pme_div  = variante_div.find_next_sibling("div", id=div_id)
            pme_span = pme_div.find('span', id=span_id)
            pme = pme_span.get_text().strip() if pme_span else ""


            # Store extracted data for current lot

            current_lot = {
                C.LOTNMB: number,
                C.OBJETL: title,
                C.CATEGL: category,
                C.DESCRI: description,
                C.ESTIMA: estimation,
                C.CAUTIO: caution,
                C.QUALIF: qualifs,
                C.AGREME: agrements,
                C.ECHANT: samples,
                C.REUNIO: meeting,
                C.VISITS: visits,
                C.VARIAN: variante,
                C.RESPME: pme,
                }

            lots.append(current_lot)
            i += 1
    return lots


def getConsObject(link_item):
    """
    # Synapsis:
        From a link, gets a structured object (JSON) representing data of the Consultation and all its related objects
    # Params:
        link_item: a line of the generated links file, containing pudlication date, portal id and organization acronym.
    # Return:
        JSON object representing data.
    """

    if link_item == None or len(link_item) < 3:
        helper.printMessage('ERROR', 'objeer.getConsObject', 'Got an invalid link item.')
        return None
    helper.printMessage('DEBUG', 'objeer.getConsObject', f'Getting objects for item id = {link_item[0]}')

    cons_link = f'{C.LINK_PREFIX}{link_item[0]}{C.LINK_STITCH}{link_item[1]}'
    dce_link = f'{C.SITE_INDEX}?page=entreprise.EntrepriseDownloadCompleteDce&reference={link_item[0]}&orgAcronym={link_item[1]}'

    rua = helper.getUa()
    rua_label = "Random"
    try:
        start_delimiter = "Mozilla/5.0 ("
        end_delimiter = "; "
        start_index = rua.index(start_delimiter) + len(start_delimiter)
        end_index = rua.index(end_delimiter, start_index)
        return rua[start_index:end_index]
    except ValueError:
        pass
    helper.printMessage('DEBUG', 'objeer.getConsObject', f'Using UA: {rua_label}.')
    headino = {"User-Agent": rua }
    sessiono = requests.Session()

    cons_bytes = 0
    try:
        dce_head = sessiono.head(dce_link, headers=headino, timeout=C.REQ_TIMEOUT, allow_redirects=True)
        if dce_head.status_code != 200 :
            helper.printMessage('ERROR', 'objeer.getConsObject', f'Request to DCE Header page returned a {dce_head.status_code} status code.')
            if dce_head.status_code == 429:
                helper.printMessage('ERROR', 'objeer.getConsObject', f'Too many Requests, said the server: {dce_head.status_code} !')
                helper.sleepRandom(300, 600)
            # return None
        if 'Content-Length' in dce_head.headers:
            cons_bytes = int(dce_head.headers['Content-Length'])
    except Exception as x:
        helper.printMessage('WARNING', 'objeer.getConsObject', f'Exception raised while getting file size at {str(dce_link)}: {str(x)}')
        # return None

    try: request_cons = sessiono.get(cons_link, headers=headino, timeout=C.REQ_TIMEOUT)  # driver.get(lots_link)
    except Exception as x:
        helper.printMessage('ERROR', 'objeer.getConsObject', f'Exception raised while getting Cons at {str(cons_link)}: {str(x)}')
        return None
    helper.printMessage('DEBUG', 'objeer.getConsObject', f'Getting Cons page : {request_cons}')
    if request_cons.status_code != 200 :
        helper.printMessage('ERROR', 'objeer.getConsObject', f'Request to Cons page returned a {request_cons.status_code} status code.')
        if request_cons.status_code == 429:
            helper.printMessage('ERROR', 'objeer.getConsObject', f'Too many Requests, said the server: {request_cons.status_code} !')
            helper.sleepRandom(300, 600)
        return None

    bowl = BeautifulSoup(request_cons.text, 'html.parser')


    soup = bowl.find(class_='recap-bloc')

    cons_idddd = link_item[0].strip()
    cons_pub_d = link_item[2].strip()

    deadl_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_dateHeureLimiteRemisePlis')
    cons_deadl = deadl_span.get_text().strip() if deadl_span else ""

    picto_img  = soup.find('img', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_pictCertificat')
    picto_src  = picto_img['src'].strip() if picto_img else ""
    cons_repec = picto_src.strip().replace('themes/images/', '').replace('.gif', '')

    cance_span = soup.find('img', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_pictConsultationAnnulee')
    cons_cance = True if cance_span else False

    categ_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_categoriePrincipale')
    cons_categ = categ_span.get_text().strip() if categ_span else ""

    refce_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_reference')
    cons_refce = refce_span.get_text().strip() if refce_span else ""

    objet_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_objet')
    cons_objet = objet_span.get_text().strip() if objet_span else ""

    helper.printMessage('DEBUG', 'objeer.getConsObject', f'Found item: {cons_refce} = {cons_objet[:C.TRUNCA]} ...')

    achet_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_entiteAchat')
    cons_achet = achet_span.get_text().strip() if achet_span else ""

    type_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_annonce')
    cons_type = type_span.get_text().strip() if type_span else ""

    proce_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_typeProcedure')
    cons_proce = proce_span.get_text().strip() if proce_span else ""

    passa_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_modePassation')
    cons_passa = passa_span.get_text().replace('|', '').strip() if passa_span else ""

    lexec_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_lieuxExecutions')
    cons_lexec = lexec_span.get_text().strip() if lexec_span else ""

    domai_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_domainesActivite')
    cons_domai = []
    domai_lis  = domai_span.find_all('li')
    for domai_li in domai_lis:
        domai = domai_li.get_text().strip() if domai_li else ""
        if len(domai) > 1 : cons_domai.append(domai)

    add_r_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseRetraitDossiers')
    cons_add_r = add_r_span.get_text().strip() if add_r_span else ""

    add_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseDepotOffres')
    cons_add_d = add_d_span.get_text().strip() if add_d_span else ""

    add_o_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_lieuOuverturePlis')
    cons_add_o = add_o_span.get_text().strip() if add_o_span else ""

    plans_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_prixAcquisitionPlan')
    cons_plans = plans_span.get_text().strip() if plans_span else ""

    adm_n_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_contactAdministratif')
    cons_adm_n = adm_n_span.get_text().strip() if adm_n_span else ""

    adm_m_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_email')
    cons_adm_m = adm_m_span.get_text().strip() if adm_m_span else ""

    adm_t_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_telephone')
    cons_adm_t = adm_t_span.get_text().strip() if adm_t_span else ""

    adm_f_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_telecopieur')
    cons_adm_f = adm_f_span.get_text().strip() if adm_f_span else ""

    reser_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_idRefRadio_RepeaterReferentielRadio_ctl0_labelReferentielRadio')
    cons_reser = reser_span.get_text().strip() if reser_span else ""

    quali_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_qualification')
    cons_quali = []
    quali_lis  = quali_span.find_all('li')
    for quali_li in quali_lis:
        quali = quali_li.get_text().strip() if quali_li else ""
        if len(quali) > 1 : cons_quali.append(quali)

    agrem_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_agrements')
    cons_agrem = []
    agrem_lis  = agrem_span.find_all('li')
    for agrem_li in agrem_lis:
        agrem = agrem_li.get_text().strip() if agrem_li else ""
        if len(agrem) > 1 : cons_agrem.append(agrem)

    # Samples
    cons_echan = []
    ech_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_dateEchantillons')
    cons_ech_d = ech_d_span.get_text().strip() if ech_d_span else ""
    ech_a_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseEchantillons')
    cons_ech_a = ech_a_span.get_text().strip() if ech_a_span else ""
    if len(cons_ech_d) > 3 or len(cons_ech_a) > 3 : cons_echan.append({C.RVDATE: cons_ech_d, C.RVLIEU: cons_ech_a})

    # Meetings
    cons_reuni = []
    reu_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_dateReunion')
    cons_reu_d = reu_d_span.get_text().strip() if reu_d_span else ""
    reu_a_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseReunion')
    cons_reu_a = reu_a_span.get_text().strip() if reu_a_span else ""
    if len(cons_reu_d) > 3 or len(cons_reu_a) > 3 : cons_reuni.append({C.RVDATE: cons_reu_d, C.RVLIEU: cons_reu_a})

    # Visits #
    cons_visit = []
    vis_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_repeaterVisitesLieux_ctl1_dateVisites')
    cons_vis_d = vis_d_span.get_text().strip() if vis_d_span else ""
    vis_a_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_repeaterVisitesLieux_ctl1_adresseVisites')
    cons_vis_a = vis_a_span.get_text().strip() if vis_a_span else ""
    if len(cons_vis_d) > 3 or len(cons_vis_a) > 3 : cons_visit.append({C.RVDATE: cons_vis_d, C.RVLIEU: cons_vis_a})

    varia_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_varianteValeur')
    cons_varia = varia_span.get_text().strip() if varia_span else ""

    estim_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_idReferentielZoneText_RepeaterReferentielZoneText_ctl0_labelReferentielZoneText')
    cons_estim = estim_span.get_text().strip() if estim_span else ""

    cauti_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_cautionProvisoire')
    cons_cauti = cauti_span.get_text().strip() if cauti_span else ""

    sized_anch = bowl.find('a', id='ctl0_CONTENU_PAGE_linkDownloadDce')
    cons_sized = sized_anch.get_text().strip() if sized_anch else ""
    cons_sized = sized_anch.get_text().strip('Dossier de consultation -').strip() if sized_anch else ""

    nbrlo_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_nbrLots')
    cons_nbrlo = nbrlo_span.get_text().replace('Lots', '').strip() if nbrlo_span else "1"
    if cons_nbrlo == '': cons_nbrlo = '1'

    lots_span = soup.find('a', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_linkDetailLots')
    lots_href = ''
    if lots_span and lots_span.has_attr('href'): lots_href = lots_span['href']

    # cons_lots = []
    if len(lots_href) > 2:
        cons_lots = getLotsObject(lots_href)
    else:
        cons_lots = [
            {
                C.LOTNMB: 1,
                C.OBJETL: cons_objet,
                C.CATEGL: cons_categ,
                C.DESCRI: '',
                C.ESTIMA: cons_estim,
                C.CAUTIO: cons_cauti,
                C.RESPME: cons_reser,
                C.QUALIF: cons_quali,
                C.AGREME: cons_agrem,
                C.ECHANT: cons_echan,
                C.REUNIO: cons_reuni,
                C.VISITS: cons_visit,
                C.VARIAN: cons_varia,
                }
            ]

    cons_dict = {
        C.PUDATE: cons_pub_d,
        C.DDLINE: cons_deadl,
        C.CANCEL: cons_cance,
        C.REFERE: cons_refce,
        C.CATEGC: cons_categ,
        C.NUMBLO: cons_nbrlo,
        C.OBJETC: cons_objet,
        C.LIEUEX: cons_lexec,
        C.ACHETE: cons_achet,
        C.TYPEAN: cons_type,
        C.PROCED: cons_proce,
        C.MODEPA: cons_passa,
        C.REPONS: cons_repec,
        C.LOTSSS: cons_lots,
        C.PRIXPL: cons_plans,
        C.DOMAIN: cons_domai,
        C.RETDOS: cons_add_r,
        C.DEPOFF: cons_add_d,
        C.LIEOUV: cons_add_o,
        C.CONTNM: cons_adm_n,
        C.CONTML: cons_adm_m,
        C.CONTTL: cons_adm_t,
        C.CONTFX: cons_adm_f,
        C.IDENTI: cons_idddd,
        C.LINKKK: cons_link,
        C.DCESIZ: cons_sized,
        C.BYTESS: cons_bytes,
        }

    return cons_dict


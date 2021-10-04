from enum import unique
import requests
from bs4 import BeautifulSoup
import re 
from time import sleep

from requests.sessions import InvalidSchema 

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Centos; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


def allowedCodes(r, allowed = [200]):
    if r.status_codes not in allowed: 
        exit(1)

def getPages(url):

    q_pages = requests.get(url, headers)
    pages = BeautifulSoup(q_pages.content, 'html.parser').find_all('a', {'class': 'butonpaginare'})


    pageNr = 0
    for page in pages: 
        if int(page['data-pagina']) > pageNr:
            pageNr = int(page['data-pagina'])
        
    return pageNr

def getUrls(url):

## (TODO) sort it out for houses as well.
## Generate the search url starting from https://www.imobiliare.ro/vanzare-apartamente/timisoara?nrcamere=3 for flats and for houses this url can be used: https://www.imobiliare.ro/vanzare-case-vile/timis?nrcamere=3
    uniqueUrls =  set()

    pages = int(getPages(url=url))
    

    for page in range(1,pages + 1):
        if pages % 5 == 0: 
            sleep(1)

        if page == 1:
            houseUrls = requests.get(url, headers)
            soup = BeautifulSoup(houseUrls.content, 'html.parser')
            sleep(0.2)            

        else:
            paginated_url= f'{url}&pagina={page}'
            houseUrls = requests.get(paginated_url, headers)
            soup = BeautifulSoup(houseUrls.content, 'html.parser')
            sleep(0.2)  

        urls = soup.find_all('a', { "data-url-params" : re.compile('lista=.*')})
        for uri in urls: 
            uniqueUrls.add(uri['href'])


    for urls in uniqueUrls: 
        try:
            getHomeDetails(urls)
        except InvalidSchema:
            continue 


def getHomeDetails(url):
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    titlu = soup.select("title")[0].string
    
    try:
        cautaDupaNrCamere = soup.find_all(text="Nr. camere:")
        nrCamere = cautaDupaNrCamere[0].parent.select("span")[0].string
    except IndexError as ie: 
        nrCamere = "unknown"

    try:
        q_suprafata_utila = soup.find_all(text="Suprafaţă utilă:")[0]
        suprafata_utila  = q_suprafata_utila.parent.select("span")[0].string
    except IndexError as ie: 
        suprafata_utila = "unknown"

    try:
        q_suprafata_construita_casa = soup.find_all(text="Suprafaţă construită")[0]
        suprafata_construita_casa   = q_suprafata_construita_casa.parent.select("span")[0].string
    except IndexError as ie: 
        suprafata_construita_casa = "unknown"

    try:
        q_compartimentare = soup.find_all(text="Compartimentare:")[0]
        compartimentare   = q_compartimentare.parent.select("span")[0].string
    except IndexError as ie: 
        compartimentare = "unknown"

    try:
        q_etaj = soup.find_all(text="Etaj:")[0]
        etaj   = q_etaj.parent.select("span")[0].string
    except IndexError as ie: 
        etaj = "unknown"

    try:
        q_nrBai = soup.find_all(text="Nr. băi:")[0]
        nrBai   = q_nrBai.parent.select("span")[0].string
    except IndexError as ie: 
        nrBai = "unknown"

    try:
        q_nrBucatarii = soup.find_all(text="Nr. bucătării:")[0]
        nrBucatarii   = q_nrBucatarii.parent.select("span")[0].string
    except IndexError as ie: 
        nrBucatarii = "unknown"

    try:
        q_anConstructie = soup.find_all(text="An construcţie:")[0]
        anConstructie   = q_anConstructie.parent.select("span")[0].string
    except IndexError as ie: 
        anConstructie = "unknown"

    try:
        q_tipImobil = soup.find_all(text="Tip imobil:")[0]
        tipImobil   = q_tipImobil.parent.select("span")[0].string
    except IndexError as ie: 
        tipImobil = "unknown"

    try:
        q_regimInaltime = soup.find_all(text="Regim înălţime:")[0]
        regimInaltime   = q_regimInaltime.parent.select("span")[0].string
    except IndexError as ie: 
        regimInaltime = "unknown"
    
    try:
        q_parcare = soup.find_all(text="Nr. locuri parcare:")[0]
        parcare   = q_parcare.parent.select("span")[0].string
    except IndexError as ie: 
        parcare = "unknown"

    try: 
        q_pret  = soup.find_all("span", {"title": "Conversie pret - 150"})[0].parent
        pret_ron = q_pret.select("span")[0].getText().split('RON')
        pret_usd = pret_ron[1].split()
    except  IndexError as ie:
        pret_ron = "unknown"
        pret_usd = "unknown"
    try: 
        q_pret_euro = soup.find_all("div", {"class":"pret-cerut"})[0]
        pret_euro   = q_pret_euro.select("span")[0].string.split(" ")[0]
    except IndexError as ie: 
        pret_euro = "unknown"

    print(f"{url};{nrCamere};{suprafata_utila}; {compartimentare}; {etaj}; {nrBai}; {nrBucatarii}; {anConstructie}; {tipImobil}; {regimInaltime};{parcare};{pret_ron[0]};{pret_usd[0]};{pret_euro};{titlu}")




print("url; Nr Camere; Suprafata Utila; Compartimentare; Etaj; Nr Bai; Nr Bucatarii; An constructie; Tip Imobil; Regim Inaltime; Parcare; Pret Ron; Pret USD; Pret Euro;titlu")
# getHomeDetails("https://www.imobiliare.ro/vanzare-apartamente/timisoara/take-ionescu/apartament-de-vanzare-3-camere-XCBD0000A?lista=8770933&listing=1&sla=lista&imoidviz=3191942853")
# getHomeDetails("https://www.imobiliare.ro/vanzare-apartamente/timisoara/bucovina/apartament-de-vanzare-3-camere-XAII0000N?lista=8770933&listing=1&sla=lista&imoidviz=3191942853")


#getUrls("https://www.imobiliare.ro/vanzare-apartamente/timis?nrcamere=3")
getUrls("https://www.imobiliare.ro/vanzare-apartamente/timisoara?nrcamere=3")
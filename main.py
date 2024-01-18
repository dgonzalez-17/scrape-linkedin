from fastapi import FastAPI
from selenium import webdriver
from fastapi.middleware.cors import CORSMiddleware
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
import time
from pydantic import BaseModel
logging.basicConfig(format='%(asctime)s %(message)s')
import os
from selenium.webdriver.chrome.service import Service
import pickle as pkl
import random




EMAIL = 'pruebaws50@gmail.com'
PASSWORD = 'WebscrapingLinkedin50'


# chrome_driver_path = 'chromedriver.exe'
options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("start-maximized")
options.add_argument('--start-fullscreen')
options.add_argument('--single-process')
options.add_argument("--incognito")
options.add_argument("disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False) 
# options.add_argument('proxy-server=106.122.8.54:3128')
driver = webdriver.Chrome(service = Service(os.environ.get("CHROMEDRIVER_PATH")), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
# driver = webdriver.Chrome(options=options)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragent}) 


class ScrapeCompany(BaseModel):
    url: str
class ScrapeUser(BaseModel):
    url: str

@app.post("/company/")
def scrape_company(request: ScrapeCompany):
    url = request.url
    driver = webdriver.Chrome(service = Service(os.environ.get("CHROMEDRIVER_PATH")), options=options)
    driver.get(url)
    cookies = pkl.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(2)
    try:
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'icon.contextual-sign-in-modal__modal-dismiss-icon.lazy-loaded').click()
    except:
        logging.warning('No se encontró el botón para cerrar el modal de "registrate / inicia sesión"')

    #Nombre empresa
    nombre_empresa = ''
    try:
        nombre_empresa = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div:nth-child(1) > h1').text
    except:
        logging.warning('No se encontro nombre empresa')

    try: 
        sede_seguidores = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div:nth-child(1) > h3').text
    except:
        logging.warning('No se encontro sede seguidores')
        
    #sede
    try:
        sede = ''
        sede = ' '.join(sede_seguidores.split()[:-2])
    except:
        logging.warning('No se encontro sede')
    #Seguidores
    try:
        seguidores = ''
        seguidores = ' '.join(sede_seguidores.split()[-2:])
    except:
        logging.warning('No se encontro seguidores')


    #Area / Sector
    try:
        sector = ''
        sector = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div:nth-child(1) > h2').text
    except:
        logging.warning('No se encontro sector')

    #Sobre nosotros
    try:
        descripcion = ''
        descripcion = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.text-color-text > div > p').text
    except:
        logging.warning('No se encontro descripcion')
    #Sitio web

    try:
        sitio_web = ''
        sitio_web = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.text-color-text > div > dl > div:nth-child(1) > dd > a').text
    except:
        logging.warning('No se encontro sitio web')
    #Tamaño de la empresa

    try:
        tamano=''
        tamano = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.text-color-text > div > dl > div:nth-child(3) > dd').text
    except:
        logging.warning('No se encontro tamaño empresa')
    #Tipo de empresa

    try:
        tipo = ''
        tipo = driver.find_element(By.CSS_SELECTOR,'#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.text-color-text > div > dl > div:nth-child(5) > dd').text
    except:
        logging.warning('No se encontro tipo')
    #Especialidades

    try:
        especialidades= ''
        especialidades = driver.find_element(By.CSS_SELECTOR,'#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.text-color-text > div > dl > div:nth-child(6) > dd').text
    except:
        logging.warning('No se encontro especialidades')
    #Ubicaciones
    try:
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.locations > div > div > button.show-more-less__button.show-more-less__more-button.show-more-less-button').click()
    except:
        logging.warning( 'Click interceptado ubicaciones')

    try:
        ubicaciones = ''
        ubicaciones = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.locations > div > div > ul')
    except:
        logging.warning('No se encontro ubicaciones')

    locations = []
    try:
        for ubicacion in ubicaciones.find_elements(By.TAG_NAME, 'li'):
            location = {'Principal':False, 'Address':''}
            try:
                ubicacion.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.core-section-container.my-3.core-section-container--with-border.border-b-1.border-solid.border-color-border-faint.m-0.py-3.locations > div > div > ul > li:nth-child(1) > span')
                location['Principal'] = True
            except:
                pass
            location['Address'] = ubicacion.find_element(By.TAG_NAME, 'div').text.replace('\n', ' ')
            if location['Address'] != '':
                locations.append(location)
    except:
        pass

    elem = driver.find_element(By.TAG_NAME, "html")
    elem.send_keys(Keys.END)

    #Paginas asociadas
    try:
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '#main-content > section.right-rail.papabear\:w-right-rail-width.papabear\:ml-column-gutter.mamabear\:max-w-\[790px\].mamabear\:px-mobile-container-padding.babybear\:max-w-\[790px\].babybear\:px-mobile-container-padding > section:nth-child(1) > div > div > button.show-more-less__button.show-more-less__more-button.show-more-less-button').click()
    except:
        logging.warning( 'Click interceptado paginas asociadas')

    try:
        asociadas=''
        asociadas = driver.find_element(By.CSS_SELECTOR, '#main-content > section.right-rail.papabear\:w-right-rail-width.papabear\:ml-column-gutter.mamabear\:max-w-\[790px\].mamabear\:px-mobile-container-padding.babybear\:max-w-\[790px\].babybear\:px-mobile-container-padding > section:nth-child(1) > div > div > ul')
    except:
        logging.warning('No se encontro asociadas')

    associated_pages = []
    try:
        for page in asociadas.find_elements(By.TAG_NAME, 'li'):
            pagina = {'name':'', 'url':'', 'detail':''}

            try:
                pagina['name'] = page.find_element(By.TAG_NAME, 'h3').text
            except:
                logging.warning('No se encontro nombre pagina asociada')
            try:
                pagina['url'] = page.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                logging.warning('No se encontro url pagina asociada')
            try:
                pagina['detail'] = ' '.join([i.text for i in page.find_elements(By.TAG_NAME, 'p')])
            except:
                logging.warning('No se encontro detalle pagina asociada')

            if pagina['name'] != '':
                associated_pages.append(pagina)
    except:
        pass


    #Paginas similares

    try:
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#main-content > section.right-rail.papabear\:w-right-rail-width.papabear\:ml-column-gutter.mamabear\:max-w-\[790px\].mamabear\:px-mobile-container-padding.babybear\:max-w-\[790px\].babybear\:px-mobile-container-padding > section:nth-child(2) > div > div > button.show-more-less__button.show-more-less__more-button.show-more-less-button').click()
    except:
        logging.warning( 'Click interceptado paginas similares')

    try:
        similares=''
        similares = driver.find_element(By.CSS_SELECTOR, '#main-content > section.right-rail.papabear\:w-right-rail-width.papabear\:ml-column-gutter.mamabear\:max-w-\[790px\].mamabear\:px-mobile-container-padding.babybear\:max-w-\[790px\].babybear\:px-mobile-container-padding > section:nth-child(2) > div > div > ul')
    except:
            logging.warning('No se encontro nombre paginas similares')
    similar_pages = []

    try:
        for page in similares.find_elements(By.TAG_NAME, 'li'):
            pagina = {'name':'', 'url':'', 'detail':''}
            try:
                pagina['name'] = page.find_element(By.TAG_NAME, 'h3').text
            except:
                logging.warning('No se encontro nombre pagina similar')
            try:
                pagina['url'] = page.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                logging.warning('No se encontro url pagina similar')
            try:
                pagina['detail'] = ' '.join([i.text for i in page.find_elements(By.TAG_NAME, 'p')])
            except:
                logging.warning('No se encontro detail pagina similar')
            similar_pages.append(pagina)
    except:
        pass


    #Financiacion
    investments = {'number':'', 'last_date':'', 'last_value':''}
        #Numero de rondas

    try:
        investments['number'] = driver.find_element(By.CSS_SELECTOR, '#main-content > section.right-rail.papabear\:w-right-rail-width.papabear\:ml-column-gutter.mamabear\:max-w-\[790px\].mamabear\:px-mobile-container-padding.babybear\:max-w-\[790px\].babybear\:px-mobile-container-padding > section:nth-child(5) > div > a.link-styled.text-sm.mb-1.inline-block.\!text-color-text-secondary > span.before\:middot').text
    except:
        logging.warning('No se encontro numero inversiones')    
    #Ultima ronda
            #fecha
    try:
        investments['last_date'] = driver.find_element(By.CSS_SELECTOR, '#main-content > section.right-rail.papabear\:w-right-rail-width.papabear\:ml-column-gutter.mamabear\:max-w-\[790px\].mamabear\:px-mobile-container-padding.babybear\:max-w-\[790px\].babybear\:px-mobile-container-padding > section:nth-child(5) > div > div > a > time').text
    except:
        logging.warning('No se encontro fecha ultima inversion')  
            #monto
    try:
        investments['last_value'] = driver.find_element(By.CSS_SELECTOR,'#main-content > section.right-rail.papabear\:w-right-rail-width.papabear\:ml-column-gutter.mamabear\:max-w-\[790px\].mamabear\:px-mobile-container-padding.babybear\:max-w-\[790px\].babybear\:px-mobile-container-padding > section:nth-child(5) > div > div > p.text-display-lg' ).text
    except:
        logging.warning('No se encontro valor ultima inversion')  
    #Cultura (vida en la empresa)
    cultura = ''
    try:
        driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > nav > ul > li:nth-child(3) > a').click()
        cultura = driver.find_element(By.CSS_SELECTOR, '#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section:nth-child(4) > div > div > div:nth-child(1) > p').text
    except:
        logging.warning( 'Click interceptado Cultura')
    try:
        driver.close()
    except:
        pass

    empresa = {'name':nombre_empresa, 'headquarters':sede, 'followers':seguidores, 'sector':sector, 'description':descripcion, 'website':sitio_web, 'size':tamano,
            'type':tipo, 'specialties':especialidades, 'locations':locations, 'associated_pages':associated_pages, 'similar_pages':similar_pages, 'investments':investments, 'culture':cultura}
    return empresa

@app.post("/user/")
def scrape_user(request: ScrapeUser):
    url = request.url
    driver = webdriver.Chrome(service = Service(os.environ.get("CHROMEDRIVER_PATH")), options=options)

    try:
        driver.get('https://www.linkedin.com/checkpoint/rm/sign-in-another-account')
        cookies = pkl.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        email_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
        
        def escribir_letra_por_letra(campo, texto):
            for caracter in texto:
                campo.send_keys(caracter)
                time.sleep(0.1)

        escribir_letra_por_letra(email_field, EMAIL)
        escribir_letra_por_letra(password_field, PASSWORD)
        time.sleep(0.2)
        logging.info("Escribí correo y contraseña")
        print("Escribí correo y contraseña")
        print(driver.current_url)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        print(driver.current_url)
    except:
        print(driver.current_url)
        logging.warning('No fue necesario iniciar sesión en el nuevo link u ocurrió un error intentándolo')
    

    driver.get(url)
    cookies = pkl.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    logging.info('Ingreso al url')
    print(driver.current_url)

    try:
        driver.find_element(By.CSS_SELECTOR, '#public_profile_contextual-sign-in > div > section > button').click()
        logging.info('Clic iniciar sesion')
        print("Clic iniciar sesion")
        print(driver.current_url)
    except:
        print(driver.current_url)
        logging.warning('No se encontró el botón para cerrar el modal de "registrate / inicia sesión"')
        
    try:
        driver.find_element(By.CSS_SELECTOR, 'body > header > nav > div > a.nav__button-secondary.btn-md.btn-secondary-emphasis').click()
        email_field = driver.find_element(By.CSS_SELECTOR, '#username')
        password_field = driver.find_element(By.CSS_SELECTOR, '#password')
        
        def escribir_letra_por_letra(campo, texto):
            for caracter in texto:
                campo.send_keys(caracter)
                time.sleep(0.1)

        escribir_letra_por_letra(email_field, EMAIL)
        escribir_letra_por_letra(password_field, PASSWORD)
        logging.info("Escribí correo y contraseña")
        print("Escribí correo y contraseña")
        print(driver.current_url)

        driver.find_element(By.CSS_SELECTOR, '#organic-div > form > div.login__form_action_container > button').click()
    except:
        print(driver.current_url)
        logging.warning('No fue necesario iniciar sesión u ocurrió un error intentándolo')
    print(driver.current_url)
    elem = driver.find_element(By.TAG_NAME, "html")
    elem.send_keys(Keys.END)

    #Nombre
    try:
        seccion_perfil = driver.find_element(By.CSS_SELECTOR, '[data-member-id]')
    except:
        logging.warning('No econtrada seccion perfil')
    try:
        div_perfil = seccion_perfil.find_element(By.CLASS_NAME, 'mt2.relative')
    except:
        logging.warning('No econtrado div perfil')
    try:
        divs = div_perfil.find_elements(By.TAG_NAME, 'div')
    except:
        logging.warning('No econtrada seccion divs')
    try:
        ul = div_perfil.find_element(By.TAG_NAME, 'ul')
    except:
        logging.warning('No econtrada seccion ul')
    
    try:
        secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    except:
        logging.warning('No econtrada seccion secciones')

    nombre_usuario = ''
    try:
        nombre_usuario = div_perfil.find_element(By.CSS_SELECTOR, 'span.artdeco-hoverable-trigger.artdeco-hoverable-trigger--content-placed-bottom.artdeco-hoverable-trigger--is-hoverable.ember-view').text
    except:
        try:
            nombre_usuario = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            logging.warning( 'No se encontró nombre usuario')

    #Caption
    caption = ''
    try:
        caption = div_perfil.find_element(By.CSS_SELECTOR, 'div.text-body-medium.break-words').text
    except:
        logging.warning( 'No se encontró caption')

    #Temas que suele tratar
        
    topics = ''
    try:
        topics = div_perfil.find_element(By.CSS_SELECTOR, 'div.text-body-medium.break-words').text
    except:
        logging.warning( 'No se encontró temas que suele tratar')

    #Instituciones
    institutions = ''
    try:
        institutions = ul.text.split('\n')
    except:
        logging.warning( 'No se encontró instituciones')  


    #Ubicacion
    ubicacion = ''
    try:
        ubicacion = driver.find_element(By.CSS_SELECTOR, 'span.text-body-small.inline.t-black--light.break-words').text
    except:
        logging.warning( 'No se encontró ubicacion')  

    #Website
    website = ''
    try:
        website = driver.find_element(By.CSS_SELECTOR, 'section.pv-top-card--website.text-body-small').text
    except:
        logging.warning( 'No se encontró website')  

    #Acerca de
    acerca_de = ''
    try:
        seccion_acerca = None
        for seccion in secciones:
            if seccion.text.startswith('Acerca de'):
                seccion_acerca = seccion
        time.sleep(2)
        seccion_acerca.find_element(By.CSS_SELECTOR,'[role="button"]').click()
        acerca_de = seccion_acerca.text.replace('Acerca de\n','')
    except:
        try:
            acerca_de = seccion_acerca.text.replace('Acerca de\n','')
        except:
            pass
        logging.warning( 'Click ver mas acerca de interceptado') 


    #Experiencia
        
    try:
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '#navigation-index-see-all-experiences').click()
    except:
        logging.warning( 'Interceptado click ver todas las experiencias')  


    try:
        lista_experiencias = driver.find_element(By.CLASS_NAME, 'pvs-list').find_elements(By.XPATH, '*')
    except:
        logging.warning( 'No se encontró lista experiencias')
        
    experiencies = []
    try:
        for exp in lista_experiencias:
            experiencia = {}
            try:
                experiencia['title'] = exp.find_element(By.CLASS_NAME, 'display-flex.align-items-center.mr1.t-bold').text.split('\n')[0]
            except:
                experiencia['title'] = ''
            try:
                experiencia['company'] = exp.find_element(By.CLASS_NAME, 't-14.t-normal').text.split('\n')[0]
            except:
                experiencia['company'] = ''

            try:
                temp = [i.text.split('\n')[0] for i in exp.find_elements(By.CLASS_NAME, 't-14.t-normal.t-black--light')]
            except:
                pass

            try:
                experiencia['date'] = temp[0]
                if len(temp) > 1:
                    experiencia['place'] = temp[1]
                else:
                    experiencia['place'] = ''

                experiencies.append(experiencia)
            except:
                pass
            
    except:
        pass

    try:
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@aria-label="Volver a la página del perfil principal"]').click()
    except:
        logging.warning( 'Click interceptado go back')


    try:
        driver.find_element(By.CSS_SELECTOR, '#navigation-index-see-all-education').click()
    except:
        logging.warning( 'Click interceptado ver toda educacion')


    #Educacion
        
    secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    try:
        seccion_educacion = None
        for seccion in secciones:
            if seccion.text.startswith('Educación'):
                seccion_educacion = seccion

        lista_educaciones=[]
        lista_educaciones = seccion_educacion.find_element(By.CLASS_NAME, 'pvs-list').find_elements(By.XPATH, '*')
    except:
        logging.warning( 'No se encontró lista educacion')

    educaciones = []
    try:

        for edu in lista_educaciones:
            educacion = {'institucion':'', 'titulo':'', 'fecha':''}
            try:
                educacion['institucion'] = edu.find_element(By.CLASS_NAME, 'display-flex.flex-wrap.align-items-center.full-height').text.split('\n')[0]
            except:
                pass

            try:
                educacion['titulo'] = edu.find_element(By.CLASS_NAME, 't-14.t-normal').text.split('\n')[0]
            except:
                pass

            try:
                educacion['date'] = edu.find_element(By.CLASS_NAME, 'pvs-entity__caption-wrapper').text.split('\n')[0] 
            except:
                pass
            if educacion['titulo'] != '':
                educaciones.append(educacion)
    except:
        pass    

    try:
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@aria-label="Volver a la página del perfil principal"]').click()
    except:
        logging.warning( 'Click interceptado go back')


    #Proyectos
    secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    proyectos = []
    try:
        seccion_proyect = None
        for seccion in secciones:
            if seccion.text.startswith('Proyectos'):
                seccion_proyect = seccion

        lista_proyectos = seccion_proyect.find_element(By.TAG_NAME, 'ul').find_elements(By.XPATH, '*')

        proyectos = [proy.find_element(By.CLASS_NAME, 'display-flex.flex-row.justify-space-between').text for proy in lista_proyectos]

    except:
        pass
        
        
    #Conocimientos
    secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    conocimientos = []
    try:
        seccion_conocimiento = None
        for seccion in secciones:
            if seccion.text.startswith('Conocimientos y aptitudes'):
                seccion_conocimiento = seccion

        lista_conocimientos = seccion_conocimiento.find_element(By.TAG_NAME, 'ul').find_elements(By.XPATH, '*')
        conocimientos = [i.find_element(By.CLASS_NAME, 'display-flex.flex-row.justify-space-between').text.split('\n')[0] for i in lista_conocimientos]

    except:
        pass


    #Publicaciones
    secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    publicaciones = []
    try:
        seccion_pub = None
        for seccion in secciones:
            if seccion.text.startswith('Publicaciones'):
                seccion_pub = seccion

        lista_publicaciones = seccion_pub.find_element(By.TAG_NAME, 'ul').find_elements(By.XPATH, '*')
        publicaciones = [i.find_element(By.CLASS_NAME, 'display-flex.flex-wrap.align-items-center.full-height').text.split('\n')[0] for i in lista_publicaciones]

    except:
        pass

    #causas beneficas
    secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    causas = ''
    try:
        seccion_causas = None
        for seccion in secciones:
            if seccion.text.startswith('Causas benéficas'):
                seccion_causas = seccion

        causas = seccion_causas.find_element(By.CLASS_NAME, 'display-flex.ph5.pv3').text

    except:
        pass

    #Logros

    secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    logros = []
    try:
        seccion_logr = None
        for seccion in secciones:
            if seccion.text.startswith('Reconocimientos y premios'):
                seccion_logr = seccion

        lista_logros = seccion_logr.find_element(By.TAG_NAME, 'ul').find_elements(By.XPATH, '*')
        logros = [i.find_element(By.CLASS_NAME, 'display-flex.flex-wrap.align-items-center.full-height').text.split('\n')[0] for i in lista_logros]

    except:
        pass

    #Idiomas

    secciones = driver.find_elements(By.CSS_SELECTOR, '[data-view-name="profile-card"]')
    idiomas = []
    try:
        seccion_idiomas = None
        for seccion in secciones:
            if seccion.text.startswith('Idiomas'):
                seccion_idiomas = seccion

        lista_idiomas = seccion_idiomas.find_element(By.TAG_NAME, 'ul').find_elements(By.XPATH, '*')
        idiomas = [i.find_element(By.CLASS_NAME, 'display-flex.flex-wrap.align-items-center.full-height').text.split('\n')[0] for i in lista_idiomas]

    except:
        pass

    persona = {'name':nombre_usuario, 'caption':caption, 'topics':topics, 'institutions':institutions, 'location':ubicacion,'website':website,
            'about':acerca_de, 'experiencies':experiencies, 'education':educaciones, 'projects':proyectos, 'skills':conocimientos,'publications':publicaciones, 'charity':causas, 'honors':logros, 'languages':idiomas}
    try:
        driver.close()
    except:
        pass
    return persona
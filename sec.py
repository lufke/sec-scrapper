from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import pymongo
from dotenv import load_dotenv
import os
from colorama import init, Fore
from apscheduler.schedulers.blocking import BlockingScheduler


init()

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=options)


cliente = pymongo.MongoClient(os.environ.get("URL_MONGO"))
db = cliente['sec']
tabla = db['sello_sec']


def busca_producto(codigo):
    try:
        driver.get(f'https://ww6.sec.cl/qr/qr.do?a=prod&i={codigo:013d}')
        sello = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]').text
        res_excenta = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]').text
        fecha_resolucion = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td[2]').text
        emisor = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[4]/td[2]').text
        producto = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]').text
        marcas = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]').text
        modelo = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]').text
        pais = driver.find_element(
            by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]').text

        datos = {'_id': codigo, 'codigo': f'{codigo:013d}', 'res_excenta': res_excenta, 'fecha_resolucion': fecha_resolucion,
                         'emisor': emisor, 'producto': producto, 'marca': marcas, 'modelo': modelo, 'pais': pais}
        tabla.insert_one(datos)
        # print(datos)

        print(Fore.GREEN + f'Sello: {codigo:013d} guardado' + Fore.RESET)

    except NoSuchElementException:
        print(Fore.RED + f'Sello: {codigo:013d} no existe' + Fore.RESET)

    except Exception as e:
        print(f'{e}')

    # finally:
    #     driver.quit()


def obtener_sellos():
    for cliente in range(1,9999999999999+1):
        busca_producto(cliente)

sched = BlockingScheduler(timezone="America/Santiago")
sched.add_job(obtener_sellos, 'cron', day_of_week=5, hour=23, minute=20)
sched.start()
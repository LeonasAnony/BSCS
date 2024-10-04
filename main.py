from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import vlc
import requests
import re
import datetime as dt

### OPTIONS
# Termin soll vor diesem Datum sein:
soll_vor_datum = "25.09.2024"
# Standort URL:
# md=5 -> BSC Mitte; md=4 -> BSC Stresemannstraße
location_url = 'https://termin.bremen.de/termine/select2?md=4'
# Termin URL:
# mdt=??? -> BSC Mitte; mdt=800 -> BSC Stresemannstraße
# cnc-8580 -> Personalausweis beantragen; cnc-8599 -> Personalausweis abholen; cnc-9281 -> KFZ ummelden
date_url = 'https://termin.bremen.de/termine/location?mdt=800&select_cnc=1&cnc-9281=1'
# Webhook für Benachrichtigung
webhook_url = ""
# Play sound
sound = True
# Abfragen Intervall
interval = 60
# Server Installation
server = False

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--remote-debugging-port=9222")
def create_driver():
	# Server:
	if server:
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
	# Desktop:
	else:
		driver = webdriver.Chrome(options=options)
	return driver

soll_datetime = dt.datetime.strptime(soll_vor_datum, "%d.%m.%Y")

class color:
	OK = '\033[92m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

def get_next_date():
	driver = create_driver()
	driver.get(location_url)
	time.sleep(1)
	driver.get(date_url)
	time.sleep(1)

	summary_text = driver.find_element(By.ID, 'suggest_location_summary').text
	datum = re.search(r"\d{2}\.\d{2}\.\d{4}", summary_text).group()
	zeit = re.search(r"\d{2}\:\d{2}", summary_text).group()
	driver.quit()

	return dt.datetime.strptime(datum+" "+zeit, "%d.%m.%Y %H:%M"), datum, zeit


termin_found = False
while (not termin_found):
	time.sleep(interval)

	if dt.datetime.now().time() >= dt.time(1, 0) and dt.datetime.now().time() <= dt.time(8, 0):
		continue

	next_datetime, datum, zeit = get_next_date()

	if next_datetime > soll_datetime:
		print(color.FAIL, datum, zeit, color.ENDC)
		continue

	termin_found = True
	print(color.OK, "Termin frei am "+datum+" um "+zeit, color.ENDC)
	if sound:
		p = vlc.MediaPlayer("./notification.mp3")
		p.play()

	if webhook_url != "":
		#requests.post(webhook_url, data=f"success={termin_found}&timestamp={next_datetime.timestamp()}&datum={datum}&zeit={zeit}")
		requests.post(webhook_url)

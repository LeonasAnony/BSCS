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
from pick import pick

def load_files():
	bscs_string = open("./lib/BSCs.txt", "r").read()
	bscs_list = []
	for bsc in bscs_string.split("\n"):
		bscs_list.append(bsc.split(","))
	typs_string = open("./lib/typs.txt", "r").read()
	typs_list = []
	for typ in typs_string.split("\n"):
		typs_list.append(typ.split(","))
	return bscs_list, typs_list

if __name__ == "__main__":
	bscs_list, typs_list = load_files()
	title = 'Bitte wähle das BSC aus bei dem du ein termin suchen willst: '
	options = [i[0] for i in bscs_list]
	option, index = pick(options, title)
	print(option)
	print(index)
	title = 'Bitte wähle den Grund des Termins aus: '
	options = [i[0] for i in typs_list]
	option, index = pick(options, title)
	print(option)
	print(index)

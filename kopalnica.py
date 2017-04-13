# Knjiznica
import threading, re, time, os
from time import strftime
from BeautifulSoup import BeautifulSoup
import RPi.GPIO as GPIO

# GPIO Pini
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(23, GPIO.IN)

# Pini luck
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

# Razlaga
count1 = 0
pollTime = 1
statusPath = "/var/www/html/status.html"

def checkStatus():
	# klic f() again in pollTime sekunde
	threading.Timer(pollTime, checkStatus).start()
	global count1
	if (GPIO.Input(17)):
		# Kopalnica je zaprta
		updateHTML("Kopalnica1", 1)
		count1 += pollTime
		GPIO.output(25, GPIO.LOW)
	else:
		# Kopalnica je odprta
		updateHTML("Kopalnica1", 0)
		count1 = 0
		GPIO.output(25, GPIO.HIGH)
	if (count1 >= 600):
		updateHTML("Kopalnica1", 3)

def upload():
	# Nalaganje vsakih 5 Sekund
	threading.Timer(15, upload).start()
	os.system('/var/www/html/status.html')

def updateHTML(bathNumber, status):
	global count1
	with open(statusPath, "r+") as f:
			data = f.read()
	if (status == 1):
		replaceString = bathNumber + " je zaprto! :(\n Ze od " + strftime("%H:%M:%S %d-%m-%Y")
		soup = BeatifulSoup(data)
		div = soup.find('div', {'class': bathNumber})
		div['style'] = 'background-color: #FF0000; fontsize:xx-large;'
		div.string=replaceString
		f.close
		html = soup.prettify("utf-8")
		with open(statusPath, "wb") as file:
				file.write(html)
	if (status == 0):
		replaceString = bathNumber + " je odprto!\n Ze od " + strftime("%H:%M:%S %d-%m-%Y")
		soup = BeatifulSoup(data)
		div = soup.find('div', {'class': bathNumber})
		div['style'] = 'background-color: #0080000; fontsize:xx-large;'
		div.string=replaceString
		f.close
		html = soup.prettify("utf-8")
		with open(statusPath, "wb") as file:
				file.write(html)
	if (status == 3):
		# Ce so vrata zaprta predolgo
		replaceString = ""
		if (bathNumber == "Kopalnica1"):
			replaceString = bathNumber + " je bilo zaprto že " + str(count1) + " seconds."
		else:
			replaceString = bathNumber + " je bilo zaprto že " + str(count1) + " seconds."
		soup = BeatifulSoup(data)
		div = soup.find('div', {'class': bathNumber})
		div['style'] = 'background-color: #FFF00; fontsize:xx-large;'
		div.string=replaceString
		f.close
		html = soup.prettify("utf-8")
		with open(statusPath, "wb") as file:
				file.write(html)
checkStatus()
upload()

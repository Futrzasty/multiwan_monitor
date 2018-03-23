#!/usr/bin/python

import RPi.GPIO as GPIO, urllib2, socket
import lcddriver2
import smbus
import datetime
from time import *

back_file = "backlight.state"

plik = open(back_file)
try:
	back_state = plik.read()
finally:
	plik.close()

if back_state != "0" and back_state != "1":
	back_state = "1"

back_state = int(back_state)

lcd = lcddriver2.lcd(0, back_state) #(clear, backlight)
bus = smbus.SMBus(1)

LED0 = 0x01
LED1 = 0x02
LED2 = 0x04
LED3 = 0x08
LED4 = 0x10
LED5 = 0x20
LED6 = 0x40
LED7 = 0x80

LED_orange = LED7
LED_yellow = LED6
LED_red    = LED5
LED_green  = LED4
LED_white  = LED3
LED_blue   = LED2
LED_sqyel  = LED1
LED_sqgr   = LED0


LED = 0x00

#check_host = "http://check-ip.eu"
check_host = "http://194.28.50.46"
timeout = 10

token_tp = "tp621426172189"
token_cp = "cp736528735293"
token_pl = "pl912476189274"
token_lt = "lt801284777436"
token_la = "tm801887278436"
token_or = "or716241762462"
token_tu = "tu238290024861"


text_tp = "TPNET "
text_cp = "Polsat"
text_pl = "Plus 1"
text_lt = "Plus 2"
text_la = "T-Mobi"
text_or = "Orange"
text_tu = "TM-unl"

text_ok = " OK "
text_er = " ER "
text_di = " -- "

padding = "          "

try:
	html = urllib2.urlopen(check_host+":8081/get_token.php", None, timeout).read()
	rtoken = html.decode("utf8")
except urllib2.URLError as e:
	rtoken = "Error"
except socket.timeout:
	rtoken = "Timeout"
if rtoken == token_tp:
	text_tp = text_tp + text_ok
else:
	LED = LED + LED_orange
	text_tp = text_tp + text_er


try:
	html = urllib2.urlopen(check_host+":8082/get_token.php", None, timeout).read()
	rtoken = html.decode("utf8")
except urllib2.URLError as e:
	rtoken = "Error"
except socket.timeout:
	rtoken = "Timeout"
if rtoken == token_cp:
	text_cp = text_cp + text_ok
else:
	LED = LED + LED_yellow
	text_cp = text_cp + text_er

try:
	html = urllib2.urlopen(check_host+":8083/get_token.php", None, timeout).read()
	rtoken = html.decode("utf8")
except urllib2.URLError as e: 
	rtoken = "Error"
except socket.timeout:
	rtoken = "Timeout"
if rtoken == token_pl:
	text_pl = text_pl + text_ok
else:
	LED = LED + LED_green
	text_pl = text_pl + text_er


try:
	html = urllib2.urlopen(check_host+":8084/get_token.php", None, timeout).read()
	rtoken = html.decode("utf8")
except urllib2.URLError as e: 
	rtoken = "Error"
except socket.timeout:
	rtoken = "Timeout"
if rtoken == token_lt:
	text_lt = text_lt + text_ok
else:
	LED = LED + LED_red
	text_lt = text_lt + text_er

"""
try:
	html = urllib2.urlopen(check_host+":8085/get_token.php", None, timeout).read()
	rtoken = html.decode("utf8")
except urllib2.URLError as e: 
	rtoken = "Error"
except socket.timeout:
	rtoken = "Timeout"
if rtoken == token_la:
	text_la = text_la + text_ok
else:
	LED = LED + LED_blue
	text_la = text_la + text_er
"""
"""
try:
	html = urllib2.urlopen(check_host+":8086/get_token.php", None, timeout).read()
	rtoken = html.decode("utf8")
except urllib2.URLError as e: 
	rtoken = "Error"
except socket.timeout:
	rtoken = "Timeout"
if rtoken == token_or:
	text_or = text_or + text_ok
else:
	LED = LED + LED_white
	text_or = text_or + text_er
"""

try:
	html = urllib2.urlopen(check_host+":8087/get_token.php", None, timeout).read()
	rtoken = html.decode("utf8")
except urllib2.URLError as e: 
	rtoken = "Error"
except socket.timeout:
	rtoken = "Timeout"
if rtoken == token_tu:
	text_tu = text_tu + text_ok
else:
	LED = LED + LED_blue
	text_tu = text_tu + text_er


czas = unicode(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
currentHour = datetime.datetime.now().hour

if LED!=0:
	plik = open("/home/pi/linklog", 'a')
	plik.write('%s: %s, %s, %s, %s, %s\n'%(datetime.datetime.now(), text_tp, text_cp, text_pl, text_lt, text_tu ))
	plik.close()


if currentHour < 7 or currentHour == 23:
	LED = 0

bus.write_byte(0x21, 0xFF-LED)

lcd.display_string("  "+czas+"  ", 1, LED!=0)
#lcd.display_string(text_lt, 1, LED!=0)
lcd.display_string(text_tp + padding, 2, LED!=0)
lcd.display_string(text_cp + text_tu, 3, LED!=0)
lcd.display_string(text_pl + text_lt, 4, LED!=0)

new_back = int(LED!=0)

if back_state != new_back:
	plik = open(back_file, 'w')
	plik.write(str(new_back))
	plik.close()


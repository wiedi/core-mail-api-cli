#!/usr/bin/env python

import smtplib
import imaplib
import uuid
import time

def send(to, from_addr, server, port=25, user=None, password=None, ssl=False, body = False, debug=0):
	if ssl:
		server = smtplib.SMTP_SSL(server, port)
	else:
		server = smtplib.SMTP(server, port)

	server.set_debuglevel(debug)
	server.ehlo_or_helo_if_needed()
	if user:
		server.login(user, password)

	subject = str(uuid.uuid4())
	if not body:
		body = subject
	msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (from_addr, ", ".join(to), subject, body)

	server.sendmail(from_addr, to, msg)
	server.quit()

	return subject

def waitformail(token, server, port, user=None, password=None, ssl=False, debug=None):
	if ssl:
		mail = imaplib.IMAP4_SSL(server, port)
	else:
		mail = imaplib.IMAP4(server, port)

	mail.login(user, password)
	mail.select("inbox")
	result, data = mail.uid('search', None, '(HEADER Subject "' + token + '")')
	waited_seconds = 0
	wait_interval  = 5
	while len(data) < 1 or data[0] == '':
		if debug:
			print "waiting for mail... since %s seconds" % waited_seconds
		time.sleep(wait_interval)
		waited_seconds += wait_interval
		if waited_seconds > 120:
			raise Exception("Timeout waiting for mail to arrive")

		mail.select("inbox")
		result, data = mail.uid('search', None, '(HEADER Subject "' + token + '")')

	uid = data[0]
	result, data = mail.uid('fetch', uid, '(RFC822)')
	raw_email = data[0][1]
	if debug:
		print raw_email
	# rm
	mail.uid('store', uid, '+FLAGS', r'(\Deleted)')
	mail.expunge()

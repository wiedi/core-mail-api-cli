#!/usr/bin/env python
import requests
import json

class MailAPI(object):
	def __init__(self, url, username=None, password=None, verify=True):
		self._url = url
		self._verify = verify
		self._username = username
		self._password = password
		
	def _req(self, verb, path, data = None, **kwargs):
		if data:
			kwargs['data'] = json.dumps(data)
			if 'headers' not in kwargs:
				kwargs['headers'] = {}
			kwargs['headers']['content-type'] = 'application/json'

		return requests.request(
			verb,
			url    = self._url + path,
			verify = self._verify,
			auth   = (self._username, self._password),
			**kwargs
		)

	# MailAccount
	#

	def createMailAccount(self, name, domain, password):
		return self._req('POST', 'mail/account/', data = {
			"name":     name,
			"domain":   domain,
			"password": password,
		}).json()

	def getMailAccount(self, name, domain):
		return self._req('GET', 'mail/account/' + name + '@' + domain + '/').json()
	
	def listMailAccounts(self, domain=None):
		return self._req('GET', 'mail/account/', params = {
			'page_size': 10000,
			'domain': domain,
		}).json()

	def setMailAccountPassword(self, name, domain, password):
		url = 'mail/account/' + name + '@' + domain + '/set_password/'
		return self._req('POST', url, data = {
			'password': password
		}).json()

	def disableMailAccountSubmission(self, name, domain):
		url = 'mail/account/' + name + '@' + domain + '/disable_submission/'
		return self._req('POST', url).json()

	def enableMailAccountSubmission(self, name, domain):
		url = 'mail/account/' + name + '@' + domain + '/enable_submission/'
		return self._req('POST', url).json()

	def setMailAccountSpoofingWhitelist(self, name, domain, spoofing_whitelist):
		url = 'mail/account/' + name + '@' + domain + '/set_spoofing_whitelist/'
		return self._req('POST', url, data = {
			"spoofing_whitelist": spoofing_whitelist,
		}).json()

	def deleteMailAccount(self, name, domain):
		return self._req('DELETE', 'mail/account/' + name + '@' + domain + '/').status_code

	# MailAlias
	#
	def createMailAlias(self, name, domain, to):
		return self._req('POST', 'mail/alias/', data = {
			"name":   name,
			"domain": domain,
			"to":     to,
		}).json()

	def getMailAlias(self, name, domain):
		return self._req('GET', 'mail/alias/' + name + '@' + domain + '/').json()
	
	def listMailAliases(self, domain=None):
		return self._req('GET', 'mail/alias/', params = {
			'page_size': 10000,
			'domain': domain,
		}).json()

	def updateMailAlias(self, name, domain, to):
		url = 'mail/alias/' + name + '@' + domain + '/'
		return self._req('POST', url, data = {
			'to': to
		}).json()

	def deleteMailAlias(self, name, domain):
		return self._req('DELETE', 'mail/alias/' + name + '@' + domain + '/').status_code


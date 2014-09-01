#!/usr/bin/env python

from lib.mailapi import MailAPI
from lib import mail
from config import CONFIG
import unittest
import random
import string



PASS = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))


class BasicTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		api = MailAPI(CONFIG['api_server'],
			username = CONFIG['api_username'],
			password = CONFIG['api_password'],
			verify   = CONFIG['api_verify_ssl'],
		)
		api.createMailAccount('acc1', CONFIG['test_domain'], PASS)
		api.createMailAccount('acc2', CONFIG['test_domain'], PASS)
		api.createMailAccount('acc3', CONFIG['test_domain'], PASS)
		
		api.createMailAccount('acc-and-alias', CONFIG['test_domain'], PASS)
		
		api.createMailAlias('alias1', CONFIG['test_domain'], 'acc1@' + CONFIG['test_domain'])
		api.createMailAlias('alias2', CONFIG['test_domain'], 'acc1@' + CONFIG['test_domain'] + ',acc2@' + CONFIG['test_domain'])
		api.createMailAlias('alias3', CONFIG['test_domain'],
			'acc1@'   + CONFIG['test_domain'] + ',' + \
			'alias2@' + CONFIG['test_domain'] + ',' + \
			'acc3@'   + CONFIG['test_domain'] + ','
		)
		
		external_addresses = ','.join([e['username'] for e in CONFIG['external']])
		api.createMailAlias('alias4', CONFIG['test_domain'], external_addresses)
		api.createMailAlias('alias5', CONFIG['test_domain'], 'alias5@' + CONFIG['test_domain'])
		
		api.createMailAlias('acc-and-alias', CONFIG['test_domain'], 'acc1@' + CONFIG['test_domain'])

	@classmethod
	def tearDownClass(cls):
		api = MailAPI(CONFIG['api_server'],
			username = CONFIG['api_username'],
			password = CONFIG['api_password'],
			verify   = CONFIG['api_verify_ssl'],
		)
		api.deleteMailAccount('acc1', CONFIG['test_domain'])
		api.deleteMailAccount('acc2', CONFIG['test_domain'])
		api.deleteMailAccount('acc3', CONFIG['test_domain'])

		api.deleteMailAlias('alias1', CONFIG['test_domain'])
		api.deleteMailAlias('alias2', CONFIG['test_domain'])
		api.deleteMailAlias('alias3', CONFIG['test_domain'])
		api.deleteMailAlias('alias4', CONFIG['test_domain'])
		api.deleteMailAlias('alias5', CONFIG['test_domain'])


	def test_send_to_account(self):
		token = mail.send(
			to       = ['acc1@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc1@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)

	def test_send_to_alias(self):
		token = mail.send(
			to        = ['alias1@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc1@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)
	
	def test_send_to_many(self):
		token = mail.send(
			to        = ['alias1@' + CONFIG['test_domain'], 'acc2@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc1@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc2@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)
	
	def test_send_to_alias_with_mulitple_destinations(self):
		token = mail.send(
			to        = ['alias2@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc1@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc2@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)

	def test_send_to_alias_with_same_named_account(self):
		token = mail.send(
			to        = ['acc-and-alias@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc1@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc-and-alias@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)



	def test_send_indirect_double_via_alias(self):
		token = mail.send(
			to        = ['alias3@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc1@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc2@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)
		mail.waitformail(
			token    = token,
			server   = CONFIG['mailbox_server'],
			port     = "993",
			user     = 'acc3@' + CONFIG['test_domain'],
			password = PASS,
			debug    = CONFIG['debug'],
			ssl      = True,
		)

	def test_alias_to_external(self):
		token = mail.send(
			to        = ['alias4@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)
		for ext in CONFIG['external']:
			mail.waitformail(
				token    = token,
				server   = ext['mailbox_server'],
				port     = ext['mailbox_port'],
				user     = ext['username'],
				password = ext['password'],
				debug    = CONFIG['debug'],
				ssl      = True,
			)

	def test_alias_loop(self):
		token = mail.send(
			to        = ['alias5@' + CONFIG['test_domain']],
			from_addr = 'acc1@' + CONFIG['test_domain'],
			server    = CONFIG['submission_server'],
			port      = '587',
			user      = 'acc1@' + CONFIG['test_domain'],
			password  = PASS,
			debug     = CONFIG['debug'],
			ssl       = True
		)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
	unittest.TextTestRunner(verbosity=2).run(suite)

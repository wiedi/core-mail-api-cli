#!/usr/bin/env python
from lib.mailapi import MailAPI
import argparse
import json

def print_result(res):
	for k, v in res.items():
		print("{:>20}: {:<80}".format(k, v))

def api(args):
	return MailAPI(args.server, args.api_username, args.api_password, verify=(not args.insecure))

def create(args):
	name, domain = args.email.split('@')
	res = api(args).createMailAccount(name, domain, args.password)
	print_result(res)

def show(args):
	name, domain = args.email.split('@')
	res = api(args).getMailAccount(name, domain)
	print_result(res)
	
def list(args):
	res = api(args).listMailAccounts(args.domain)
	keys = ['id', 'submission_disabled', 'spoofing_whitelist']
	row_format	= "{:>48} {:>2} {:<60}"
	print(row_format.format(*keys))
	for row in res['results']:
		print(row_format.format(*[row[k] for k in keys]))
	pass

def set_password(args):
	name, domain = args.email.split('@')
	res = api(args).setMailAccountPassword(name, domain, args.password)
	print_result(res)

def disable_submission(args):
	name, domain = args.email.split('@')
	res = api(args).disableMailAccountSubmission(name, domain)
	print_result(res)

def enable_submission(args):
	name, domain = args.email.split('@')
	res = api(args).enableMailAccountSubmission(name, domain)
	print_result(res)

def set_spoofing_whitelist(args):
	name, domain = args.email.split('@')
	res = api(args).setMailAccountSpoofingWhitelist(name, domain, args.spoofing_whitelist)
	print_result(res)

def delete(args):
	name, domain = args.email.split('@')
	res = api(args).deleteMailAccount(name, domain)
	print(res)
	
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--server', '-s', action="store", help='API-Server [http://localhost:8000/]', default='http://localhost:8000/')
	parser.add_argument('--api-username', '-u', action="store", help='API Username [admin]', default='admin')
	parser.add_argument('--api-password', '-p', action="store", help='API Password', default='')
	parser.add_argument('--insecure',     '-k', action="store_true", help='Ignore invalid SSL Certificates [false]', default=False)
	subparsers = parser.add_subparsers(help='commands', dest='cmd')
	subparsers.required = True

	# create
	create_parser = subparsers.add_parser('create', help='Create new Mail Account')
	create_parser.add_argument('email',	   action='store', help='Email address')
	create_parser.add_argument('password', action='store', help='Password')
	create_parser.set_defaults(func=create)

	# show
	show_parser = subparsers.add_parser('show', help='Show Mail Account details')
	show_parser.add_argument('email', action='store', help='Email address')
	show_parser.set_defaults(func=show)

	# list
	list_parser = subparsers.add_parser('list', help='List all count-jobs')
	list_parser.add_argument('--domain', '-d', action='store', help='Domain')
	list_parser.set_defaults(func=list)
	
	# set_password
	set_password_parser = subparsers.add_parser('set_password', help='Set Password')
	set_password_parser.add_argument('email',    action='store', help='Email address')
	set_password_parser.add_argument('password', action='store', help='Password')
	set_password_parser.set_defaults(func=set_password)
	
	# disable_submission
	disable_submission_parser = subparsers.add_parser('disable_submission', help='Disable Submission')
	disable_submission_parser.add_argument('email', action='store', help='Email address')
	disable_submission_parser.set_defaults(func=disable_submission)

	# enable_submission
	enable_submission_parser = subparsers.add_parser('enable_submission', help='Enable Submission')
	enable_submission_parser.add_argument('email', action='store', help='Email address')
	enable_submission_parser.set_defaults(func=enable_submission)

	# set_spoofing_whitelist
	set_spoofing_whitelist_parser = subparsers.add_parser('set_spoofing_whitelist', help='Set Spoofing Whitelist')
	set_spoofing_whitelist_parser.add_argument('email', action='store', help='Email address')
	set_spoofing_whitelist_parser.add_argument('spoofing_whitelist', action='store', help='Spoofing Whitelist')
	set_spoofing_whitelist_parser.set_defaults(func=set_spoofing_whitelist)

	# delete
	delete_parser = subparsers.add_parser('delete', help='Delete Mail Account')
	delete_parser.add_argument('email', action='store', help='Email address')
	delete_parser.set_defaults(func=delete)

	return parser.parse_args()

def main():
	args = parse_args()
	args.func(args)

if __name__ == '__main__':
	main()
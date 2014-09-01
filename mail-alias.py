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
	res = api(args).createMailAlias(name, domain, args.to)
	print_result(res)

def show(args):
	name, domain = args.email.split('@')
	res = api(args).getMailAlias(name, domain)
	print_result(res)
	
def list(args):
	res = api(args).listMailAliases(args.domain)
	keys = ['id', 'to',]
	row_format	= "{:>48} {:<80}"
	print(row_format.format(*keys))
	for row in res['results']:
		print(row_format.format(*[row[k] for k in keys]))
	pass

def update(args):
	name, domain = args.email.split('@')
	res = api(args).updateMailAlias(name, domain, args.to)
	print_result(res)

def delete(args):
	name, domain = args.email.split('@')
	res = api(args).deleteMailAlias(name, domain)
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
	create_parser = subparsers.add_parser('create', help='Create new Mail Alias')
	create_parser.add_argument('email', action='store', help='Email address')
	create_parser.add_argument('to',    action='store', help='To')
	create_parser.set_defaults(func=create)

	# show
	show_parser = subparsers.add_parser('show', help='Show Mail Alias details')
	show_parser.add_argument('email', action='store', help='Email address')
	show_parser.set_defaults(func=show)

	# list
	list_parser = subparsers.add_parser('list', help='List all count-jobs')
	list_parser.add_argument('--domain', '-d', action='store', help='Domain')
	list_parser.set_defaults(func=list)

	# update
	update_parser = subparsers.add_parser('update', help='Update Alias')
	update_parser.add_argument('email', action='store', help='Email address')
	update_parser.add_argument('to',    action='store', help='to')
	update_parser.set_defaults(func=update)

	# delete
	delete_parser = subparsers.add_parser('delete', help='Delete Mail Alias')
	delete_parser.add_argument('email', action='store', help='Email address')
	delete_parser.set_defaults(func=delete)

	return parser.parse_args()

def main():
	args = parse_args()
	args.func(args)

if __name__ == '__main__':
	main()
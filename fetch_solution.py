import requests
import dotenv
import pickle
import re
import argparse
import pathlib

dir = pathlib.Path(__file__).parent

def get_cookies(url, data):
	try:
		with open(dir / 'cookies', 'rb') as f:
			cookies = pickle.load(f)
			return cookies or fetch_cookies(url, data)
	except: return fetch_cookies(url, data)

def fetch_cookies(url, data):
	print('Signing in...')
	res = requests.post(url, data=data)
	
	if res.status_code != 200:
		print("Couldn't sign in...")
		exit()

	cookies = res.cookies
	with open(dir / 'cookies', 'wb') as f:
		pickle.dump(cookies, f)
	return cookies

def print_measurements(text, verbose=False):
	output = ''
	error = ''
	for line in text.split('\n'):
		if 'h3' in line and 'measurements' in line:
			output += f"solution: {line.split('&nbsp;')[1]}\n"

		elif verbose and '@' in line and 'script' not in line:
			for x in re.split('<|>', line):
				if '@' in x:
					output += f'x\n'
		elif 'error' in line:
			error += f'{line}\n'

	print(output or error, end='')

if __name__ == '__main__':

	a = argparse.ArgumentParser()
	a.add_argument('--verbose', action='store_true')
	a.add_argument('sysconfig')
	a.add_argument('commands')

	args = a.parse_args()
	
	# files
	try:
		sysconfig, commands = [open(f, 'r').read() for f in (args.sysconfig, args.commands)]
	except:
		print('Cannot open files')
		exit()

	# credentials
	env = dotenv.dotenv_values(dir / '.env')
	
	url = env['url']

	data = {
		'tryuwaid': env['username'],
		'trypassword': env['password'],
		'trylogin': 'y',
		'run-sample': ' run-sample '
	}

	cookies = get_cookies(url, data)

	files = {
		'file-sysconfig': ('sysconfig.txt', sysconfig),
		'file-commands': ('commands.txt', commands),
	}

	res = requests.post(url, files=files, data=data, cookies=cookies)
	if res.status_code == 200:
		print_measurements(res.text, verbose=args.verbose)
	else:
		print("Couldn't fetch solution")
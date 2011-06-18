#! /usr/bin/python
#
# Simple WINE menu creator

import sys
import os
import stat
import getopt

from printer import *

''' Class for menu information about either a WINE program or directory '''
class MenuEntry:
	def __init__(self):
		self.name = ''
		self.cmd = ''
		self.entries = []

	''' Returns TRUE if is leaf '''
	def is_leaf(self):
		return not self.entries

def read_desktop_file(entry, path):
	''' Reads application info

		Arguments:
		root = MenuEntry to put information in
		path = Absolute path to file
	'''
	
	with open(path) as f:
		for line in f:
			s = line.split('=', 1)

			if len(s) == 2:	
				if s[0] == "Name":
					entry.name = s[1].rstrip('\n')
				elif s[0] == "Exec":
					entry.cmd = s[1].rstrip('\n')

def create_menu(root, path):
	''' Recursively reads a given directory for .desktop files

		Arguments:
		root = MenuEntry that represents the root in the tree
		path = Absolute path to directory
	'''

	# TODO handle exceptions

	files = os.listdir(path)

	for f in files:
		buf = os.path.join(path, f)
		st = os.lstat(buf)
		
		ent = MenuEntry()
		root.entries.append(ent)
		
		if stat.S_ISDIR(st.st_mode):
			ent.name = f
			create_menu(ent, buf)
		elif buf.endswith('.desktop'):
			read_desktop_file(ent, buf)

def usage(cmd):
	''' Print program usage information '''
	
	print('Usage:', cmd, '[OPTIONS]...')
	print()
	print('Mandatory arguments to long options are mandatory for short options too.')
	print()
	print('-h, --help      print this message.')
	print('-f, --format    select format (see format list below).')
	print()
	print('Format list')
	print(' plain          Plain menu format')
	print(' awesome        Awesome Window Manager')
	print()

def main(argv = None):
	if argv is None:
		argv = sys.argv

	cmd = argv[0]

	try:
		opts, argv = getopt.getopt(argv[1:], 'f:h', [ 'help', 'format=' ])
	except getopt.GetoptError as e:
		print(e)
		usage(cmd)
		sys.exit()

	printer = None

	for o, a in opts:
		if o in ('-h', '--help'):
			usage(cmd)
			sys.exit()
		elif o in ('-f', '--format'):
			if a == 'awesome':
				printer = AwesomePrinter()
			elif not (a == 'plain'):
				print('unknown choice for', o)
				sys.exit()

	''' Get absolute path for WINE applications directory '''
	path = os.path.expanduser('~/.local/share/applications/wine/Programs')

	root = MenuEntry()
	root.name = "Wine"

	create_menu(root, path)

	if not printer:
		printer = Printer()

	printer.print_menu(root)

if __name__ == "__main__":
	main()

import hashlib

''' Base class for menu printers '''
class Printer:
	def print_menu(self, entry, lvl = 0):
		print_space(lvl)

		if not entry.is_leaf():
			print(entry.name, "{")
			for e in entry.entries:
				self.print_menu(e, lvl + 1)
			print_space(lvl)
			print("}")
		else:
			print(entry.name, entry.cmd)

''' Printer class for Awesome Window Manager '''
class AwesomePrinter(Printer):
	''' Print menu '''
	def print_menu(self, entry, lvl = 0):
		if not entry.is_leaf():
			for e in entry.entries:
				self.print_menu(e, lvl + 1)

			print(self.create_ref(entry.name), '=', '{')
			
			stop = len(entry.entries) - 1
			i = 0

			while i <= stop:
				e = entry.entries[i]

				self.print_item(e, i == stop)
				i += 1
			print("}")
			print()

	''' Print menu string '''
	def print_item(self, entry, last):
		if entry.is_leaf():
			self.print_leaf(entry, last)
		else:
			self.print_dir(entry, last)

	''' Print program menu string '''
	def print_leaf(self, entry, last):
		''' Escape " and ' '''
		name = entry.name.replace('\'', '\\\'').replace('\"', '\\\"')
		cmd = entry.cmd.replace('\'', '\\\'').replace('\"', '\\\"')

		e = '" }'
		if last == False:
			e += ','
		print('   {"', name, '", "', cmd, e, sep='')

	''' Print directory menu string '''
	def print_dir(self, entry, last):
		name = entry.name.replace('\'', '\\\'').replace('\"', '\\\"')
		
		e = '}'
		if last == False:
			e += ','
		print('   {"', name, '", ', self.create_ref(name), e, sep='')

	''' Create a MD5 checksum menu name '''
	def create_ref(self, name):
		return "menu_" +  hashlib.md5(name.encode('UTF-8')).hexdigest()

def print_space(x):
	''' Print x number of spaces, without newline at the end '''

	while x > 0:
		print(' ', end='')
		x = x - 1

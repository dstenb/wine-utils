import hashlib


class Printer:
    ''' Base class for menu printers '''
    def print_menu(self, entry, lvl=0):
        if not entry.is_leaf():
            print("%s%s {" % (" " * lvl, entry.name))
            for e in entry.entries:
                self.print_menu(e, lvl + 1)
            print("%s}" % " " * lvl)
        else:
            print("%s%s %s" % (" " * lvl, entry.name, entry.cmd))


class AwesomePrinter(Printer):
    ''' Printer class for Awesome Window Manager '''

    ''' Print menu '''
    def print_menu(self, entry, lvl=0):
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
        return "menu_" + hashlib.md5(name.encode('UTF-8')).hexdigest()


class PekWMPrinter:
    ''' Printer class for PekWM Window Manager '''

    def __init__(self, dynamic):
        self.dynamic = dynamic

    def print_menu(self, entry, lvl=0):
        name = entry.name.replace('\'', '\\\'').replace('\"', '\\\"')

        if not entry.is_leaf():
            if lvl == 0 and self.dynamic:
                print("%sDynamic = \"%s\" {" % ("\t" * lvl, name))
            else:
                print("%sSubmenu = \"%s\" {" % ("\t" * lvl, name))
            for e in entry.entries:
                self.print_menu(e, lvl + 1)
            print("\t" * lvl, "}", sep="")
        else:
            cmd = entry.cmd.replace('\'', '\\\'').replace('\"', '\\\"')
            print("%sEntry = \"%s\" { Actions = \"Exec %s &\" }" % (
                "\t" * lvl, name, cmd))

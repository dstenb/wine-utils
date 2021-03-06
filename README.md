# WINE Menu Creator

WINE Menu Creator is a simple script that generates WINE menus for various
window managers and other utilities.

The script currently supports

* Awesome WM
* PekWM

## Formats

### awesome - Awesome Window Manager
To keep the rc.lua configuration file clean the WINE menu can be placed in
another lua file and imported with the 'require' command, and added to the
default menu as follows

    mymainmenu = awful.menu({ items = { { "awesome", myawesomemenu, beautiful.awesome_icon },
        { "open terminal", terminal },
        { "wine", menu_b9eadba3c35f7f89e93c92eb2c8d39b0 }
        }
    })

### pekwm - PekWM Window Manager
Static menu that should be included in ~/.pekwm/menu

### pekwm-dynamic - Dynamic PekWM Window Manager
Dynamic menu that is reloaded every time it's selected.
This is way more flexible than the normal menu.
The dynamic menu can be included in ~/.pekwm/menu as

    Submenu = "WINE" {
        Entry { Actions = "Dynamic /home/david/code/wine-utils/wine-menu-creator/main.py -f pekwm-dynamic" }
    }

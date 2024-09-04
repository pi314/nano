import sys
import os
import shutil


import smol


def main():
    if not sys.stdin.isatty():
        items = [line for line in sys.stdin]
    else:
        items = os.listdir('.')

    items.sort()

    print(shutil.get_terminal_size())

    def onkey(menu, cursor, key):
        if key == 'j':
            return 'down'
        if key == 'k':
            return 'up'
        if key == 'H':
            return 'home'
        if key == 'L':
            return 'end'
        if key in ('0', '^'):
            return 'home'
        if key in ('G', '$'):
            return 'end'

        if key == 'd':
            menu.cursor = 'default'
        elif key == 'r':
            menu.cursor = 'radio'
        elif key == 'c':
            menu.cursor = 'checkbox'

    menu = smol.tui.Menu('Select menu type:', options=['default', 'radio', 'checkbox'], onkey=onkey, wrap=True)
    menu_type = menu.interact()
    print(menu_type)
    print()

    if menu_type is None:
        return

    def onkey(menu, cursor, key):
        if key == 'j':
            return 'down'
        if key == 'k':
            return 'up'
        if key == 'H':
            return 'home'
        if key == 'L':
            return 'end'
        if key in ('0', '^'):
            return 'home'
        if key in ('G', '$'):
            return 'end'

        if key == '\x04':
            menu.message = 'DwD'
            return False

        if key == '\x01':
            menu.message = 'AwA'
            return False

        if key == chr(ord('u') - ord('a') + 1):
            menu.message = 'UwU'
            return False

        if key == 'tab':
            menu.message = 'TwT'
            return False

        if key == 'enter':
            if not menu.type:
                return None

            if not cursor.selected:
                cursor.select()
            else:
                menu.done()

            return False

        if key == 'c':
            menu.unselect_all()
            return False

        if key == 'a':
            menu.select_all()
            return False

        if key == 'd':
            menu.cursor = 'Done'

    if menu_type == 'checkbox':
        meta_options = ['Select all', 'Unselect all'] + items + ['Done']
    else:
        meta_options = items

    menu = smol.tui.Menu('Select one you like:', options=meta_options, type=menu_type, onkey=onkey, wrap=True)

    if menu_type == 'checkbox':
        menu[0].set_meta(
                mark=lambda menu: {
                    len(items): '*',
                    0: ' '
                    }.get(sum(item.selected for item in menu if not item.is_meta), '-')
                )
        def select_all_onkey(menu, cursor, key):
            if key == 'space':
                menu.select_all()
                menu.cursor.color = smol.black / smol.green
                return False
        menu[0].onkey = select_all_onkey

        def unselect_all_onkey(menu, cursor, key):
            if key == 'space':
                menu.unselect_all()
                menu.cursor.color = smol.black / smol.red
                return False

        menu[1].set_meta(
                mark=lambda menu: {
                    len(items): ' ',
                    0: '*'
                    }.get(sum(item.selected for item in menu if not item.is_meta), '-'),
                onkey=unselect_all_onkey)

        menu[-1].set_meta(mark=lambda menu: '>' if menu.cursor == 'Done' else ' ')
        menu[-1].arrow = ' '
        def done_onkey(menu, cursor, key):
            if key == 'space':
                menu.cursor = '.gitignore'
                menu.cursor.color = smol.black / smol.white
                return False
            if key == 'enter':
                menu.done()
        menu[-1].onkey = done_onkey

    ret = menu.interact()
    if isinstance(ret, tuple):
        print('You selected:', '(', ret[0], ')')
    elif isinstance(ret, list):
        print('You selected:', '[', ', '.join(ret), ']')
    else:
        print('You selected:', ret)


if __name__ == '__main__':
    main()

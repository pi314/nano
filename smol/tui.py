import contextlib
import itertools
import sys
import threading
import time

from .paints import paint


__all__ = ['ThreadedSpinner', 'prompt']


class ThreadedSpinner:
    def __init__(self, *icon, delay=0.1):
        if not icon:
            self.icon_entry = '⠉⠛⠿⣿⠿⠛⠉⠙'
            self.icon_loop = '⠹⢸⣰⣤⣆⡇⠏⠛'
            self.icon_leave = '⣿'
        elif isinstance(icon, str):
            self.icon_entry = tuple()
            self.icon_loop = [icon]
            self.icon_leave = '.'
        elif len(icon) == 1:
            self.icon_entry = tuple()
            self.icon_loop = icon
            self.icon_leave = '.'
        elif len(icon) == 2:
            self.icon_entry = icon[0]
            self.icon_loop = icon[1]
            self.icon_leave = '.'
        elif len(icon) == 3:
            self.icon_entry = icon[0]
            self.icon_loop = icon[1]
            self.icon_leave = icon[2]
        else:
            raise ValueError('Invalid value: ' + repr(icon))

        if not isinstance(self.icon_leave, str):
            raise ValueError('Icon[leave] needs to be a single string')

        self.delay = delay
        self.is_end = False
        self.thread = None
        self._text = ''
        self.icon_iter = (
                itertools.chain(
                    self.icon_entry,
                    itertools.cycle(self.icon_loop)
                    ),
                iter(self.icon_leave)
                )
        self.icon_head = [None, None]

        self.print_function = print

    def __enter__(self):
        if self.thread:
            return self

        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    @property
    def icon(self):
        idx = self.is_end
        if self.icon_head[idx] is None:
            self.icon_head[idx] = next(self.icon_iter[idx])
        return self.icon_head[idx]

    def text(self, *args):
        if not args:
            return self._text

        self._text = ' '.join(str(a) for a in args)
        if self.thread:
            self.refresh()

    def refresh(self):
        self.print_function('\r' + self.icon + '\033[K ' + self._text, end='')

    def animate(self):
        while not self.is_end:
            self.refresh()
            time.sleep(self.delay)
            self.icon_head[0] = next(self.icon_iter[0])

        try:
            while True:
                self.refresh()
                self.icon_head[1] = next(self.icon_iter[1])
                time.sleep(self.delay)
        except StopIteration:
            pass

        self.print_function()

    def start(self):
        if self.thread:
            return

        self.thread = threading.Thread(target=self.animate)
        self.thread.daemon = True
        self.thread.start()

    def end(self, wait=True):
        self.is_end = True
        if wait:
            self.join()

    def join(self):
        self.thread.join()


def alt_if_none(A, B):
    if A is None:
        return B
    return A


class UserSelection:
    def __init__(self, options, accept_cr=None, abbr=None, sep=None, ignorecase=None):
        if not options:
            accept_cr = True # carriage return
            abbr = False
            ignorecase = False

        self.accept_cr = alt_if_none(accept_cr, True)
        self.abbr = alt_if_none(abbr, True)
        self.ignorecase = alt_if_none(ignorecase, self.abbr)
        self.sep = alt_if_none(sep, ' / ')

        self.mapping = dict()
        self.options = [o for o in options]

        if self.options:
            if self.accept_cr:
                self.mapping[''] = self.options[0]

            for opt in self.options:
                for o in (opt,) + ((opt[0],) if self.abbr else tuple()):
                    self.mapping[o.lower() if self.ignorecase else o] = opt

        self.selected = None

    def select(self, o=''):
        if self.ignorecase:
            o = o.lower()

        if not self.options:
            self.selected = o
            return

        if o not in self.mapping:
            raise ValueError('Invalid option: ' + o)

        self.selected = o

    @property
    def prompt(self):
        if not self.options:
            return ''

        opts = [o for o in self.options]
        if self.accept_cr and self.ignorecase:
            opts[0] = opts[0].capitalize()

        if self.abbr:
            return ' [' + self.sep.join('({}){}'.format(o[0], o[1:]) for o in opts) + ']'
        else:
            return ' [' + self.sep.join(opts) + ']'

    def __eq__(self, other):
        if self.ignorecase and other is not None:
            other = other.lower()

        if self.selected == other:
            return True

        if self.selected in self.mapping:
            return self.mapping[self.selected] == self.mapping.get(other)

        return False

    def __str__(self):
        return self.selected

    def __repr__(self):
        return '<smol.tui.UserSelection selected=[{}]>'.format(self.selected)


def prompt(question, options=tuple(),
           accept_cr=None,
           abbr=None,
           ignorecase=None,
           sep=None,
           suppress=(EOFError, KeyboardInterrupt)):

    if isinstance(options, str) and ' ' in options:
        options = options.split()

    user_selection = UserSelection(options, accept_cr=accept_cr, abbr=abbr, sep=sep, ignorecase=ignorecase)

    class SingleUseContextManager:
        def __enter__(self):
            self.stdin_backup = sys.stdin
            self.stdout_backup = sys.stdout
            self.stderr_backup = sys.stderr

        def __exit__(self, exc_type, exc_value, traceback):
            sys.stdin = self.stdin_backup
            sys.stdout = self.stdout_backup
            sys.stderr = self.stderr_backup

    class ExceptionSuppressor:
        def __init__(self, *exc_group):
            if isinstance(exc_group[0], tuple):
                self.exc_group = exc_group[0]
            else:
                self.exc_group = exc_group

        def __enter__(self, *exc_group):
            pass

        def __exit__(self, exc_type, exc_value, traceback):
            if exc_type in (EOFError, KeyboardInterrupt):
                print()
            return exc_type in self.exc_group

    with SingleUseContextManager():
        sys.stdin = open('/dev/tty')
        sys.stdout = open('/dev/tty', 'w')
        sys.stderr = open('/dev/tty', 'w')

        with ExceptionSuppressor(suppress):
            while user_selection.selected is None:
                print((question + (user_selection.prompt)), end=' ')

                with contextlib.suppress(ValueError):
                    i = input().strip()
                    user_selection.select(i)

        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()

    return user_selection

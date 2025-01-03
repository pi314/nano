from .test_utils import *

from warawara import *


class TestColorFacade(TestCase):
    def test_color_facade(self):
        # arg unpack
        self.eq(color((208,)), color(208))
        self.eq(color([208]), color(208))
        self.eq(color((0xC0, 0xFF, 0xEE)), color('#C0FFEE'))
        self.eq(color([0xC0, 0xFF, 0xEE]), color('#C0FFEE'))

        # copy_ctor
        self.eq(color(color(208)), color(208))

        # subclass
        self.is_true(issubclass(Color256, Color))
        self.is_true(issubclass(ColorRGB, Color))

        # Color256
        orange = color(208)
        self.is_true(isinstance(orange, Color256))
        self.is_true(isinstance(orange, Color))

        # ColorRGB
        coffee = color((0xC0, 0xFF, 0xEE))
        self.is_true(isinstance(coffee, ColorRGB))
        self.is_true(isinstance(coffee, Color))

        # ColorRGB
        coffee = color('#C0FFEE')
        self.is_true(isinstance(coffee, ColorRGB))
        self.is_true(isinstance(coffee, Color))

    def test_color_invalid_value(self):
        with self.assertRaises(TypeError):
            color(True)

        with self.assertRaises(TypeError):
            Color256(True)

        with self.assertRaises(TypeError):
            ColorRGB(True)


class TestColorTrait(TestCase):
    def setUp(self):
        self.orange = color(208)
        self.coffee = color('#C0FFEE')

    def test_repr(self):
        self.eq(repr(self.orange), 'Color256(208)')
        self.eq(' '.join(repr(self.coffee).split()), 'ColorRGB(192, 255, 238)')

    def test_int(self):
        self.eq(int(self.orange), 208)
        self.eq(int(self.coffee), 0xC0FFEE)

    def test_fg(self):
        self.eq(self.orange('text'), '\033[38;5;208mtext\033[m')
        self.eq(self.coffee('text'), '\033[38;2;192;255;238mtext\033[m')
        self.eq(self.orange.fg('text'), '\033[38;5;208mtext\033[m')
        self.eq(self.coffee.fg('text'), '\033[38;2;192;255;238mtext\033[m')

    def test_bg(self):
        self.eq(self.orange.bg('text'), '\033[48;5;208mtext\033[m')
        self.eq(self.coffee.bg('text'), '\033[48;2;192;255;238mtext\033[m')

    def test_str(self):
        self.eq(str(self.orange), '\033[38;5;208m')
        self.eq(str(self.coffee), '\033[38;2;192;255;238m')

    def test_invert(self):
        self.eq(str(~self.orange), '\033[48;5;208m')
        self.eq(str(~self.coffee), '\033[48;2;192;255;238m')
        self.is_true(isinstance(~self.orange, paint))
        self.is_true(isinstance(~self.coffee, paint))

    def test_div(self):
        self.eq(self.orange / self.coffee, paint(fg=self.orange, bg=self.coffee))

        with self.assertRaises(TypeError):
            self.orange / 1

    def test_or(self):
        self.eq(nocolor | self.coffee, self.coffee)
        self.eq(self.orange | self.coffee, self.orange)


class TestColor256(TestCase):
    def test_color256_code(self):
        for i in range(256):
            self.eq(color(i).code, i)

    def test_color256_to_rgb(self):
        self.eq(color(0).to_rgb(), ColorRGB(0x00, 0x00, 0x00))
        self.eq(color(1).to_rgb(), ColorRGB(0x80, 0x00, 0x00))
        self.eq(color(2).to_rgb(), ColorRGB(0x00, 0x80, 0x00))
        self.eq(color(3).to_rgb(), ColorRGB(0x80, 0x80, 0x00))
        self.eq(color(4).to_rgb(), ColorRGB(0x00, 0x00, 0x80))
        self.eq(color(5).to_rgb(), ColorRGB(0x80, 0x00, 0x80))
        self.eq(color(6).to_rgb(), ColorRGB(0x00, 0x80, 0x80))
        self.eq(color(7).to_rgb(), ColorRGB(0xC0, 0xC0, 0xC0))
        self.eq(color(8).to_rgb(), ColorRGB(0x80, 0x80, 0x80))
        self.eq(color(9).to_rgb(), ColorRGB(0xFF, 0x00, 0x00))
        self.eq(color(10).to_rgb(), ColorRGB(0x00, 0xFF, 0x00))
        self.eq(color(11).to_rgb(), ColorRGB(0xFF, 0xFF, 0x00))
        self.eq(color(12).to_rgb(), ColorRGB(0x00, 0x00, 0xFF))
        self.eq(color(13).to_rgb(), ColorRGB(0xFF, 0x00, 0xFF))
        self.eq(color(14).to_rgb(), ColorRGB(0x00, 0xFF, 0xFF))
        self.eq(color(15).to_rgb(), ColorRGB(0xFF, 0xFF, 0xFF))
        self.eq(color(208).to_rgb(), ColorRGB(0xFF, 0x87, 0x00))
        self.eq(color(232).to_rgb(), ColorRGB(0x08, 0x08, 0x08))
        self.eq(color(237).to_rgb(), ColorRGB(0x3A, 0x3A, 0x3A))


class TestColorRGB(TestCase):
    def test_rgb_empty(self):
        self.eq(ColorRGB().seq, '')

    def test_rgb(self):
        some_color = ColorRGB(160, 90, 0)
        self.eq(some_color.r, 160)
        self.eq(some_color.g, 90)
        self.eq(some_color.b, 0)
        self.eq(int(some_color), 0xA05A00)

    def test_value_range_check(self):
        with self.assertRaises(TypeError):
            ColorRGB(300, 300, 300)

    def test_rgb_mul(self):
        some_color = ColorRGB(160, 90, 0) * 2
        self.eq(some_color.r, 320)
        self.eq(some_color.g, 180)
        self.eq(some_color.b, 0)

        some_color = ColorRGB(160, 90, 0) * 0.8
        self.eq(str(some_color), '\033[38;2;128;72;0m')

    def test_rgb_div(self):
        some_color = ColorRGB(160, 90, 0) // 2
        self.eq(some_color, ColorRGB(80, 45, 0))

    def test_rgb_overflow(self):
        some_color = ColorRGB(160, 90, 0) * 2
        self.eq(str(some_color), '\033[38;2;255;180;0m')
        self.eq(int(some_color), 0xFFB400)

    def test_rgb_average(self):
        d_red = ColorRGB(255, 0, 0) * 2
        self.eq(d_red.r, 255 * 2)
        self.eq(d_red.g, 0)
        self.eq(d_red.b, 0)

        d_green = ColorRGB(0, 255, 0) * 2
        self.eq(d_green.r, 0)
        self.eq(d_green.g, 255 * 2)
        self.eq(d_green.b, 0)

        d_yellow = d_red + d_green
        self.eq(d_yellow.r, 255 * 2)
        self.eq(d_yellow.g, 255 * 2)
        self.eq(d_yellow.b, 0)

        yellow = d_yellow // 2
        self.eq(yellow, ColorRGB(255, 255, 0))


class TestBuiltInColors(TestCase):
    def test_nocolor(self):
        self.eq(nocolor(), '')
        self.eq(nocolor('text'), 'text')
        self.eq(str(nocolor), '\033[m')
        self.eq('{}'.format(nocolor), '\033[m')

    def test_str(self):
        self.eq(str(black),     '\033[38;5;0m')
        self.eq(str(maroon),    '\033[38;5;1m')
        self.eq(str(green),     '\033[38;5;2m')
        self.eq(str(olive),     '\033[38;5;3m')
        self.eq(str(navy),      '\033[38;5;4m')
        self.eq(str(purple),    '\033[38;5;5m')
        self.eq(str(teal),      '\033[38;5;6m')
        self.eq(str(silver),    '\033[38;5;7m')
        self.eq(str(grey),      '\033[38;5;8m')
        self.eq(str(red),       '\033[38;5;9m')
        self.eq(str(lime),      '\033[38;5;10m')
        self.eq(str(yellow),    '\033[38;5;11m')
        self.eq(str(blue),      '\033[38;5;12m')
        self.eq(str(fuchsia),   '\033[38;5;13m')
        self.eq(str(magenta),   '\033[38;5;13m')
        self.eq(str(cyan),      '\033[38;5;14m')
        self.eq(str(aqua),      '\033[38;5;14m')
        self.eq(str(white),     '\033[38;5;15m')
        self.eq(str(darkorange),'\033[38;5;208m')
        self.eq(str(murasaki),  '\033[38;5;135m')

    def test_invert(self):
        self.eq(~red,      paint(bg=red))
        self.eq(~green,    paint(bg=green))
        self.eq(~yellow,   paint(bg=yellow))
        self.eq(~blue,     paint(bg=blue))
        self.eq(~magenta,  paint(bg=magenta))
        self.eq(~cyan,     paint(bg=cyan))
        self.eq(~white,    paint(bg=white))
        self.eq(~orange,   paint(bg=orange))

    def test_call(self):
        self.eq(black('text'),     '\033[38;5;0mtext\033[m')
        self.eq(maroon('text'),    '\033[38;5;1mtext\033[m')
        self.eq(green('text'),     '\033[38;5;2mtext\033[m')
        self.eq(olive('text'),     '\033[38;5;3mtext\033[m')
        self.eq(navy('text'),      '\033[38;5;4mtext\033[m')
        self.eq(purple('text'),    '\033[38;5;5mtext\033[m')
        self.eq(teal('text'),      '\033[38;5;6mtext\033[m')
        self.eq(silver('text'),    '\033[38;5;7mtext\033[m')
        self.eq(grey('text'),      '\033[38;5;8mtext\033[m')
        self.eq(red('text'),       '\033[38;5;9mtext\033[m')
        self.eq(lime('text'),      '\033[38;5;10mtext\033[m')
        self.eq(yellow('text'),    '\033[38;5;11mtext\033[m')
        self.eq(blue('text'),      '\033[38;5;12mtext\033[m')
        self.eq(fuchsia('text'),   '\033[38;5;13mtext\033[m')
        self.eq(magenta('text'),   '\033[38;5;13mtext\033[m')
        self.eq(cyan('text'),      '\033[38;5;14mtext\033[m')
        self.eq(aqua('text'),      '\033[38;5;14mtext\033[m')
        self.eq(white('text'),     '\033[38;5;15mtext\033[m')
        self.eq(darkorange('text'),'\033[38;5;208mtext\033[m')
        self.eq(murasaki('text'),  '\033[38;5;135mtext\033[m')


class TestPaint(TestCase):
    def test_repr(self):
        self.is_true(repr(paint()).startswith('ColorCompound'))

    def test_or(self):
        self.eq(black | (~yellow), paint(fg=0, bg=11))

    def test_div(self):
        ry = red / yellow
        bg = blue / green
        rybg = ry / bg
        self.eq(rybg, paint(fg=red, bg=blue))
        self.eq(rybg('text'), f'\033[38;5;9;48;5;12mtext\033[m')

    def test_invert(self):
        ry = red / yellow
        bg = blue / green
        rybg = ry / bg
        self.eq(~rybg, paint(fg=blue, bg=red))
        self.eq((~rybg)('text'), '\033[38;5;12;48;5;9mtext\033[m')


class TestDecolor(TestCase):
    def test_decolor(self):
        self.eq(decolor(orange('test')), 'test')
        self.eq(decolor('\033[1;31mred\033[m'), 'red')


class TestGradient(TestCase):
    def test_invalid_values(self):
        with self.assertRaises(TypeError):
            gradient(True, False)

        A = color()
        B = color()

        with self.assertRaises(TypeError):
            gradient(A, B, 1.5)

        with self.assertRaises(ValueError):
            gradient(A, B, 1)

    def test_trivial(self):
        # N=2 trivial case
        A = color(39)
        B = color(214)
        self.eq(gradient(A, B, 2), (A, B))

        # Color256() and ColorRGB() case
        A = color(39)
        B = color('#C0FFEE')
        self.eq(gradient(A, B), (A, B))

        # Color256() rgb6 and gray case
        A = color(39)
        B = color(255)
        self.eq(gradient(A, B), (A, B))

    def test_color256_gray(self):
        A = color(235)
        B = color(245)

        # default length
        res = gradient(A, B)
        ans = tuple(range(235, 246))
        self.eq(res, tuple(map(color, ans)))

        # shorter length
        res = gradient(A, B, N=5)
        ans = (235, 238, 241, 243, 245)
        self.eq(res, tuple(map(color, ans)))

        # longer length
        res = gradient(A, B, N=15)
        ans = (235, 235, 236, 236, 237, 237, 238, 238, 239, 240, 241, 242, 243, 244, 245)
        self.eq(res, tuple(map(color, ans)))


    def test_color256_rgb(self):
        A = color(39)
        B = color(214)

        # default length
        res = gradient(A, B)
        ans = (39 ,74 ,109 ,144 ,179 ,214)
        self.eq(res, tuple(map(color, ans)))

        # shorter length
        res = gradient(A, B, N=4)
        ans = (39, 109, 179, 214)
        self.eq(res, tuple(map(color, ans)))

        # longer length
        res = gradient(A, B, N=15)
        ans = (39, 39, 39, 74, 74, 74, 109, 109, 109, 144, 144, 179, 179, 214, 214)
        self.eq(res, tuple(map(color, ans)))

    def test_rgb(self):
        A = color(242, 5, 148)
        B = color(146, 219, 189)

        # default length
        res = gradient(A, B)
        ans = (ColorRGB(242, 5, 148),
               ColorRGB(204, 35, 237),
               ColorRGB(110, 64, 232),
               ColorRGB(93, 132, 228),
               ColorRGB(120, 208, 223),
               ColorRGB(146, 219, 189))

        self.eq(res, ans)

        # shorter length
        res = gradient(A, B, N=4)
        ans = (color(242, 5, 148),
               color(137, 55, 234),
               color(102, 161, 226),
               color(146, 219, 189))
        self.eq(res, tuple(map(color, ans)))

        # longer length
        res = gradient(A, B, N=15)
        ans = (ColorRGB(242, 5, 148),
               ColorRGB(240, 16, 196),
               ColorRGB(237, 26, 238),
               ColorRGB(196, 37, 237),
               ColorRGB(159, 48, 235),
               ColorRGB(127, 58, 233),
               ColorRGB(100, 69, 232),
               ColorRGB(79, 80, 230),
               ColorRGB(89, 118, 228),
               ColorRGB(99, 151, 227),
               ColorRGB(108, 179, 225),
               ColorRGB(118, 203, 223),
               ColorRGB(127, 222, 221),
               ColorRGB(136, 220, 203),
               ColorRGB(146, 219, 189),)
        self.eq(res, ans)

        A = color('#FF1100')
        B = color('#FF0011')
        res = gradient(A, B, N=3)
        self.eq(res, (A, color('#FF0000'), B))

        A = color('#FF0011')
        B = color('#FF1100')
        res = gradient(A, B, N=3)
        self.eq(res, (A, color('#FF0000'), B))

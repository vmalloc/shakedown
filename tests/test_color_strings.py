import colorama
from .utils import TestCase
from slash.utils.color_string import ColorString, ColorStringBase


class ColoredStringTest(TestCase):

    def test_colored_string(self):
        orig = "some string"
        colored = ColorString(orig, 'red')
        self.assertEqual(str(orig), str(colored))
        self.assertEqual(repr(orig), repr(colored))
        self.assertEqual(
            colored.get_colored(), colorama.Fore.RED + orig + colorama.Fore.RESET)

    def test_get_formatter(self):
        f = ColorString.get_formatter("red")
        self.assert_colored(
            f("test"), colorama.Fore.RED + "test" + colorama.Fore.RESET, "test")

    def test_transformations(self):
        for modifier in [
                (lambda s: s.ljust(20)),
        ]:
            self.assertEqual(modifier(ColorString("string", "red")).get_colored(),
                              ColorString(modifier("string"), "red").get_colored())

    def test_len(self):
        for x in ["test", "me", "here!!!"]:
            self.assertEqual(len(ColorString(x, "red")), len(x))

        self.assertEqual(len("hello" + ColorString(" there", "red")), len("hello there"))

    def test_formatting(self):
        orig = "value1=%s, value2=%s"
        values = (6, 7)
        orig_formatted = orig % values
        colored = ColorString(orig, 'red')
        colored_formatted = colored % values
        self.assert_colored(
            colored_formatted,
            colorama.Fore.RED + orig_formatted + colorama.Fore.RESET,
            orig_formatted
        )
        self.assertIsInstance(colored_formatted, ColorString)
        self.assertEqual(colored_formatted._color, 'red')  # pylint: disable=protected-access
        self.assertEqual(colored_formatted._string, orig_formatted)  # pylint: disable=protected-access

    def test_concatenation_postfix(self):
        self.assert_colored(
            ColorString('a', color='red') + 'b',
            colorama.Fore.RED + 'a' + colorama.Fore.RESET + 'b',
            'ab'
        )

    def test_concatenation_prefix(self):
        self.assert_colored(
            'a' + ColorString('b', color='red'),
            'a' + colorama.Fore.RED + 'b' + colorama.Fore.RESET,
            'ab'
        )

    def test_complex_concatenation(self):
        self.assert_colored(
            'this is ' +
            ColorString('a message', color='red') + ' to be colored',
            'this is ' + colorama.Fore.RED + 'a message' +
            colorama.Fore.RESET + ' to be colored',
            'this is a message to be colored'
        )

    def assert_colored(self, s, colored, uncolored):
        self.assertIsInstance(s, ColorStringBase)
        self.assertEqual(str(s), str(uncolored))
        self.assertEqual(repr(s), repr(uncolored))
        self.assertEqual(s.get_colored(), colored)


from django.test import TestCase

from checker.management.commands.checker import Checker


class CheckerTest(TestCase):

    def test_checker_get_id(self):
        """
        Comprueba Checker.get_id()
        """
        check = Checker()
        # Extrae el ID de los megavideo
        result = check.get_id('v', 'http://www.megavideo.com/?v=XE1R3861&f=blablalblaba')
        self.assertEqual('XE1R3861', result)
        result = check.get_id('v', 'http://www.megavideo.com/?x=slasffajlafklaffnakfk&v=XE1R3861&f=blablalblaba')
        self.assertEqual('XE1R3861', result)
        result = check.get_id('v', 'http://www.megavideo.com/?v=XE1R3861')
        self.assertEqual('XE1R3861', result)
        # Extrae el ID de los megaupload
        result = check.get_id('d', 'http://www.megaupload.com/?d=XE1R3861&f=blablalblaba')
        self.assertEqual('XE1R3861', result)
        result = check.get_id('d', 'http://www.megaupload.com/?x=slasffajlafklaffnakfk&d=XE1R3861&f=blablalblaba')
        self.assertEqual('XE1R3861', result)
        result = check.get_id('d', 'http://www.megaupload.com/?d=XE1R3861')
        self.assertEqual('XE1R3861', result)
        # Falla cuando tiene que fallar
        result = check.get_id('z', 'http://www.google.com/?d=XE1R3861')
        self.assertEqual(False, result)

    def test_checker_get_mega_code(self):
        """
        Comprueba Checker.get_mega_code()
        """
        check = Checker()
        # Extrae la informacion de los links de megavideo
        result = check.get_mega_code('http://www.megavideo.com/?v=XE1R3861&f=blablalblaba')
        self.assertEqual('XE1R3861', result['url_id'])
        self.assertEqual('megavideo', result['domain'])
        self.assertEqual('http://www.megavideo.com/?v=XE1R3861&f=blablalblaba', result['full_url'])
        # Extrae la informacion de los links de megaupload
        result = check.get_mega_code('http://www.megaupload.com/?d=XE1R3861&f=blablalblaba')
        self.assertEqual('XE1R3861', result['url_id'])
        self.assertEqual('megaupload', result['domain'])
        self.assertEqual('http://www.megaupload.com/?d=XE1R3861&f=blablalblaba', result['full_url'])
        # Falla cuando tiene que fallar
        result = check.get_mega_code('http://www.google.com/?d=XE1R3861')
        self.assertEqual('notvalid', result['domain'])
        self.assertEqual('http://www.google.com/?d=XE1R3861', result['full_url'])

    def test_checker_get_status(self):
        """
        Comprueba Checker.get_status()
        """
        check = Checker()
        # Extrae la informacion de los links de megavideo
        result = check.get_status('http://www.megavideo.com/?v=XE1R3861&f=blablalblaba')
        self.assertEqual('KO', result)
        result = check.get_status('http://www.megavideo.com/?v=DQBEJ1OK')
        self.assertEqual('OK', result)
        # Extrae la informacion de los links de megaupload
        result = check.get_status('http://www.megaupload.com/?d=XE1R3861&f=blablalblaba')
        self.assertEqual('KO', result)
        # Falla cuando tiene que fallar
        result = check.get_status('http://www.google.com/?d=XE1R3861')
        self.assertEqual(False, result)



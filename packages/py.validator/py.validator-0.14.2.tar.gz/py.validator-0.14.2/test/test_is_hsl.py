import unittest

from pyvalidator import *


class TestIsHsl(unittest.TestCase):

    def test_valid_hsl(self):
        self.assertTrue(is_hsl('hsl(360,0000000000100%,000000100%)'))
        self.assertTrue(is_hsl('hsl(000010, 00000000001%, 00000040%)'))
        self.assertTrue(is_hsl('HSL(00000,0000000000100%,000000100%)'))
        self.assertTrue(is_hsl('hsL(0, 0%, 0%)'))
        self.assertTrue(is_hsl('hSl(  360  , 100%  , 100%   )'))
        self.assertTrue(is_hsl('Hsl(  00150  , 000099%  , 01%   )'))
        self.assertTrue(is_hsl('hsl(01080, 03%, 4%)'))
        self.assertTrue(is_hsl('hsl(-540, 03%, 4%)'))
        self.assertTrue(is_hsl('hsla(+540, 03%, 4%)'))
        self.assertTrue(is_hsl('hsla(+540, 03%, 4%, 500)'))
        self.assertTrue(is_hsl('hsl(+540deg, 03%, 4%, 500)'))
        self.assertTrue(is_hsl('hsl(+540gRaD, 03%, 4%, 500)'))
        self.assertTrue(is_hsl('hsl(+540.01e-98rad, 03%, 4%, 500)'))
        self.assertTrue(is_hsl('hsl(-540.5turn, 03%, 4%, 500)'))
        self.assertTrue(is_hsl('hsl(+540, 03%, 4%, 500e-01)'))
        self.assertTrue(is_hsl('hsl(+540, 03%, 4%, 500e+80)'))
        self.assertTrue(is_hsl('hsl(4.71239rad, 60%, 70%)'))
        self.assertTrue(is_hsl('hsl(270deg, 60%, 70%)'))
        self.assertTrue(is_hsl('hsl(200, +.1%, 62%, 1)'))
        self.assertTrue(is_hsl('hsl(270 60% 70%)'))
        self.assertTrue(is_hsl('hsl(200, +.1e-9%, 62e10%, 1)'))
        self.assertTrue(is_hsl('hsl(.75turn, 60%, 70%)'))
        self.assertTrue(is_hsl('hsl(200grad +.1% 62% / 1)'))
        self.assertTrue(is_hsl('hsl(270, 60%, 50%, .15)'))
        self.assertTrue(is_hsl('hsl(270, 60%, 50%, 15%)'))
        self.assertTrue(is_hsl('hsl(270 60% 50% / .15)'))
        self.assertTrue(is_hsl('hsl(270 60% 50% / 15%)'))
        print('OK - test_valid_hsl')

    def test_invalid_hsl(self):
        self.assertFalse(is_hsl('hsl (360,0000000000100%,000000100%)'))
        self.assertFalse(is_hsl('hsl(0260, 100 %, 100%)'))
        self.assertFalse(is_hsl('hsl(0160, 100%, 100%, 100 %)'))
        self.assertFalse(is_hsl('hsl(-0160, 100%, 100a)'))
        self.assertFalse(is_hsl('hsl(-0160, 100%, 100)'))
        self.assertFalse(is_hsl('hsl(-0160 100%, 100%, )'))
        self.assertFalse(is_hsl('hsl(270 deg, 60%, 70%)'))
        self.assertFalse(is_hsl('hsl( deg, 60%, 70%)'))
        self.assertFalse(is_hsl('hsl(, 60%, 70%)'))
        self.assertFalse(is_hsl('hsl(3000deg, 70%)'))
        print('OK - test_invalid_hsl')

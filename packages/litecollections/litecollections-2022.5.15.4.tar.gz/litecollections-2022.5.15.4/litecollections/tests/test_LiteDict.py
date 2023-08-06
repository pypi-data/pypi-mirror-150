#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from unittest import TestCase, main
from random import getrandbits

from hypothesis import given
from hypothesis.strategies import text

from litecollections import LiteDict

''' Main unittests for litecollections.LiteDict '''

def random_bytes():
    return getrandbits(128).to_bytes(16, 'little')

class TestLiteDict(TestCase):
    ''' Main unittests for litecollections.LiteDict '''
    def test_int_keys(self):
        '''test if ints can be used as keys'''
        with LiteDict() as d:
            for k in range(10):
                assert k not in d
                assert k == len(d), [k, len(d)]
                d[k] = 'waffle'
                assert k in d
                assert d[k] == 'waffle', repr(d[k])
                assert k+1 == len(d), [k+1, len(d)]

    def test_str_keys(self):
        '''test if strings can be used as keys'''
        with LiteDict() as d:
            for _k in range(10):
                k=str(_k)
                assert k not in d, [k, d.keys()]
                assert _k == len(d), [_k, len(d)]
                d[k] = 'waffle'
                assert k in d, [k, d.keys()]
                assert d[k] == 'waffle', repr(d[k])
                assert _k+1 == len(d), [_k+1, len(d)]

    def test_random_byte_keys(self):
        '''test if bytes can be used as keys'''
        with LiteDict() as d:
            for _k in range(10):
                k=random_bytes()
                assert k not in d, [k, d.keys()]
                assert _k == len(d), [_k, d]
                d[k] = 'waffle'
                assert k in d, [k, d.keys()]
                assert d[k] == 'waffle', repr(d[k])
                assert _k+1 == len(d), [_k+1, len(d)]
                
    #def test_str_keys_with_persistence(self):
    #    print('now for persistence (this should fail if ran twice)')
    #    with LiteDict('persistent_dict.db') as d:
    #        for _k in range(10):
    #            k=str(_k)
    #            assert k not in d, [k, d.keys()]
    #            assert _k == len(d), [_k, d]
    #            d[k] = 'waffle'
    #            assert k in d, [k, d.keys()]
    #            assert d[k] == 'waffle', repr(d[k])
    #            assert _k+1 == len(d), [_k+1, len(d)]

class TestLiteDictHypthesisBeatdown(TestCase):
    def test_str_keys(self):
        '''tests if hypothesis can come up with keys that LiteDict wont work with'''
        @given(text(), text())
        def test(k, v):
            with LiteDict() as d:
                d[k] = v
                self.assertIn(k, d)
                self.assertEqual(d[k], v)
                d[k] = v + v
                self.assertEqual(d[k], v + v)
                del d[k]
                self.assertNotIn(k, d)
        test()

if __name__ == '__main__':
    main(verbosity=2)
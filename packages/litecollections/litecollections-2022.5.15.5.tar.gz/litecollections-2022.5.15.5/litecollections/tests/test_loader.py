from decimal import Decimal
from functools import partial
from random import getrandbits, random
from unittest import TestCase

from hypothesis import given
from hypothesis import strategies

from litecollections.loader import load, dump


def random_bytes():
    return getrandbits(128).to_bytes(16, 'little')

class Test_loader(TestCase):
    ''' Main unittests for litecollections.loader '''
    def test_various_encodings(self):
        test_inputs = [
            *[random() for i in range(4)],
            *[int(i*128) for i in range(4)],
            *[int(i*128)%2==1 for i in range(4)],
            *[str(i) for i in range(4)],
            *[complex(random(),random()) for i in range(4)],
            *[Decimal(random()) for i in range(4)],
            *[list(range(int(random()*128))) for i in range(4)],
            *[{str(random()): random() for ii in range(4)} for i in range(4)]
        ]
        for n, test in enumerate(test_inputs):
            #print('test', n+1, 'of', len(test_inputs), '-', type(test), '-', repr(test))
            # assert correct types for dump
            dt = dump(test)
            self.assertIsInstance(dt, str)
            # assert correct types for load
            dtl = load(dt)
            self.assertIsInstance(dtl, type(test))
            # assert no data change for double dump
            dtld = dump(dtl)
            self.assertEqual(dt, dtld)

class Test_loader_HypothesisBeatdown(TestCase):
    def generate_type_test(self, target_strategy):
        '''acts as a harness for type tests from hypothesis to try'''
        assert callable(target_strategy), target_strategy

        @given(target_strategy())
        def test(obj):
            dumped_obj = dump(obj)
            self.assertIsInstance(dumped_obj, str)
            reloaded_obj = load(dumped_obj)
            self.assertIsInstance(reloaded_obj, type(obj))
            # compare equality using repr because python thinks nan != nan
            self.assertEqual(
                repr(type(reloaded_obj)) + repr(reloaded_obj),
                repr(type(obj)) + repr(obj)
            )
            redumped_obj = dump(reloaded_obj)
            self.assertIsInstance(redumped_obj, str)
            self.assertEqual(redumped_obj, dumped_obj)

        return test

    def test_text(self):
        '''tests if hypothesis can come up with text that will break encoding'''
        self.generate_type_test(strategies.text)()
        
    def test_integers(self):
        '''tests if hypothesis can come up with integers that will break encoding'''
        self.generate_type_test(strategies.integers)()
    
    def test_floats(self):
        '''tests if hypothesis can come up with floats that will break encoding'''
        self.generate_type_test(strategies.floats)()
        
    def test_complex_numbers(self):
        '''tests if hypothesis can come up with complex_numbers that will break encoding'''
        self.generate_type_test(strategies.complex_numbers)()
        
    def test_booleans(self):
        '''tests if hypothesis can come up with booleans that will break encoding'''
        self.generate_type_test(strategies.booleans)()
        
    def test_binary(self):
        '''tests if hypothesis can come up with binary that will break encoding'''
        self.generate_type_test(strategies.binary)()
        
    def test_decimals(self):
        '''tests if hypothesis can come up with decimals that will break encoding'''
        self.generate_type_test(strategies.decimals)()
    
    def test_lists_of_text(self):
        '''tests if hypothesis can come up with lists of text that will break encoding'''
        self.generate_type_test(partial(strategies.lists, strategies.text()))()

    def test_lists_of_floats(self):
        '''tests if hypothesis can come up with lists of floats that will break encoding'''
        self.generate_type_test(partial(strategies.lists, strategies.floats()))()
    
    def test_lists_of_complex_numbers(self):
        '''tests if hypothesis can come up with lists of complex_numbers that will break encoding'''
        self.generate_type_test(partial(strategies.lists, strategies.complex_numbers()))()
    
    def test_lists_of_booleans(self):
        '''tests if hypothesis can come up with lists of booleans that will break encoding'''
        self.generate_type_test(partial(strategies.lists, strategies.booleans()))()
    
    def test_lists_of_binary(self):
        '''tests if hypothesis can come up with lists of binary that will break encoding'''
        self.generate_type_test(partial(strategies.lists, strategies.binary()))()
    
    def test_lists_of_decimals(self):
        '''tests if hypothesis can come up with lists of decimals that will break encoding'''
        self.generate_type_test(partial(strategies.lists, strategies.decimals()))()
    

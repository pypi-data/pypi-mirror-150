from json import loads as j_loads, JSONEncoder
from decimal import Decimal, DecimalTuple
from functools import partial

'''
    This is the enhanced json encoding library
    litecollections uses for json encoding the
    not officially supported json encodable
    python data types.
'''


__all__ = ['dump', 'load']


# map of "json dict encodings" for various python types
custom_dict_encodings = {
    bytes: (lambda o: {
        '__type__': 'bytes',
        'hex': o.hex()
    }),
    complex: (lambda o: {
        '__type__': 'complex',
        'imag': o.imag,
        'real': o.real
    }),
    Decimal: (lambda o: {
        '__type__': 'Decimal',
        'digits': list(o.as_tuple().digits),
        'exponent': o.as_tuple().exponent,
        'sign': o.as_tuple().sign
    })
}

# corresponding map of "json dict decoders" for the same various python types
custom_dict_decodings = {
    'bytes': (
        lambda o: bytes.fromhex(o['hex'])
    ),
    'complex': (
        lambda o: complex(o["real"], o["imag"])
    ),
    'Decimal': (
        lambda o: Decimal(DecimalTuple(
            sign=o["sign"],
            digits=o["digits"],
            exponent=o["exponent"]
        ))
    )
}

# validate custom_dict_encodings
for k, v in custom_dict_encodings.items():
    # type assertions
    assert isinstance(k, type), f'custom_dict_encoding only wants type keys not {repr(k)}'
    assert callable(v), f'custom_dict_encoding[{k}] needs to be callable not {repr(v)}'
    # integration assertions
    assert any(k.__name__==i for i in custom_dict_decodings), f'custom_dict_encodings[{k}] does not have a corresponding "decode" function in custom_dict_decodings'

# validate custom_dict_decodings
for k, v in custom_dict_decodings.items():
    # type assertions
    assert isinstance(k, str), f'custom_dict_decodings only wants "str" keys not {repr(k)}'
    assert callable(v), f'custom_dict_decodings[{k}] needs to be callable not {repr(v)}'
    # integration assertions
    assert any(i.__name__==k for i in custom_dict_encodings), f'custom_dict_decodings[{k}] does not have a corresponding "encode" function in custom_dict_encodings'

class LiteEncoder(JSONEncoder):
    ''' custom json encoder for additional supported json types '''
    def default(self, o):
        ''' encoder function to run if an object doesnt already have an official json encoder cooked in the json library '''
        # check if we have handlers for the incoming type
        if type(o) in custom_dict_encodings:
            return custom_dict_encodings[type(o)](o)
        # otherwise raise a NotImplementedError
        else:
            raise NotImplementedError(f'encoding for type[{type(o.__name__)}] has not been implemented yet')
    
    @staticmethod
    def dict_decode(dct):
        ''' dict decoder to catch custom dict encodings this library encoded to reassemble proper python datatypes '''
        if '__type__' in dct and dct['__type__'] in custom_dict_decodings:
            return custom_dict_decodings[dct['__type__']](dct)
        else:
            return dct

# user friendly functions we already understand how to use
dump = LiteEncoder().encode
load = partial(
    j_loads,
    object_hook=LiteEncoder().dict_decode
)


if __name__ == '__main__':
    # running this file runs light smoke testing
    # against the setup
    
    from random import getrandbits, random
    
    def random_bytes():
        return getrandbits(128).to_bytes(16, 'little')
    
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
        print('test', n+1, 'of', len(test_inputs), '-', type(test), '-', repr(test))
    
        # assert correct types
        dt = dump(test)
        assert isinstance(dt, str), dt
        assert isinstance(load(dt), type(test)), load(dt)
        # assert no data change
        dldt = dump(load(dump(test)))
        assert dt == dldt, [dt, dldt]
        print('good\n')

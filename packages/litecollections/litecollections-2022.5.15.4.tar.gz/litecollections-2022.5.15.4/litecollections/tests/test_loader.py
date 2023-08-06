from hypothesis import given
from hypothesis.strategies import text

from litecollections.loader import load, dump

print('test_decode_inverts_encode')
@given(text())
def test_decode_inverts_encode(s):
    print(s)
    assert load(dump(s)) == s

print('done')

if __name__ == "__main__":
    test_decode_inverts_encode()
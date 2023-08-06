from ..mycaesarcipher import CaesarCipher


class CaesarCipherTesting:

    def __init__(self, test_class=CaesarCipher()):
        self.test_class = test_class

    def test_encrypt(
        self,
        text,
        key,
        assertion,
        output_results: bool = True,
    ):
        assert self.test_class.encrypt(text, key, output_results) == assertion

    def test_decrypt(self, text, assertion, printResults: bool = False):
        assert self.test_class.decrypt(text, printResults) == assertion


testCC = CaesarCipherTesting()


def test_encodeA():
    testCC.test_encrypt('TESTING', 5, 'YJXYNSL')


def test_encodeB():
    testCC.test_encrypt("TeStInG", 5, 'YjXyNsL', False)


def test_encodeC():
    testCC.test_encrypt("Kk", 5, 'Pp', False)


def test_encodeD():
    testCC.test_encrypt("Password", 5, 'Ufxxbtwi', False)


def test_decodeA():
    testCC.test_decrypt('YJXYNSL', 'ZKYZOTM')


def test_decodeB():
    testCC.test_decrypt('YjXyNsL', 'ZkYzOtM', False)


def test_decodeC():
    testCC.test_decrypt('1djjktcqttccwprztsd', '6ekkludruuddxqsaute')

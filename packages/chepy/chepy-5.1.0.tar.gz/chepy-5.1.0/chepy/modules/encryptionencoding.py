import base64
import binascii
import codecs
import itertools
import string
from typing import Literal, TypeVar, Dict

import lazy_import

jwt = lazy_import.lazy_module("jwt")
import pathlib

import regex as re
import json

AES = lazy_import.lazy_module("Crypto.Cipher.AES")
ARC4 = lazy_import.lazy_module("Crypto.Cipher.ARC4")
DES = lazy_import.lazy_module("Crypto.Cipher.DES")
ChaCha20 = lazy_import.lazy_module("Crypto.Cipher.ChaCha20")
DES3 = lazy_import.lazy_module("Crypto.Cipher.DES3")
RSA = lazy_import.lazy_module("Crypto.PublicKey.RSA")
Hash = lazy_import.lazy_module("Crypto.Hash")
PKCS1_15 = lazy_import.lazy_module("Crypto.Signature.pkcs1_15")
PKCS1_OAEP = lazy_import.lazy_module("Crypto.Cipher.PKCS1_OAEP")
Blowfish = lazy_import.lazy_module("Crypto.Cipher.Blowfish")
Padding = lazy_import.lazy_module("Crypto.Util.Padding")
pycipher = lazy_import.lazy_module("pycipher")

from ..core import ChepyCore, ChepyDecorators
from ..extras.combinatons import hex_chars
from .internal.constants import EncryptionConsts

EncryptionEncodingT = TypeVar("EncryptionEncodingT", bound="EncryptionEncoding")


class EncryptionEncoding(ChepyCore):
    """This class handles most operations related to various encryption
    related operations. This class inherits the ChepyCore class, and all the
    methods are also available from the Chepy class

    Examples:
        >>> from chepy import Chepy
        or
        >>> from chepy.modules.encryptionencoding import EncryptionEncoding
    """

    def __init__(self, *data):
        super().__init__(*data)

    def __check_mode(self, mode) -> None:
        assert mode in ["CBC", "OFB", "CTR", "ECB"], "Not a valid mode."

    def _convert_key(
        self, key, iv, key_format: str, iv_format: str
    ) -> EncryptionEncodingT:  # pragma: no cover
        if isinstance(key, str):
            key = key.encode()
        # modify key according to mode
        if key_format == "hex":
            key = binascii.unhexlify(key)
        if key_format == "base64" or key_format == "b64":
            key = base64.b64decode(key)
        if key_format == "utf-8" or key_format == "utf8":
            key = key.decode().encode("utf-8")
        if key_format == "latin-1":
            key = key.decode().encode("latin-1")

        # modify iv according to mode
        if isinstance(iv, str):
            iv = iv.encode()
        if iv_format == "hex":
            iv = binascii.unhexlify(iv)
        if iv_format == "base64" or iv_format == "b64":
            iv = base64.b64decode(iv)
        if iv_format == "utf-8" or iv_format == "utf8":
            key = key.decode().encode("utf-8")
        if iv_format == "latin-1":
            key = key.decode().encode("latin-1")
        else:
            iv = binascii.unhexlify(binascii.hexlify(iv))
        return key, iv

    @ChepyDecorators.call_stack
    def rotate(self, rotate_by: int) -> EncryptionEncodingT:
        """Rotate string by provided number

        Args:
            rotate_by (int): Required. Number to rotate by

        Returns:
            Chepy: The Chepy object.

        Examples:
            In this example, we will rotate by 20

            >>> Chepy("some data").rotate(20).out
            "migy xunu"
        """
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(
            lc + uc, lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by]
        )
        self.state = self.state.translate(lookup)
        return self

    @ChepyDecorators.call_stack
    def rotate_bruteforce(self) -> EncryptionEncodingT:
        """Brute force rotation from 1 to 26.
        Returned value is a dict where key is the rotation count.

        Returns:
            Chepy: The Chepy object.

        Examples:
            In this example, we will rotate by 20

            >>> Chepy('uryyb').rotate_bruteforce()
            {
                '1': 'vszzc',
                '2': 'wtaad',
                ...
                '13': 'hello',
                ...
            }
        """
        hold = {}
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        for rotate_by in range(1, 27):
            lookup = str.maketrans(
                lc + uc,
                lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by],
            )
            hold[str(rotate_by)] = self.state.translate(lookup)
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def rot_13(self) -> EncryptionEncodingT:
        """ROT-13 encoding

        A simple caesar substitution cipher which rotates alphabet
        characters by the specified amount (default 13).

        Returns:
            Chepy: The Chepy object.
        """
        self.state = codecs.encode(self._convert_to_str(), "rot_13")
        return self

    @ChepyDecorators.call_stack
    def rot_47(self, amount: int = 14) -> EncryptionEncodingT:
        """ROT 47 encoding

        A slightly more complex variation of a caesar cipher, which includes
        ASCII characters from 33 '!' to 126 '~'. Default rotation: 47.

        Args:
            amount (int, optional): Amount to rotate by. Defaults to 14.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some").rot_47().out
            "D@>6"
        """
        x = []
        for i in range(len(self.state)):
            j = ord(self.state[i])
            if j >= 33 and j <= 126:
                x.append(chr(33 + ((j + amount) % 94)))
            else:  # pragma: no cover
                x.append(self.state[i])
        self.state = "".join(x)
        return self

    @ChepyDecorators.call_stack
    def xor(
        self,
        key: str,
        key_type: Literal["hex", "utf", "base64"] = "hex",
    ) -> EncryptionEncodingT:
        """XOR state with a key

        Args:
            key (str): Required. The key to xor by
            key_type (str, optional): The key type. Valid values are hex, utf and base64. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("secret").xor(key="secret", key_type="utf").to_hex()
            000000000000
        """
        assert key_type in [
            "utf",
            "hex",
            "base64",
        ], "Valid key types are hex, utf and base64"

        if isinstance(key, int):
            key = str(key)
        if key_type == "utf":
            key = binascii.hexlify(key.encode())
        elif key_type == "base64":
            key = binascii.hexlify(base64.b64decode(key.encode()))
        key = binascii.unhexlify(key)
        x = bytearray(b"")
        try:
            for char, key_val in zip(self._convert_to_str(), itertools.cycle(key)):
                x.append(ord(char) ^ key_val)
        except:
            for char, key_val in zip(self._convert_to_bytes(), itertools.cycle(key)):
                x.append(char ^ key_val)

        self.state = x
        return self

    @ChepyDecorators.call_stack
    def xor_bruteforce(self, length: int = 100) -> EncryptionEncodingT:
        """Brute force single byte xor

        For multibyte xor bruteforce, use chepy.extras.crypto_extras.xor_bruteforce_multi
        function

        Args:
            length (int, optional): How to bytes to bruteforce. Defaults to 100.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("pf`qfw").xor_bruteforce()
            {'00': bytearray(b'pf`qfw'),
            '01': bytearray(b'qgapgv'),
            '02': bytearray(b'rdbsdu'),
            '03': bytearray(b'secret'), # here is our secret xored with the hex key 03
            '04': bytearray(b'tbdubs'),
            '05': bytearray(b'ucetcr'),
            ...}
            >>> c.get_by_key("03").bytearray_to_str()
            secret
            >>> c.xor("03").bytearray_to_str()
            pf`qfw
        """
        original = self.state
        found = {}
        keys = hex_chars()
        self.state = original[:length]
        for key in keys:
            self.xor(key)
            found[key] = self.state
            self.state = original[:length]
        self.state = found
        return self

    @ChepyDecorators.call_stack
    def jwt_decode(self) -> EncryptionEncodingT:
        """Decode a JWT token. Does not verify

        Returns:
            Chepy: The Chepy object.
        """
        self.state = {
            "payload": jwt.decode(self._convert_to_str(), verify=False),
            "header": jwt.get_unverified_header(self._convert_to_str()),
        }
        return self

    @ChepyDecorators.call_stack
    def jwt_verify(
        self, secret: str, algorithm: list = ["HS256"]
    ) -> EncryptionEncodingT:
        """Verify JWT token

        Args:
            secret (str): Required. Secret key for token
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"]

        Returns:
            Chepy: The Chepy object.
        """
        self.state = jwt.decode(
            self._convert_to_str(), key=secret, algorithms=algorithm
        )
        return self

    @ChepyDecorators.call_stack
    def jwt_sign(self, secret: str, algorithms: str = "HS256") -> EncryptionEncodingT:
        """Sign a json/dict object in JWT

        Args:
            secret (str): Required. Secret to sign with
            algorithms (str, optional): Signing algorithm. Defaults to "HS256".

        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, dict):
            data = self.state
        elif isinstance(self.state, str):
            data = json.loads(self.state)
        self.state = jwt.encode(data, key=secret, algorithm=algorithms)
        return self

    @ChepyDecorators.call_stack
    def jwt_bruteforce(
        self, wordlist: str, b64_encode: bool = False, algorithm: list = ["HS256"]
    ) -> EncryptionEncodingT:
        """Brute force JWT token secret

        This method will use the provided wordlist to try and bruteforce the
        verification.

        Args:
            wordlist (str): Required. Path to a wordlist
            b64_encode (bool, optional): Encoded the words in base64. Defaults to False.
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"].

        Returns:
            Chepy: The Chepy object.
        """
        with open(pathlib.Path(wordlist).expanduser().absolute()) as words:
            for word in words:
                try:
                    word = word.strip()
                    if b64_encode:  # pragma: no cover
                        word = base64.b64encode(word)
                    j = jwt.decode(self._convert_to_str(), word, algorithms=algorithm)
                    self.state = {
                        "paylod": j,
                        "header": jwt.get_unverified_header(self._convert_to_str()),
                        "secret": word,
                    }
                    return self
                except jwt.InvalidSignatureError:
                    continue
            else:  # pragma: no cover
                return self

    @ChepyDecorators.call_stack
    def rc4_encrypt(self, key: str, key_format: str = "hex") -> EncryptionEncodingT:
        """Encrypt raw state with RC4

        Args:
            key (str): Required. Secret key
            key_format (str, optional): Key format. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").rc4_encrypt("736563726574").o
            b"9e59bf79a2c0b7d253"
        """
        if isinstance(key, str):
            key = key.encode()
        if key_format == "hex":
            key = binascii.unhexlify(key)
        elif key_format == "base64":
            key = base64.b64decode(key)
        elif key_format == "utf-16-le":
            key = key.decode().encode("utf-16-le")
        elif key_format == "utf-16-be":
            key = key.decode().encode("utf-16-be")
        cipher = ARC4.new(key)
        self.state = binascii.hexlify(cipher.encrypt(self._convert_to_bytes()))
        return self

    @ChepyDecorators.call_stack
    def rc4_decrypt(self, key: str, key_format: str = "hex") -> EncryptionEncodingT:
        """Decrypt raw state with RC4

        Args:
            key (str): Required. Secret key
            key_format (str, optional): Key format. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("9e59bf79a2c0b7d253").hex_to_str().rc4_decrypt("secret").o
            b"some data"
        """
        if isinstance(key, str):
            key = key.encode()
        if key_format == "hex":
            key = binascii.unhexlify(key)
        elif key_format == "base64":
            key = base64.b64decode(key)
        elif key_format == "utf-16-le":
            key = key.decode().encode("utf-16-le")
        elif key_format == "utf-16-be":
            key = key.decode().encode("utf-16-be")
        cipher = ARC4.new(key)
        self.state = cipher.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with DES

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").des_encrypt("70617373776f7264").o
            b"1ee5cb52954b211d1acd6e79c598baac"

            To encrypt using a differnt mode

            >>> Chepy("some data").des_encrypt("password", mode="CTR").o
            b"0b7399049b0267d93d"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = DES.new(key, mode=DES.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES.new(key, mode=DES.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def des_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("1ee5cb52954b211d1acd6e79c598baac").hex_to_str().des_decrypt("password").o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = DES.new(key, mode=DES.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES.new(key, mode=DES.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def chacha_encrypt(
        self,
        key: str,
        nonce: str = "0000000000000000",
        key_format: str = "hex",
        nonce_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with ChaCha 20 rounds

        Args:
            key (str): Required. The secret key
            nonce (str, optional): Nonce. Defaults to '0000000000000000'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            nonce_format (str, optional): Format of nonce. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.
        """

        key, nonce = self._convert_key(key, nonce, key_format, nonce_format)

        cipher = ChaCha20.new(key=key, nonce=nonce)
        self.state = cipher.encrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def chacha_decrypt(
        self,
        key: str,
        nonce: str = "0000000000000000",
        key_format: str = "hex",
        nonce_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with ChaCha 20 rounds.

        Args:
            key (str): Required. The secret key
            nonce (str, optional): nonce for certain modes only. Defaults to '0000000000000000'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            nonce_format (str, optional): Format of nonce. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.
        """

        key, nonce = self._convert_key(key, nonce, key_format, nonce_format)

        cipher = ChaCha20.new(key=key, nonce=nonce)
        self.state = cipher.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def triple_des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Triple DES

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").triple_des_encrypt("super secret password !!", mode="ECB").o
            b"f8b27a0d8c837edc8fb00ea85f502fb4"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = DES3.new(key, mode=DES3.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES3.new(key, mode=DES3.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def triple_des_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("f8b27a0d8c837edce87dd13a1ab41f96")
            >>> c.hex_to_str()
            >>> c.triple_des_decrypt("super secret password !!")
            >>> c.o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = DES3.new(key, mode=DES3.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES3.new(key, mode=DES3.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def aes_encrypt(
        self,
        key: str,
        iv: str = "00000000000000000000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with AES.
        CFB mode reflects Cyberchef and not native python behaviour.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").aes_encrypt("secret password!", mode="ECB").o
            b"5fb8c186394fc399849b89d3b6605fa3"
        """

        assert mode in ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"], "Not a valid mode."

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "CFB":
            cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv, segment_size=128)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "CTR":
            cipher = AES.new(key, mode=AES.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "GCM":
            cipher = AES.new(
                key,
                mode=AES.MODE_GCM,
                nonce=binascii.unhexlify("00000000000000000000000000000000"),
            )
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = AES.new(key, mode=AES.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def aes_decrypt(
        self,
        key: str,
        iv: str = "00000000000000000000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.
        CFB mode reflects Cyberchef and not native python behaviour.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("5fb8c186394fc399849b89d3b6605fa3")
            >>> c.hex_to_str()
            >>> c.aes_decrypt("7365637265742070617373776f726421")
            >>> c.o
            b"some data"
        """

        assert mode in ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"], "Not a valid mode."

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        if mode == "CFB":
            cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv, segment_size=128)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        elif mode == "CTR":
            cipher = AES.new(key, mode=AES.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "GCM":
            cipher = AES.new(
                key,
                mode=AES.MODE_GCM,
                nonce=binascii.unhexlify("00000000000000000000000000000000"),
            )
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = AES.new(key, mode=AES.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def blowfish_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Blowfish

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").blowfish_encrypt("password", mode="ECB").o
            b"d9b0a79853f139603951bff96c3d0dd5"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def blowfish_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Blowfish

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("d9b0a79853f13960fcee3cae16e27884")
            >>> c.hex_to_str()
            >>> c.blowfish_decrypt("password", key_format="utf-8")
            >>> c.o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def vigenere_encode(self, key: str) -> EncryptionEncodingT:
        """Encode with Vigenere ciper

        Args:
            key (str): Required. The secret key

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("secret").vigenere_encode("secret").o
            "KIEIIM"
        """
        self.state = pycipher.Vigenere(key=key).encipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def vigenere_decode(self, key: str) -> EncryptionEncodingT:
        """Decode Vigenere ciper

        Args:
            key (str): Required. The secret key

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("KIEIIM").vigenere_decode("secret").o
            "SECRET"
        """
        self.state = pycipher.Vigenere(key=key).decipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def affine_encode(self, a: int = 1, b: int = 1) -> EncryptionEncodingT:
        """Encode with Affine ciper

        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("secret").affine_encode().o
            "TFDSFU"
        """
        self.state = pycipher.Affine(a=a, b=b).encipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def affine_decode(self, a: int = 1, b: int = 1) -> EncryptionEncodingT:
        """Decode Affine ciper

        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("TFDSFU").affine_decode().o
            "SECRET"
        """
        self.state = pycipher.Affine(a=a, b=b).decipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def atbash_encode(self) -> EncryptionEncodingT:
        """Encode with Atbash ciper

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("secret").atbash_encode().o
            "HVXIVG"
        """
        self.state = pycipher.Atbash().encipher(self._convert_to_str(), keep_punct=True)
        return self

    @ChepyDecorators.call_stack
    def atbash_decode(self) -> EncryptionEncodingT:
        """Decode Atbash ciper

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("hvxivg").atbash_decode().o
            "SECRET"
        """
        self.state = pycipher.Atbash().decipher(self._convert_to_str(), keep_punct=True)
        return self

    @ChepyDecorators.call_stack
    def to_morse_code(
        self,
        dot: str = ".",
        dash: str = "-",
        letter_delim: str = " ",
        word_delim: str = "\n",
    ) -> EncryptionEncodingT:
        """Encode string to morse code

        Args:
            dot (str, optional): The char for dot. Defaults to ".".
            dash (str, optional): The char for dash. Defaults to "-".
            letter_delim (str, optional): Letter delimiter. Defaults to " ".
            word_delim (str, optional): Word delimiter. Defaults to "\\n".

        Returns:
            Chepy: The Chepy object.
        """
        encode = ""
        morse_code_dict = EncryptionConsts.MORSE_CODE_DICT
        for k, v in morse_code_dict.items():
            morse_code_dict[k] = v.replace(".", dot).replace("-", dash)
        for word in self._convert_to_str().split():
            for w in word:
                encode += morse_code_dict.get(w.upper()) + letter_delim
            encode += word_delim
        self.state = encode
        return self

    @ChepyDecorators.call_stack
    def from_morse_code(
        self,
        dot: str = ".",
        dash: str = "-",
        letter_delim: str = " ",
        word_delim: str = "\n",
    ) -> EncryptionEncodingT:
        """Decode morse code

        Args:
            dot (str, optional): The char for dot. Defaults to ".".
            dash (str, optional): The char for dash. Defaults to "-".
            letter_delim (str, optional): Letter delimiter. Defaults to " ".
            word_delim (str, optional): Word delimiter. Defaults to "\\n".

        Returns:
            Chepy: The Chepy object.
        """
        decode = ""
        morse_code_dict = EncryptionConsts.MORSE_CODE_DICT
        for k, v in morse_code_dict.items():
            morse_code_dict[k] = v.replace(".", dot).replace("-", dash)

        morse_code_dict = {value: key for key, value in morse_code_dict.items()}
        for chars in self._convert_to_str().split(letter_delim):
            if word_delim in chars:
                chars = re.sub(word_delim, "", chars, re.I)
                if morse_code_dict.get(chars) is not None:
                    decode += " " + morse_code_dict.get(chars)
                else:  # pragma: no cover
                    decode += " " + chars
            else:
                decode += morse_code_dict.get(chars)
        self.state = decode
        return self

    @ChepyDecorators.call_stack
    def rsa_encrypt(self, pub_key_path: str) -> EncryptionEncodingT:
        """Encrypt data with RSA Public key in PEM format

        Args:
            pub_key_path (str): Path to Public key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(pub_key_path)), "r") as f:
            pub_key = f.read()
            key = RSA.importKey(pub_key)
            cipher = PKCS1_OAEP.new(key)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def rsa_decrypt(self, priv_key_path: str) -> EncryptionEncodingT:
        """Decrypt data with RSA Private key in PEM format

        Args:
            priv_key_path (str): Path to Private key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(priv_key_path)), "r") as f:
            priv_key = f.read()
            key = RSA.importKey(priv_key)
            cipher = PKCS1_OAEP.new(key)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def rsa_sign(self, priv_key_path: str) -> EncryptionEncodingT:
        """Sign data in state with RSA Private key in PEM format

        Args:
            priv_key_path (str): Path to Private key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(priv_key_path)), "r") as f:
            priv_key = f.read()
            key = RSA.importKey(priv_key)
            h = Hash.SHA256.new(self._convert_to_bytes())
            self.state = PKCS1_15.new(key).sign(h)
            return self

    @ChepyDecorators.call_stack
    def rsa_verify(
        self, signature: bytes, public_key_path: str
    ) -> EncryptionEncodingT:  # pragma: no cover
        """Verify data in state with RSA Public key in PEM format

        Args:
            signature (bytes): The signature as bytes
            public_key_path (str): Path to Private key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(public_key_path)), "r") as f:
            pub_key = f.read()
            key = RSA.importKey(pub_key)
            h = Hash.SHA256.new(self._convert_to_bytes())
            self.state = PKCS1_15.new(key).verify(h, signature)
            return self

    @ChepyDecorators.call_stack
    def monoalphabetic_substitution(
        self, mapping: Dict[str, str] = {}
    ) -> EncryptionEncodingT:
        """Monoalphabetic substitution. Re-map characters

        Args:
            mapping (Dict[str, str], optional): Mapping of characters where key is the character to map and value is the new character to replace with. Defaults to {}.

        Returns:
            Chepy: The Chepy object
        """
        hold = ""
        cipher = self._convert_to_str()
        for c in cipher:
            hold += mapping.get(c.lower(), c)
        self.state = hold
        return self

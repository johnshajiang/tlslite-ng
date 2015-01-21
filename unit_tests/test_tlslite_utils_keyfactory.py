# Copyright (c) 2015, Hubert Kario
#
# See the LICENSE file for legal information regarding use of this file.

import unittest

from tlslite.utils.keyfactory import parsePEMKey
from tlslite.utils.rsakey import RSAKey
from tlslite.utils import cryptomath

class TestParsePEMKey(unittest.TestCase):

    # generated with:
    # openssl req -x509 -newkey rsa:1024 -keyout localhost.key \
    # -out localhost.crt -subj /CN=localhost -nodes -batch -sha256
    privKey_str = str(
        "-----BEGIN PRIVATE KEY-----"\
        "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBANEJBHmpEslfyzLU"\
        "3gEXUbV+aXW81blLqjiHc95YO2DskSf6Mi0z81l6Ssa//7eBT0L2LEiYlTpT5PPe"\
        "RTburDRf7iUMkBnxVmCpBOn8xYn0OrPZLLLJBZS9Q1SP3Q/2Z+7IM7mtj9UsiyR0"\
        "E07NTLTG9e9P319hAT5A8/tpGCjdAgMBAAECgYBVItsTwezI358fANu6jgjVZrsF"\
        "HPffFBYsF971O/JTM4abRaeSCYqfctNpx2EbGCt0FldK6fo9W1XwjSKbkPHJVo12"\
        "Lfeyn48iRlTfzp/VVSpydieaCyexRAQElC59RmaA0z5t9H5F+WLgx7DyVDSyitn5"\
        "3b/l+wzSDzRCGLkzcQJBAO9d4LKtzLS78dkU2MiWjJdoAi9q9notzqB/OcJJ8dzl"\
        "jCmU5jt0hanwVFElzJeQDfvSXl0nQRePkbG51X1BDjcCQQDfj5HGNGTgNPtmj61s"\
        "z8WSiLuOHX/SEWRTk0MfB4l4f+Ymx6Ie2wco5w8a0QYEGpPYo09ZXPgWPX0uJSaa"\
        "NZeLAkEAgGzj07n/7LAx0ACpVuW/RLSfB4Xh/Cd7hwz7lkxKIfRewSiMZjXcSRMS"\
        "if83x9GYTxXNXzliaRu0VaCY9Hzk/QJBAKx6VZs3XQRlm/f6rXAftGxjNWBlffIS"\
        "HPclzEkqRXNEKcqNhpSLozB5Y3vq+9s6rgobpOJrCbQO6H8rhma/JhUCQGmkTlFF"\
        "CpeK/UoX1sCtwAke8ubS+cc+l/XIhCvltbqeMG4vipzGVoolUZFdPvIW2PZ+PSC/"\
        "f3XiNjay5aqnxck="\
        "-----END PRIVATE KEY-----")
    cert_str = str(
        "-----BEGIN CERTIFICATE-----"\
        "MIIB9jCCAV+gAwIBAgIJAMyn9DpsTG55MA0GCSqGSIb3DQEBCwUAMBQxEjAQBgNV"\
        "BAMMCWxvY2FsaG9zdDAeFw0xNTAxMjExNDQzMDFaFw0xNTAyMjAxNDQzMDFaMBQx"\
        "EjAQBgNVBAMMCWxvY2FsaG9zdDCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA"\
        "0QkEeakSyV/LMtTeARdRtX5pdbzVuUuqOIdz3lg7YOyRJ/oyLTPzWXpKxr//t4FP"\
        "QvYsSJiVOlPk895FNu6sNF/uJQyQGfFWYKkE6fzFifQ6s9kssskFlL1DVI/dD/Zn"\
        "7sgzua2P1SyLJHQTTs1MtMb170/fX2EBPkDz+2kYKN0CAwEAAaNQME4wHQYDVR0O"\
        "BBYEFJtvXbRmxRFXYVMOPH/29pXCpGmLMB8GA1UdIwQYMBaAFJtvXbRmxRFXYVMO"\
        "PH/29pXCpGmLMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQELBQADgYEAkOgC7LP/"\
        "Rd6uJXY28HlD2K+/hMh1C3SRT855ggiCMiwstTHACGgNM+AZNqt6k8nSfXc6k1gw"\
        "5a7SGjzkWzMaZC3ChBeCzt/vIAGlMyXeqTRhjTCdc/ygRv3NPrhUKKsxUYyXRk5v"\
        "g/g6MwxzXfQP3IyFu3a9Jia/P89Z1rQCNRY="\
        "-----END CERTIFICATE-----"\
        )
    privKey_str_newLines = str(
        "-----BEGIN PRIVATE KEY-----\n"\
        "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBANEJBHmpEslfyzLU\n"\
        "3gEXUbV+aXW81blLqjiHc95YO2DskSf6Mi0z81l6Ssa//7eBT0L2LEiYlTpT5PPe\n"\
        "RTburDRf7iUMkBnxVmCpBOn8xYn0OrPZLLLJBZS9Q1SP3Q/2Z+7IM7mtj9UsiyR0\n"\
        "E07NTLTG9e9P319hAT5A8/tpGCjdAgMBAAECgYBVItsTwezI358fANu6jgjVZrsF\n"\
        "HPffFBYsF971O/JTM4abRaeSCYqfctNpx2EbGCt0FldK6fo9W1XwjSKbkPHJVo12\n"\
        "Lfeyn48iRlTfzp/VVSpydieaCyexRAQElC59RmaA0z5t9H5F+WLgx7DyVDSyitn5\n"\
        "3b/l+wzSDzRCGLkzcQJBAO9d4LKtzLS78dkU2MiWjJdoAi9q9notzqB/OcJJ8dzl\n"\
        "jCmU5jt0hanwVFElzJeQDfvSXl0nQRePkbG51X1BDjcCQQDfj5HGNGTgNPtmj61s\n"\
        "z8WSiLuOHX/SEWRTk0MfB4l4f+Ymx6Ie2wco5w8a0QYEGpPYo09ZXPgWPX0uJSaa\n"\
        "NZeLAkEAgGzj07n/7LAx0ACpVuW/RLSfB4Xh/Cd7hwz7lkxKIfRewSiMZjXcSRMS\n"\
        "if83x9GYTxXNXzliaRu0VaCY9Hzk/QJBAKx6VZs3XQRlm/f6rXAftGxjNWBlffIS\n"\
        "HPclzEkqRXNEKcqNhpSLozB5Y3vq+9s6rgobpOJrCbQO6H8rhma/JhUCQGmkTlFF\n"\
        "CpeK/UoX1sCtwAke8ubS+cc+l/XIhCvltbqeMG4vipzGVoolUZFdPvIW2PZ+PSC/\n"\
        "f3XiNjay5aqnxck=\n"\
        "-----END PRIVATE KEY-----\n")
    cert_str_newLines = str(
        "-----BEGIN CERTIFICATE-----\n"\
        "MIIB9jCCAV+gAwIBAgIJAMyn9DpsTG55MA0GCSqGSIb3DQEBCwUAMBQxEjAQBgNV\n"\
        "BAMMCWxvY2FsaG9zdDAeFw0xNTAxMjExNDQzMDFaFw0xNTAyMjAxNDQzMDFaMBQx\n"\
        "EjAQBgNVBAMMCWxvY2FsaG9zdDCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA\n"\
        "0QkEeakSyV/LMtTeARdRtX5pdbzVuUuqOIdz3lg7YOyRJ/oyLTPzWXpKxr//t4FP\n"\
        "QvYsSJiVOlPk895FNu6sNF/uJQyQGfFWYKkE6fzFifQ6s9kssskFlL1DVI/dD/Zn\n"\
        "7sgzua2P1SyLJHQTTs1MtMb170/fX2EBPkDz+2kYKN0CAwEAAaNQME4wHQYDVR0O\n"\
        "BBYEFJtvXbRmxRFXYVMOPH/29pXCpGmLMB8GA1UdIwQYMBaAFJtvXbRmxRFXYVMO\n"\
        "PH/29pXCpGmLMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQELBQADgYEAkOgC7LP/\n"\
        "Rd6uJXY28HlD2K+/hMh1C3SRT855ggiCMiwstTHACGgNM+AZNqt6k8nSfXc6k1gw\n"\
        "5a7SGjzkWzMaZC3ChBeCzt/vIAGlMyXeqTRhjTCdc/ygRv3NPrhUKKsxUYyXRk5v\n"\
        "g/g6MwxzXfQP3IyFu3a9Jia/P89Z1rQCNRY=\n"\
        "-----END CERTIFICATE-----\n"\
        )

    # generated with:
    # openssl genrsa -out privkey.pem 1024
    privRSAKey_str = str(
        "-----BEGIN RSA PRIVATE KEY-----"\
        "MIICXAIBAAKBgQCnBW08FYymHDwA+Vug5QWH2g0nX2EnTnzdyvaZ/mE1pCTxV+Fp"\
        "j0glrRIoPJPP+rZTcl/cqm7FSD+n2QDWHrg4h8xFPC7uPyfrbd/u6hTO3edu0los"\
        "tKkq93ZiM/kmfHIS57/nOiG9ETySx4TP4ca6dhNoIAU5uMQDHjhgSXSU4wIDAQAB"\
        "AoGAOB2PpOdMmSbVVjJxga5Q3GL7lmXqW214cIBXuEeKW55ptxiiqHe2csoiVph7"\
        "xR3kEkdUQ+yTSP9MO9Wh/U7W78RTKM21tRn2uwzVD4p0whVK/WCa0zsSu41VQ23l"\
        "wxN3Byrxw6jTTKD3gSLJc/4kGaduXgc/1IHCtmVaD9L2XJkCQQDVjqaDuQhPqzGI"\
        "kHZ77PARFLf3q+nVIFSIf1m/wxLQEj1HZ9PuyHNm0USQYswwDnh9g7F25YylWex+"\
        "yiefS0/fAkEAyDcekKtYudtgOhyN7tgSlUiHEyLCRo5IeazKQ0wNCDWfok9HYpEo"\
        "mOuE+NIQEcCJu+sRXK6rykJQGkHgYsALfQJAN5aJK3Jngm1aWGTaIonbN2cAN/zM"\
        "wghHWLxlfS/m3rhQsRyKovYUa+f/A+JjqgKqRGmaMQuxX30XvS0bwTAWWwJAQl3j"\
        "B9mEg7cwYpLsiWueXVW5UKKI+5JWe97G/R/MghgkXk0hQI8VgfswDLq1EO1duqjl"\
        "DG/qChWJL+r+Uj2OkQJBAK22WDZnIa52dm6G2dC+pM7TC10p7pwOS+G4YsA92Jd2"\
        "rBjtgPGNR6tCjWMh0+2AUF5lTbXAPqECeV6MIvJXGpg="\
        "-----END RSA PRIVATE KEY-----"\
        )
    privRSAKey_str_newLines = str(
        "-----BEGIN RSA PRIVATE KEY-----\n"\
        "MIICXAIBAAKBgQCnBW08FYymHDwA+Vug5QWH2g0nX2EnTnzdyvaZ/mE1pCTxV+Fp\n"\
        "j0glrRIoPJPP+rZTcl/cqm7FSD+n2QDWHrg4h8xFPC7uPyfrbd/u6hTO3edu0los\n"\
        "tKkq93ZiM/kmfHIS57/nOiG9ETySx4TP4ca6dhNoIAU5uMQDHjhgSXSU4wIDAQAB\n"\
        "AoGAOB2PpOdMmSbVVjJxga5Q3GL7lmXqW214cIBXuEeKW55ptxiiqHe2csoiVph7\n"\
        "xR3kEkdUQ+yTSP9MO9Wh/U7W78RTKM21tRn2uwzVD4p0whVK/WCa0zsSu41VQ23l\n"\
        "wxN3Byrxw6jTTKD3gSLJc/4kGaduXgc/1IHCtmVaD9L2XJkCQQDVjqaDuQhPqzGI\n"\
        "kHZ77PARFLf3q+nVIFSIf1m/wxLQEj1HZ9PuyHNm0USQYswwDnh9g7F25YylWex+\n"\
        "yiefS0/fAkEAyDcekKtYudtgOhyN7tgSlUiHEyLCRo5IeazKQ0wNCDWfok9HYpEo\n"\
        "mOuE+NIQEcCJu+sRXK6rykJQGkHgYsALfQJAN5aJK3Jngm1aWGTaIonbN2cAN/zM\n"\
        "wghHWLxlfS/m3rhQsRyKovYUa+f/A+JjqgKqRGmaMQuxX30XvS0bwTAWWwJAQl3j\n"\
        "B9mEg7cwYpLsiWueXVW5UKKI+5JWe97G/R/MghgkXk0hQI8VgfswDLq1EO1duqjl\n"\
        "DG/qChWJL+r+Uj2OkQJBAK22WDZnIa52dm6G2dC+pM7TC10p7pwOS+G4YsA92Jd2\n"\
        "rBjtgPGNR6tCjWMh0+2AUF5lTbXAPqECeV6MIvJXGpg=\n"\
        "-----END RSA PRIVATE KEY-----\n"\
        )

    @unittest.skipIf(cryptomath.m2cryptoLoaded, "requires no M2Crypto")
    def test_with_missing_m2crypto(self):
        with self.assertRaises(ValueError):
            key = parsePEMKey(self.privKey_str,
                    private=True,
                    implementations=["openssl"])

    @unittest.skipUnless(cryptomath.m2cryptoLoaded, "requires M2Crypto")
    def test_key_parse_using_openssl(self):

        # XXX doesn't handle "BEGIN PRIVATE KEY" header, as generated by
        # openssl req -x509 -newkey rsa:1024 -keyout localhost.key \
        # -out localhost.crt -subj /CN=localhost -nodes -batch -sha256
        with self.assertRaises(SyntaxError):
            key = parsePEMKey(self.privKey_str,
                    private=True,
                    implementations=["openssl"])

        #self.assertIsInstance(key, RSAKey)
        #self.assertEqual(1024, len(key))
        #self.assertTrue(key.hasPrivateKey())

    @unittest.skipUnless(cryptomath.m2cryptoLoaded, "requires M2Crypto")
    def test_key_parse_with_new_lines_using_openssl(self):

        # XXX doesn't handle "BEGIN PRIVATE KEY" header, as generated by
        # openssl req -x509 -newkey rsa:1024 -keyout localhost.key \
        # -out localhost.crt -subj /CN=localhost -nodes -batch -sha256
        with self.assertRaises(SyntaxError):
            key = parsePEMKey(self.privKey_str_newLines,
                    private=True,
                    implementations=["openssl"])

        #self.assertIsInstance(key, RSAKey)
        #self.assertEqual(1024, len(key))
        #self.assertTrue(key.hasPrivateKey())

    @unittest.skipUnless(cryptomath.m2cryptoLoaded, "requires M2Crypto")
    def test_rsa_key_parse_using_openssl(self):
        # XXX doesn't handle files without newlines
        with self.assertRaises(SyntaxError):
            key = parsePEMKey(self.privRSAKey_str,
                    private=True,
                    implementations=["openssl"])

        #self.assertIsInstance(key, RSAKey)
        #self.assertEqual(1024, len(key))
        #self.assertTrue(key.hasPrivateKey())

    @unittest.skipUnless(cryptomath.m2cryptoLoaded, "requires M2Crypto")
    def test_rsa_key_parse_with_new_lines_using_openssl(self):
        key = parsePEMKey(self.privRSAKey_str_newLines,
                private=True,
                implementations=["openssl"])

        self.assertIsInstance(key, RSAKey)
        self.assertEqual(1024, len(key))
        self.assertTrue(key.hasPrivateKey())

    def test_key_parse_using_python(self):

        key = parsePEMKey(self.privKey_str,
                private=True,
                implementations=["python"])

        self.assertIsInstance(key, RSAKey)
        self.assertEqual(1024, len(key))
        self.assertTrue(key.hasPrivateKey())

    def test_key_parse_with_new_lines_using_python(self):

        key = parsePEMKey(self.privKey_str_newLines,
                private=True,
                implementations=["python"])

        self.assertIsInstance(key, RSAKey)
        self.assertEqual(1024, len(key))
        self.assertTrue(key.hasPrivateKey())

    def test_rsa_key_parse_using_python(self):
        key = parsePEMKey(self.privRSAKey_str,
                private=True,
                implementations=["python"])

        self.assertIsInstance(key, RSAKey)
        self.assertEqual(1024, len(key))
        self.assertTrue(key.hasPrivateKey())

    def test_rsa_key_parse_with_new_lines_using_python(self):
        key = parsePEMKey(self.privRSAKey_str_newLines,
                private=True,
                implementations=["python"])

        self.assertIsInstance(key, RSAKey)
        self.assertEqual(1024, len(key))
        self.assertTrue(key.hasPrivateKey())

from certify_issuer.Issuer import Issuer
from certify_issuer.PdfIssuer import PdfIssuer


def test_issue():
    issuer = Issuer('0xcc546a88db1af7d250a2f20dee42ec436f99e075',
                    'https://node-testnet.corexchain.io', '0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730', 'test_user',
                    chain_id=3305)
    res = issuer.issue('', 'test', 0, '', 'a737d20b2e2a001bbf54c7edfcbffb015b0e67924e20f561c238ddaad6c4ed0e',
                       do_hash=True)
    print(res)


def test_pdf_issue():
    issuer = PdfIssuer('0xcc546a88db1af7d250a2f20dee42ec436f99e075',
                       'https://node-testnet.corexchain.io', '0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730', 'test_user',
                       chain_id=3305)
    res = issuer.issue_pdf('', '/home/surenbayar/Downloads/30/106-real-test.pdf',
                           '/home/surenbayar/Downloads/test2.pdf', 0, '', 'additional2',
                           'a737d20b2e2a001bbf54c7edfcbffb015b0e67924e20f561c238ddaad6c4ed0e')
    print(res)


def test_verify_pdf():
    issuer = PdfIssuer('0xcc546a88db1af7d250a2f20dee42ec436f99e075',
                       'https://node-testnet.corexchain.io', '0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730', 'test_user',
                       chain_id=3305)

    res = issuer.verify_pdf('/home/surenbayar/Downloads/test2.pdf')
    assert res['state'] == 'REVOKED'


def test_revoke_pdf():
    issuer = PdfIssuer('0xcc546a88db1af7d250a2f20dee42ec436f99e075',
                       'https://node-testnet.corexchain.io', '0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730', 'test_user',
                       chain_id=3305)

    res = issuer.revoke_pdf('/home/surenbayar/Downloads/test2.pdf', 'test',
                            'a737d20b2e2a001bbf54c7edfcbffb015b0e67924e20f561c238ddaad6c4ed0e')

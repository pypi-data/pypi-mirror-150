from libra_core import send_sms, send_mail


def test_send_smd():
    send_sms("测试", "13903813433")


def test_send_mail():
    send_mail("libra_core unit test", "libra_core unit test content", ["jiajia@apusapps.com"])

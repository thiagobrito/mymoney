import time
from pynubank import Nubank, NuException

nu = Nubank()
uuid, qr_code = nu.get_qr_code()
qr_code.print_ascii(invert=True)

authenticated = False
while not authenticated:
    try:
        r = nu.authenticate_with_qr_code('34026454835', 'aut55165', 'a78828f2-fc1b-4918-8013-792af34c17e8')
        authenticated = True
    except NuException:
        print('Failed...')
        authenticated = False
        time.sleep(5)

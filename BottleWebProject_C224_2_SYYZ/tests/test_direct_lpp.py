import unittest
import re
import direct_lpp

class test_F_mail(unittest.TestCase):
    def test_F(self):
        for mail in mails.uncorrect_mails:
            self.assertFalse(re.match(myform.reg, mail))

if __name__ == '__main__':
    unittest.main()
import os
import unittest
import siteUtils

class ParfileTestCase(unittest.TestCase):
    def setUp(self):
        "Write test parameter file that checks the casting mechanism."
        self.test_file = 'pars_test.txt'
        self.sections = ('Default', 'Case 1')
        self.values = {}
        self.values[self.sections[0]] = dict([('integer', 3),
                                              ('floating_point', 5e-4),
                                              ('string_value', 'foobar')])
        self.values[self.sections[1]] = dict([('integer', 5),
                                              ('floating_point', 126.1),
                                              ('string_value', 'test string')])
        output = open(self.test_file, 'w')
        for section in self.sections:
            output.write("[%s]\n" % section)
            for key, value in self.values[section].items():
                output.write("%s = %s\n" % (key, value))
        output.close()
    def tearDown(self):
        os.remove(self.test_file)
    def test_casting(self):
        for section in self.sections:
            pars = siteUtils.Parfile(self.test_file, section)
            for key, value in self.values[section].items():
                self.assertEquals(pars[key], value)

if __name__ == '__main__':
    unittest.main()

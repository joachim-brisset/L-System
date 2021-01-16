import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
lsys = __import__("l-system") # 'import l-system as lsys' not working because of the dash

import unittest

nextinput = ''
def input(): # redefine input function to handle user input
    return nextinput

class fileInputTest(unittest.TestCase):
    def test_defaultFile(self):
        ''' check if existing file is correctly returned '''
        self.assertTrue(lsys.inputFile(defaultFile=), os.getcwd() + "inputFileTest.py")

if __name__ == "__main__":
    unittest.main(verbosity=2)
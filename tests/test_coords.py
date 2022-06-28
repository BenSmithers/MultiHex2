from MultiHex2.core.coordinates import HexID

import unittest

class TestPathInits(unittest.TestCase):
    def test_build_HexIDs(self):
        ex = HexID(0,0)
        self.assertEqual(ex.zid, 0)

        ex2 = HexID(3,1)
        self.assertEqual(ex2.zid, -4)

        ex3 = ex+ex2
        self.assertEqual(ex3.xid, 3)
        self.assertEqual(ex3.yid, 1)

if __name__=="__main__":
    unittest.main()
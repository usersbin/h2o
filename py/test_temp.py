import os, json, unittest, time, shutil, sys
# not needed, but in case you move it down to subdir
sys.path.extend(['.','..'])
import h2o_cmd
import h2o
import h2o_browse as h2b

class Basic(unittest.TestCase):
    def tearDown(self):
        h2o.check_sandbox_for_errors()

    @classmethod
    def setUpClass(cls):
        h2o.build_cloud(node_count=3)

    @classmethod
    def tearDownClass(cls):
        h2o.tear_down_cloud()

    def test_A_Basic(self):
        # if any are wrong, dump node-ordered info from everyone, EC2 debug.
        expectedSize = len(h2o.nodes)
        cloudSizes = []
        for n in h2o.nodes:
            print h2o.dump_json(n.get_cloud())
            gc = n.get_cloud()
            cloudSizes.append(gc['cloud_size'])
        print cloudSizes
        csStr = ",".join(cloudSizes))
        print csStr
        for s in cloudSizes:
            self.assertEqual(s, expectedSize,
                "Inconsistent cloud size. nodes report %s instead of %d" % \
                (csStr, expectedSize))

    def test_B_RF_iris2(self):
        h2o_cmd.runRF(trees=6, timeoutSecs=10,
                csvPathname = h2o.find_file('smalldata/iris/iris2.csv'))

    def test_C_RF_poker100(self):
        h2o_cmd.runRF(trees=6, timeoutSecs=10,
                csvPathname = h2o.find_file('smalldata/poker/poker100'))

    def test_D_GenParity1(self):
        trees = 50
        h2o_cmd.runRF(trees=50, timeoutSecs=15, 
                csvPathname = h2o.find_file('smalldata/parity_128_4_100_quad.data'))

    def test_E_ParseManyCols(self):
        csvPathname=h2o.find_file('smalldata/fail1_100x11000.csv.gz')
        parseKey = h2o_cmd.parseFile(None, csvPathname, timeoutSecs=10)
        inspect = h2o_cmd.runInspect(None, parseKey['destination_key'], offset=-1, view=5)


if __name__ == '__main__':
    h2o.unit_main()
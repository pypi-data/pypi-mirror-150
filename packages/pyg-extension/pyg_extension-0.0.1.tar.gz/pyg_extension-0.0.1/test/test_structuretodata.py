import unittest

import numpy as np
from pymatgen.core import Structure

from pyg_extension.data.structuretodata import AddSAPymatgen, AddXPymatgen, AddXASE, StructureToData, AddXArray, \
    AddPBCEdgeDistance, AddPBCEdgeXYZ

data = Structure.from_file("POSCAR")
datas = [data]*10000


class MyTestCase(unittest.TestCase):
    def test_AddSAPymatgen(self):
        addsap = AddSAPymatgen()
        res = addsap.convert(data, y=None, state_attr=None)
        print(res)

    def test_AddSAPymatgen2(self):
        sub_converters = AddXPymatgen()
        addsap = AddSAPymatgen(sub_converters=[sub_converters])
        res = addsap.convert(data, y=None, state_attr=None)
        print(res)

    def test_AddXASE(self):
        sub_converters1 = AddSAPymatgen()
        sub_converters2 = AddXPymatgen()
        addsap = StructureToData(sub_converters=[sub_converters1,sub_converters2],n_jobs=3)
        # res = addsap.transform(datas, y=None, )
        res = addsap.transform(datas, y=None, state_attr=[3,4,5])
        print(res)

    def test_AddXArray(self):
        array = np.random.random((120,10))
        sub_converters1 = AddXASE()
        sub_converters2 = AddXPymatgen()
        sub_converters3 = AddXArray(array)
        sub_converters4 = AddSAPymatgen()
        addsap = StructureToData(sub_converters=[sub_converters1, sub_converters2,sub_converters3,sub_converters4],n_jobs=1)
        # res = addsap.transform(datas, y=None, )
        res = addsap.transform(datas, y=None, state_attr=[3, 4, 5])
        print(res)

    def test_AddPBCEdgeDistance(self):

        addsap = StructureToData(sub_converters=[AddXPymatgen(), AddSAPymatgen(), AddPBCEdgeXYZ()],n_jobs=4)
        res = addsap.transform_and_save(datas)
        print(res)


if __name__ == '__main__':
    unittest.main()

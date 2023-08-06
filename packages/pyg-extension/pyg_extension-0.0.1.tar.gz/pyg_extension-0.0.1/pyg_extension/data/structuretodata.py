# -*- coding: utf-8 -*-

# @Time  : 2022/5/9 17:46
# @Author : boliqq07
# @Software: PyCharm
# @License: MIT License

"""
Abstract classes for building graph representations consist with ``pytorch-geometric``.

All the Graph in this part should return data as following:

Each Graph data (for each structure):

``x``: Node feature matrix. np.ndarray, with shape [num_nodes, num_node_features]

``pos``: Node position matrix. np.ndarray, with shape [num_nodes, num_dimensions]

``y``: target. np.ndarray, shape (1, num_target) , default shape (1,)

``z``: atom numbers. np.ndarray, with shape [num_nodes,]

``state_attr``: state feature. np.ndarray, shape (1, num_state_features)

``edge_index``: Graph connectivity in COO format. np.ndarray, with shape [2, num_edges] and type torch.long

``edge_attr``: Edge feature matrix. np.ndarray,  with shape [num_edges, num_edge_features]

Where the state_attr is added newly.

"""
import itertools
import math
import os
from shutil import rmtree
from typing import List, Iterable, Union

import ase.data as ase_data
import numpy as np
import torch
from pymatgen.core import Structure, Element
from pymatgen.optimization.neighbors import find_points_in_spheres
from torch_geometric.data import Data

from mgetool.tool import parallelize, batch_parallelize, time_this_function, tt


def data_merge(data_sub:List[Data], merge_key=None):
    if merge_key is None:
        merge_key = ["state_attr", "edge_attr", "x"]
    data_base = data_sub[0]
    for di in data_sub[1:]:
        ks = di.keys
        for k in ks:
            v = getattr(di, k)
            if v is not None:
                if k not in merge_key:
                    data_base.__setattr__(k, v)
                else:
                    if not hasattr(data_base, k):
                        data_base.__setattr__(k, v)
                    elif isinstance(getattr(data_base, k), torch.Tensor) and isinstance(v, torch.Tensor):
                        v_base = getattr(data_base, k)
                        v_base_s = len(v_base.shape)
                        v_s = len(v.shape)
                        if v_base_s==0 or v_s==0 or all((v_base_s==1,v_s==1)):
                            data_base.__setattr__(k, torch.cat([v_base.flatten(), v.flatten()]))
                        elif all((v_base_s>=2,v_s>=2)) and v_base.shape[0]==v_base.shape[0]:
                            data_base.__setattr__(k, torch.cat([v_base, v],dim=1))
                        else:
                            data_base.__setattr__(k, v)
                    else:
                        data_base.__setattr__(k, v)
    return data_base


class StructureToData:
    def __init__(self, sub_converters: List = None, merge_key=None, n_jobs: int = 1,
                 batch_calculate: bool = True,
                 batch_size: int = 30):
        self.n_jobs = n_jobs
        self.batch_calculate = batch_calculate
        self.batch_size = batch_size
        self.sub_converters = sub_converters
        self.merge_key = merge_key

    def __call__(self, *args, **kwargs):
        return self.convert(*args, **kwargs)

    def convert(self, data: Structure, y=None, state_attr=None, **kwargs) -> Data:
        """

        Args:
            data: (Structure)
            y: (float,int)
            state_attr: (float,int,np.ndarray)
            **kwargs: kwargs are just applied on main converter ranther than the subconverters

        Returns:
            data:(Data),pyg Data

        """
        if self.sub_converters is None:
            return self._convert(data, y=y, state_attr=state_attr, **kwargs)
        else:
            data_sub = [ci.convert(data, y=y, state_attr=state_attr,**kwargs) for ci in self.sub_converters]
            data = self._convert(data, y=y, state_attr=state_attr, **kwargs)
            data_sub.append(data)
            data_base = data_merge(data_sub)
            return data_base

    def transform(self, structures: List[Structure], **kwargs) -> List[Data]:
        """

        Args:
            structures:(list) Preprocessing of samples need to transform to Graph.
            state_attr: (list)
                preprocessing of samples need to add to Graph.
            y: (list)
                Target to train against (the same size with structure)

            **kwargs:

        Returns:
            list of graphs:
                List of dict

        """
        assert isinstance(structures, Iterable)
        if hasattr(structures, "__len__"):
            assert len(structures) > 0, "Empty input data!"

        le = len(structures)

        for i in kwargs.keys():
            if kwargs[i] is None:
                kwargs[i] = [kwargs[i]] * len(structures)
            elif not isinstance(kwargs[i], Iterable):
                kwargs[i] = [kwargs[i]] * len(structures)

        try:
            kw = [{k: v[i] for k, v in kwargs.items()} for i in range(le)]
        except  IndexError as e:
            print(e)
            raise IndexError("Make sure the other parameters such as y and state_attr"
                             " are with same number (length) of structure.")

        iterables = zip(structures, kw)

        if not self.batch_calculate:
            rets = parallelize(self.n_jobs, self.convert, iterables, tq=True, respective=True,
                               respective_kwargs=True)

        else:
            rets = batch_parallelize(self.n_jobs, self.convert, iterables, respective=True,
                                     respective_kwargs=True,
                                     tq=True, mode="j", batch_size=self.batch_size)

        return rets

    def check_dup(self, structures, file_names="composition_name"):
        """Check the names duplication"""
        names = [i.composition.reduced_formula for i in structures]
        if file_names == "composition_name" and len(names) != len(set(names)):
            raise KeyError("There are same composition name for different structure, "
                           "please use file_names='rank_number' "
                           "to definition or specific names list.")
        elif len(set(file_names)) == len(structures):
            return file_names
        elif file_names == "rank_number":
            return ["raw_data_{}".format(i) for i in range(len(structures))]
        else:
            return names

    def save(self, obj, name, root_dir=".") -> None:
        """Save."""
        torch.save(obj, os.path.join(root_dir, "raw", '{}.pt'.format(name)))

    def transform_and_save(self, data, y=None, state_attr=None, root_dir=".",
                           file_names="composition_name", save_mode="o", **kwargs):
        r"""Save the data to 'root_dir/raw' if save_mode="i", else 'root_dir', compact with InMemoryDatasetGeo"""
        raw_path = os.path.join(root_dir, "raw")
        if os.path.isdir(raw_path):
            rmtree(raw_path)
        os.makedirs(raw_path)

        result = self.transform(data, y=y, state_attr=state_attr,  **kwargs)
        print("Save raw files to {}.".format(raw_path))
        if save_mode in ["i", "r", "respective"]:
            fns = self.check_dup(data, file_names=file_names)
            [self.save(i, j, root_dir) for i, j in zip(result, fns)]
        else:
            self.save(result, "raw_data", root_dir=root_dir)
        print("Done.")
        return result


    @staticmethod
    def _convert(data: Structure, y=None, state_attr=None, **kwargs) -> Data:
        z = torch.tensor(list(data.atomic_numbers))
        pos = torch.from_numpy(data.cart_coords)
        if state_attr is not None:
            state_attr = torch.tensor(state_attr)
        if y is not None:
            y = torch.tensor(y)

        for key, value in kwargs.items():
            try:
                kwargs[key] = torch.tensor(value)
            except ValueError:
                pass

        return Data(y=y, pos=pos, z=z, state_attr=state_attr, **kwargs)


class AddSAPymatgen(StructureToData):
    """
    Add state_attr.
    pymatgen's structure.num_sites, structure.ntypesp, structure.density, structure.volume"""

    def __init__(self, *args, prop_name=None, **kwargs):
        if prop_name is None:
            self.prop_name = ['num_sites', 'ntypesp', 'density', 'volume']
        super(AddSAPymatgen, self).__init__(*args, **kwargs)

    @staticmethod
    def _convert(data: Structure, **kwargs) -> Data:
        state_attr = torch.tensor([data.num_sites, data.ntypesp, data.density, data.volume])
        return Data(state_attr=state_attr)


class AddXPymatgen(StructureToData):
    """
    Add x.

    Get pymatgen element preprocessing.
    prop_name = [
    "atomic_radius",
    "atomic_mass",
    "number",
    "max_oxidation_state",
    "min_oxidation_state",
    "row",
    "group",
    "atomic_radius_calculated",
    "mendeleev_no",
    "average_ionic_radius",
    "average_cationic_radius",
    "average_anionic_radius",]
    """

    def __init__(self, *args, prop_name=None, **kwargs):
        super(AddXPymatgen, self).__init__(*args, **kwargs)
        if prop_name is None:
            self.prop_name = ["atomic_mass","average_ionic_radius","average_anionic_radius","atomic_radius_calculated"]
        self.da = [Element.from_Z(i) for i in range(1, 119)]
        self.da.insert(0, self.da[0])  # for start from 1

    def _convert(self,data: Structure, **kwargs) -> Data:
        x = torch.tensor([[getattr(self.da[i], pi) for pi in self.prop_name] for i in data.atomic_numbers])
        return Data(x=x)


class AddXASE(StructureToData):
    """
    Add x.

    Get pymatgen element preprocessing.
    prop_name = [
    'vdw_radii', 'reference_states', 'atomic_masses', 'covalent_radii'
    ]
    """

    def __init__(self, *args, prop_name=None, **kwargs):
        super(AddXASE, self).__init__(*args, **kwargs)
        if prop_name is None:
            self.prop_name = ['atomic_masses', 'covalent_radii']
        arrays = np.concatenate([getattr(ase_data, i).reshape(-1, 1) for i in self.prop_name], axis=1)
        self.arrays = torch.from_numpy(arrays)

    def _convert(self, data: Structure, **kwargs) -> Data:
        x = self.arrays[data.atomic_numbers, :]
        return Data(x=x)


class AddXArray(StructureToData):
    """
    Add x by np.array (2D).
    The array are insert in 0 position automatically in code.

    """

    def __init__(self, array:np.ndarray, *args, **kwargs):
        super(AddXArray, self).__init__(*args, **kwargs)
        if array.ndim==1:
            array = array.reshape(-1,1)
        array = np.concatenate((array[0,:].reshape(1,-1),array),axis=0)
        self.arrays = torch.from_numpy(array)

    def _convert(self, data: Structure, **kwargs) -> Data:
        x = self.arrays[data.atomic_numbers, :]
        return Data(x=x)


def _re_pbc(pbc: Union[bool, List[bool], np.ndarray], return_type="bool"):
    if pbc is True:
        pbc = [1, 1, 1]
    elif pbc is False:
        pbc = [0, 0, 0]
    elif isinstance(pbc, Iterable):
        pbc = [1 if i is True or i == 1 else 0 for i in pbc]
    else:
        raise TypeError("Can't accept {}".format(pbc))
    if return_type == "bool":
        pbc = np.array(pbc) == 1
    else:
        pbc = np.array(pbc)
    return pbc


def _get_r_in_spheres(data,pbc=True, cutoff=5.0,numerical_tol=1e-6):
    if isinstance(data, Structure):
        lattice_matrix = np.ascontiguousarray(np.array(data.lattice.matrix), dtype=float)
        if pbc is not False:
            pbc = _re_pbc(pbc, return_type="int")
        else:
            pbc = np.array([0, 0, 0])
    else:
        raise ValueError("structure type not supported")

    r = float(cutoff)
    cart_coords = np.ascontiguousarray(np.array(data.cart_coords), dtype=float)
    center_indices, neighbor_indices, images, distances = find_points_in_spheres(
        cart_coords, cart_coords, r=r, pbc=pbc, lattice=lattice_matrix, tol=numerical_tol
    )
    center_indices = center_indices.astype(np.int64)
    neighbor_indices = neighbor_indices.astype(np.int64)
    # images = images.astype(np.int64)
    distances = distances.astype(np.float32)
    exclude_self = (distances > numerical_tol)
    # exclude_self = (center_indices != neighbor_indices) | (distances > numerical_tol)
    center_indices = center_indices[exclude_self]
    neighbor_indices = neighbor_indices[exclude_self]
    distances = distances[exclude_self]
    return center_indices, neighbor_indices, distances,None


def _get_xyz_in_spheres(data, pbc=True, cutoff=5.0, numerical_tol=1e-6):
    if isinstance(data, Structure):
        lattice_matrix = np.ascontiguousarray(np.array(data.lattice.matrix), dtype=float)
        if pbc is not False:
            pbc = _re_pbc(pbc, return_type="int")
        else:
            pbc = np.array([0, 0, 0])
    else:
        raise ValueError("structure type not supported")
    r = float(cutoff)
    cart_coords = np.ascontiguousarray(np.array(data.cart_coords), dtype=float)
    center_indices, neighbor_indices, images, distances = find_points_in_spheres(
        cart_coords, cart_coords, r=r, pbc=pbc, lattice=lattice_matrix, tol=numerical_tol
    )
    center_indices = center_indices.astype(np.int64)
    neighbor_indices = neighbor_indices.astype(np.int64)
    images = images.astype(np.int64)
    distances = distances.astype(np.float32)
    exclude_self = (distances > numerical_tol)

    center_indices = center_indices[exclude_self]
    neighbor_indices = neighbor_indices[exclude_self]
    distances = distances[exclude_self]
    images = images[exclude_self]

    offset = np.dot(images, data.lattice.matrix)

    coords = cart_coords[neighbor_indices, :] - cart_coords[center_indices, :]
    xyz = offset+coords

    return center_indices, neighbor_indices, distances, xyz


class AddPBCEdgeDistance(StructureToData):
    """
    Add Edge with PBC.
    make sure

    Get pymatgen element preprocessing.
    prop_name = [
    'vdw_radii', 'reference_states', 'atomic_masses', 'covalent_radii'
    ]
    """

    def __init__(self, *args, cutoff: float = 5.0,
                 numerical_tol: float = 1e-6,
                 pbc=True, **kwargs):

        """
        Get graph representations from structure within cutoff.

        Args:
            structure (pymatgen Structure or molecule)
            cutoff (float): cutoff radius
            numerical_tol (float): numerical tolerance
            nn_strategy(str,None):not used
        Returns:
            center_indices, neighbor_indices, distances
        """
        super(AddPBCEdgeDistance, self).__init__(*args, **kwargs)
        self.numerical_tol = numerical_tol
        self.pbc = pbc
        self.cutoff = cutoff

    def _convert(self, data: Structure, **kwargs) -> Data:

        center_indices,neighbor_indices,distances,_= _get_r_in_spheres(data, pbc=self.pbc,
                                                                     cutoff=self.cutoff,
                                                                     numerical_tol=self.numerical_tol)

        edge_index = torch.vstack([torch.from_numpy(center_indices),
                                   torch.from_numpy(neighbor_indices)])
        edge_weight = torch.from_numpy(distances)

        return Data(edge_index=edge_index, edge_weight=edge_weight)


class AddPBCEdgeXYZ(StructureToData):
    """
    Add x.
    make sure.

    Get pymatgen element preprocessing.
    prop_name = [
    'vdw_radii', 'reference_states', 'atomic_masses', 'covalent_radii'
    ]
    """

    def __init__(self, *args, cutoff: float = 5.0,
                 numerical_tol: float = 1e-6,
                 pbc=True, **kwargs):

        """
        Get graph representations from structure within cutoff.

        Args:
            structure (pymatgen Structure or molecule)
            cutoff (float): cutoff radius
            numerical_tol (float): numerical tolerance
            nn_strategy(str,None):not used
        Returns:
            center_indices, neighbor_indices, distances
        """
        super(AddPBCEdgeXYZ, self).__init__(*args, **kwargs)
        self.numerical_tol = numerical_tol
        self.pbc = pbc
        self.cutoff = cutoff

    def _convert(self, data: Structure, **kwargs) -> Data:

        center_indices, neighbor_indices, distances, xyz = _get_xyz_in_spheres(data, pbc=self.pbc,
                                                                     cutoff=self.cutoff,
                                                                     numerical_tol=self.numerical_tol)

        edge_index = torch.vstack([torch.from_numpy(center_indices),
                                   torch.from_numpy(neighbor_indices)])
        edge_weight = torch.from_numpy(distances)
        edge_attr = torch.from_numpy(xyz)

        return Data(edge_index=edge_index,edge_weight=edge_weight, edge_attr=edge_attr)

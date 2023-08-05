import os
import numpy as np
import pytest
import mikeio
from mikeio import Dfsu, Mesh
from mikeio.spatial.FM_geometry import (
    GeometryFM,
    GeometryFM3D,
    GeometryFMVerticalColumn,
)
from mikeio.spatial.geometry import GeometryPoint3D


def test_read_simple_3d():
    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    ds = mikeio.read(filename)

    assert ds.to_numpy().shape[0] == 3
    assert len(ds.items) == 3

    assert ds.items[0].name != "Z coordinate"
    assert ds.items[2].name == "W velocity"


def test_read_simple_2dv():
    filename = os.path.join("tests", "testdata", "basin_2dv.dfsu")
    dfs = Dfsu(filename)

    ds = dfs.read()

    assert ds.to_numpy().shape[0] == 3
    assert len(ds.items) == 3

    assert ds.items[0].name != "Z coordinate"
    assert ds.items[2].name == "W velocity"


def test_read_returns_correct_items_sigma_z():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = Dfsu(filename)

    ds = dfs.read()

    assert len(ds) == 2
    assert ds.items[0].name == "Temperature"
    assert ds.items[1].name == "Salinity"


def test_read_top_layer():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    ds = dfs.read()  # all data in file
    dstop1 = ds.sel(layers="top")

    dstop2 = dfs.read(layers="top")
    assert dstop1.shape == dstop2.shape
    assert dstop1.dims == dstop2.dims
    assert isinstance(dstop1.geometry, GeometryFM)
    assert dstop1.geometry._type == dstop2.geometry._type
    assert np.all(dstop1.values == dstop2.values)
    assert dstop1.geometry.max_nodes_per_element <= 4


def test_read_bottom_layer():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    ds = dfs.read()  # all data in file
    dsbot1 = ds.sel(layers="bottom")

    dsbot2 = dfs.read(layers="bottom")
    assert dsbot1.shape == dsbot2.shape
    assert dsbot1.dims == dsbot2.dims
    assert isinstance(dsbot1.geometry, GeometryFM)
    assert dsbot1.geometry._type == dsbot2.geometry._type
    assert np.all(dsbot1.values == dsbot2.values)
    assert dsbot1.geometry.max_nodes_per_element <= 4


def test_read_single_step_bottom_layer():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    ds = dfs.read(time=-1)  # Last timestep
    dsbot1 = ds.sel(layers="bottom")


def test_read_multiple_layers():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    ds = dfs.read()  # all data in file
    dstop1 = ds.sel(layers=[-3, -2, -1])

    dstop2 = dfs.read(layers=[-3, -2, -1])
    assert dstop1.shape == dstop2.shape
    assert dstop1.dims == dstop2.dims
    assert isinstance(dstop1.geometry, GeometryFM3D)
    assert dstop1.geometry._type == dstop2.geometry._type
    assert np.all(dstop1.values == dstop2.values)
    assert dstop1.geometry.max_nodes_per_element >= 6


def test_read_dfsu3d_area():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    bbox = [350000, 6192000, 380000, 6198000]

    ds = dfs.read()  # all data in file
    assert ds.geometry.contains((350000, 6192000))

    dsa1 = ds.sel(area=bbox)
    assert not dsa1.geometry.contains((350000, 6192000))
    assert dsa1.geometry.n_layers > 1

    dsa2 = dfs.read(area=bbox)
    assert dsa1.shape == dsa2.shape
    assert dsa1.dims == dsa2.dims
    assert dsa1.geometry._type == dsa2.geometry._type
    assert np.all(dsa1.values == dsa2.values)


def test_read_dfsu3d_column():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    (x, y) = (333934.1, 6158101.5)

    ds = dfs.read()  # all data in file
    dscol1 = ds.sel(x=x, y=y)
    assert isinstance(dscol1.geometry, GeometryFMVerticalColumn)
    assert dscol1.geometry.n_layers == 4
    assert dscol1.geometry.n_elements == 4
    assert dscol1.geometry.n_nodes == 5 * 3
    assert dscol1._zn.shape == (ds.n_timesteps, 5 * 3)

    dscol2 = dfs.read(x=x, y=y)
    assert isinstance(dscol2.geometry, GeometryFMVerticalColumn)
    assert dscol1.shape == dscol2.shape
    assert dscol1.dims == dscol2.dims
    assert dscol1.geometry._type == dscol2.geometry._type
    assert np.all(dscol1.values == dscol2.values)
    assert dscol2._zn.shape == (ds.n_timesteps, 5 * 3)


def test_read_dfsu3d_xyz():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    (x, y, z) = (333934.1, 6158101.5, -5)

    ds = dfs.read()  # all data in file
    dspt1 = ds.sel(x=x, y=y, z=z)
    assert isinstance(dspt1.geometry, GeometryPoint3D)

    dspt2 = dfs.read(x=x, y=y, z=z)
    assert isinstance(dspt2.geometry, GeometryPoint3D)
    assert dspt1.shape == dspt2.shape
    assert dspt1.dims == dspt2.dims
    assert np.all(dspt1.values == dspt2.values)

    dspt3 = dfs.read(time=-1, x=x, y=y, z=z)
    assert dspt3.dims == ()
    assert dspt3[0].values == dspt1[0].values[-1]
    # 20.531237


def test_read_column_select_single_time_plot():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    x, y = 333934.1, 6158101.5

    dsp = dfs.read(x=x, y=y)
    sal_prof = dsp.Salinity.isel(time=0)
    sal_prof.plot()
    sal_prof.plot.line()


def test_read_column_interp_time_and_select_time():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = mikeio.open(filename)

    x, y = 333934.1, 6158101.5

    dscol = dfs.read(x=x, y=y)
    dscol_t = dscol.isel(time=0)

    assert "time" not in dscol_t.dims

    dscol_et = dscol.sel(time=dfs.end_time)

    assert "time" not in dscol_et.dims

    ds_15m = dscol.interp_time(dt=900)

    da = ds_15m.Salinity

    salinity_it = da.isel(time=0)  # single time-step
    assert salinity_it.n_timesteps == 1

    salinity_st = da.sel(time="1997-09-15 23:00")  # single time-step
    assert salinity_st.n_timesteps == 1

    with pytest.raises(IndexError):
        # not in time
        da.sel(time="1997-09-15 00:00")


def test_number_of_nodes_and_elements_sigma_z():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = Dfsu(filename)

    assert dfs.n_elements == 17118
    assert dfs.n_nodes == 12042


def test_calc_element_coordinates_3d():
    filename = "tests/testdata/oresund_sigma_z.dfsu"
    dfs = Dfsu(filename)

    # extract dynamic z values for profile
    elem_ids = dfs.find_nearest_profile_elements(333934.1, 6158101.5)
    ds = dfs.read(items=0, elements=elem_ids, time=0)
    zn_dyn = ds[0]._zn  # TODO
    ec = dfs.calc_element_coordinates(elements=elem_ids, zn=zn_dyn)

    assert ec[0, 2] == pytest.approx(-6.981768845)


def test_find_nearest_elements_3d():
    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)

    elem_id = dfs.find_nearest_elements(333934, 6158101)
    assert elem_id == 5323
    assert elem_id in dfs.top_elements

    elem_id = dfs.find_nearest_elements(333934, 6158101, layer=7)
    assert elem_id == 5322

    elem_id = dfs.find_nearest_elements(333934, 6158101, -7)
    assert elem_id == 5320


def test_read_and_select_single_element_dfsu_3d():

    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)

    ds = dfs.read()

    selds = ds.isel(idx=1739, axis=1)

    assert selds[0].shape == (3,)


def test_n_layers():

    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_layers == 10

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_layers == 9

    filename = os.path.join("tests", "testdata", "oresund_vertical_slice.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_layers == 9

    filename = "tests/testdata/HD2D.dfsu"
    dfs = Dfsu(filename)
    assert not hasattr(dfs, "n_layers")


def test_n_sigma_layers():

    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_sigma_layers == 10

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_sigma_layers == 4

    filename = os.path.join("tests", "testdata", "oresund_vertical_slice.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_sigma_layers == 4

    filename = "tests/testdata/HD2D.dfsu"
    dfs = Dfsu(filename)
    assert not hasattr(dfs, "n_sigma_layers")


def test_n_z_layers():

    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_z_layers == 0

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_z_layers == 5

    filename = os.path.join("tests", "testdata", "oresund_vertical_slice.dfsu")
    dfs = Dfsu(filename)
    assert dfs.n_z_layers == 5

    filename = "tests/testdata/HD2D.dfsu"
    dfs = Dfsu(filename)
    assert not hasattr(dfs, "n_z_layers")


def test_boundary_codes():

    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.boundary_codes) == 1

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)

    assert len(dfs.boundary_codes) == 3


def test_top_elements():
    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.top_elements) == 174
    assert dfs.top_elements[3] == 39

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.top_elements) == 3700
    assert dfs.top_elements[3] == 16

    filename = os.path.join("tests", "testdata", "oresund_vertical_slice.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.top_elements) == 99
    assert dfs.top_elements[3] == 19

    filename = "tests/testdata/HD2D.dfsu"
    dfs = Dfsu(filename)
    assert not hasattr(dfs, "top_elements")


def test_bottom_elements():
    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.bottom_elements) == 174
    assert dfs.bottom_elements[3] == 30

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.bottom_elements) == 3700
    assert dfs.bottom_elements[3] == 13

    filename = os.path.join("tests", "testdata", "oresund_vertical_slice.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.bottom_elements) == 99
    assert dfs.bottom_elements[3] == 15

    filename = "tests/testdata/HD2D.dfsu"
    dfs = Dfsu(filename)
    assert not hasattr(dfs, "bottom_elements")


def test_n_layers_per_column():
    filename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.n_layers_per_column) == 174
    assert dfs.n_layers_per_column[3] == 10

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.n_layers_per_column) == 3700
    assert dfs.n_layers_per_column[3] == 4
    assert max(dfs.n_layers_per_column) == dfs.n_layers

    filename = os.path.join("tests", "testdata", "oresund_vertical_slice.dfsu")
    dfs = Dfsu(filename)
    assert len(dfs.n_layers_per_column) == 99
    assert dfs.n_layers_per_column[3] == 5

    filename = "tests/testdata/HD2D.dfsu"
    dfs = Dfsu(filename)
    assert not hasattr(dfs, "n_layers_per_column")


def test_get_layer_elements():
    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)

    elem_ids = dfs.get_layer_elements(-1)
    assert np.all(elem_ids == dfs.top_elements)

    elem_ids = dfs.get_layer_elements(-2)
    assert elem_ids[5] == 23

    elem_ids = dfs.get_layer_elements(0)
    assert elem_ids[5] == 8638
    assert len(elem_ids) == 10

    elem_ids = dfs.get_layer_elements([0, 2])
    assert len(elem_ids) == 197

    with pytest.raises(Exception):
        elem_ids = dfs.get_layer_elements(11)


def test_find_nearest_profile_elements():
    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    elem_ids = dfs.find_nearest_profile_elements(358337, 6196090)
    assert len(elem_ids) == 8
    assert elem_ids[-1] == 3042


def test_get_element_area_3D():
    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    areas = dfs.get_element_area()
    assert areas[0] == 350186.43530453625


def test_write_from_dfsu3D(tmpdir):

    sourcefilename = os.path.join("tests", "testdata", "basin_3d.dfsu")
    outfilename = os.path.join(tmpdir.dirname, "simple3D.dfsu")
    dfs = Dfsu(sourcefilename)

    ds = dfs.read(items=[0, 1])

    dfs.write(outfilename, ds)

    assert os.path.exists(outfilename)


def test_extract_top_layer_to_2d(tmpdir):
    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")

    dfs = Dfsu(filename)
    top_ids = dfs.top_elements

    ds = dfs.read(elements=top_ids)

    outfilename = os.path.join(tmpdir, "toplayer.dfsu")
    dfs.write(outfilename, ds, elements=top_ids)

    newdfs = Dfsu(outfilename)
    assert os.path.exists(outfilename)

    assert newdfs.is_2d


def test_modify_values_in_layer(tmpdir):

    ds = mikeio.read("tests/testdata/oresund_sigma_z.dfsu")
    selected_layer = 6  # Zero-based indexing!
    layer_elem_ids = ds.geometry.get_layer_elements(selected_layer)

    ds.Salinity[:, layer_elem_ids] = 35.0  # Set values

    outfilename = os.path.join(tmpdir, "oresund_modified.dfsu")

    ds.to_dfs(outfilename)

    ds_sel_layer = mikeio.read(outfilename, layers=selected_layer)
    assert np.all(np.isclose(ds_sel_layer.Salinity.to_numpy(), 35.0))


def test_to_mesh_3d(tmpdir):

    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")

    dfs = Dfsu(filename)

    outfilename = os.path.join(tmpdir, "oresund.mesh")

    dfs.to_mesh(outfilename)

    assert os.path.exists(outfilename)

    mesh = Mesh(outfilename)

    assert True


def test_extract_surface_elevation_from_3d():
    dfs = Dfsu("tests/testdata/oresund_sigma_z.dfsu")
    outputfile = "tests/testdata/oresund_surface_elev_extracted.dfsu"
    n_top1 = len(dfs.top_elements)

    dfs.extract_surface_elevation_from_3d(outputfile, time=-1)

    dfs2 = Dfsu(outputfile)
    assert dfs2.n_elements == n_top1
    os.remove(outputfile)  # clean up


def test_find_nearest_element_in_Zlayer():
    filename = os.path.join("tests", "testdata", "oresund_sigma_z.dfsu")
    dfs = Dfsu(filename)
    el2dindx = dfs.elem2d_ids[12]
    assert el2dindx == 2
    ids = dfs.find_nearest_elements(357000, 6200000, layer=0)
    el2dindx = dfs.elem2d_ids[ids]
    table = dfs.e2_e3_table[el2dindx]
    assert ids == 3216
    assert el2dindx == 745
    assert len(table) == 9
    ids = dfs.find_nearest_elements(357000, 6200000, layer=8)
    el2dindx = dfs.elem2d_ids[ids]
    table = dfs.e2_e3_table[el2dindx]
    assert ids == 3224
    assert el2dindx == 745
    assert len(table) == 9

    with pytest.raises(Exception):
        # z and layer cannot both be given
        dfs.find_nearest_elements(357000, 6200000, z=-3, layer=8)


def test_dataset_write_dfsu3d(tmp_path):

    outfilename = tmp_path / "oresund_sigma_z.dfsu"
    ds = mikeio.read("tests/testdata/oresund_sigma_z.dfsu", time=[0, 1])
    ds.to_dfs(outfilename)

    ds2 = mikeio.read(outfilename)
    assert ds2.n_timesteps == 2


def test_dataset_write_dfsu3d_max(tmp_path):

    outfilename = tmp_path / "oresund_sigma_z.dfsu"
    ds = mikeio.read("tests/testdata/oresund_sigma_z.dfsu")
    assert ds._zn is not None
    ds_max = ds.max("time")
    assert ds_max._zn is not None
    ds_max.to_dfs(outfilename)

    ds2 = mikeio.read(outfilename)
    assert ds2.n_timesteps == 1
    assert ds2.geometry.is_layered

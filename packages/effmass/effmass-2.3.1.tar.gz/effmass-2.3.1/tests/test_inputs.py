#! /usr/bin/env python3
import pytest
# using pytest-lazy-fixture plugin
import numpy as np
from effmass import inputs
from effmass import kt_to_ev
import math

@pytest.mark.parametrize("settings_object,extrema_search_depth,energy_range",[
	(pytest.lazy_fixture('MAPI_settings_object'), 0.025, 0.25),
])
def test_settings(settings_object,extrema_search_depth,energy_range):
	assert settings_object.extrema_search_depth==extrema_search_depth
	assert settings_object.energy_range==energy_range

@pytest.mark.parametrize("data_object,CBM,VBM,fermi_energy", [
	(pytest.lazy_fixture('MAPI_cl_data_object'), 3.28781692, 1.2556844599999999,(3.28781692+1.2556844599999999)/2 ),
	(pytest.lazy_fixture('MAPI_soc_data_object'), 2.29063902, 1.4189758400000001,(2.29063902 +1.4189758400000001)/2),
        (pytest.lazy_fixture('Ge_SP_data_object'),5.50690368,5.23191533,(5.23191533+5.50690368)/2),
        (pytest.lazy_fixture('Ge_sp_aims_data_object'), 0.00082, -0.0027, (0.00082-0.0027)/2),
        (pytest.lazy_fixture('Ge_nsp_aims_data_object'), 0.02619, 0.01512, (0.02619+0.01512)/2),
        (pytest.lazy_fixture('Ge_soc_aims_data_object'), 0.00531, -0.01667, (0.00531-0.01667)/2),
        (pytest.lazy_fixture('Si_nsp_data_object'), 2.40429888498042, 1.284889194542445, 1.2881053080765)
])
def test_data(data_object,CBM,VBM,fermi_energy):
	# note that there is testing done after parsing from PROCAR within the VASPPY module
    assert math.isclose(data_object.CBM,CBM,rel_tol=1e-5)
    assert math.isclose(data_object.VBM,VBM,rel_tol=1e-5)
    assert math.isclose(data_object.fermi_energy,fermi_energy,rel_tol=1e-5)

@pytest.mark.parametrize("data_object,num_points,dos_f3,integrated_dos_f3", [
	(pytest.lazy_fixture('MAPI_soc_data_object_with_DOSCAR'),301,np.array([[ -2.26430000e+01,   0.00000000e+00],[ -2.25120000e+01,   0.00000000e+00],[ -2.23810000e+01,   0.00000000e+00]]),np.array([[ -2.26430000e+01,   0.00000000e+00],[ -2.25120000e+01,   0.00000000e+00],[ -2.23810000e+01,   0.00000000e+00]])),
])
def test_parse_DOSCAR(data_object,num_points,dos_f3,integrated_dos_f3):
    assert len(data_object.dos) == num_points
    assert len(data_object.integrated_dos) == num_points
    assert np.allclose(data_object.dos[:3],dos_f3)
    assert np.allclose(data_object.integrated_dos[:3],integrated_dos_f3)
    

# This file is part of PyCosmo, a multipurpose cosmology calculation tool in Python.
#
# Copyright (C) 2013-2021 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.

import os

import numpy as np
import pytest

import PyCosmo
from PyCosmo.PerturbationTable import optimize_grid

__author__ = "Andrina"
"""
Test the Obs module.

"""


@pytest.fixture
def cosmo_icosmo_w1(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_icosmo_w-1_param.ini"))
    yield c


@pytest.fixture
def cosmo_icosmo_w095(data_path):
    c = PyCosmo.build("wcdm")
    c.load_params(data_path("param_files/PyCosmo_icosmo_w-095_param.ini"))
    yield c


@pytest.fixture
def cosmo_camb_p13(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_param_planck2013-hand.ini"))
    yield c


@pytest.fixture
def cosmo_icosmo_cosmo1(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_icosmo_cosmo1_param.ini"))
    yield c


@pytest.fixture
def cosmo_cosmo0(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_cosmo0_param.ini"))
    c.set(mpc=3.086e22, msun=1.9885e30)
    yield c


@pytest.fixture
def obs():
    return PyCosmo.Obs()


def _get_abspath(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def test_cl_weak_lensing_regression(obs, cosmo_cosmo0):

    ells = [10, 3000, 12000]

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.03, 1, 5.0]),
        "A_IA": 0.0,
        "z0_IA": 0.0,
        "eta_IA": 0.0,
    }

    cosmo_cosmo0.set(tabulation="off")
    cl = obs.cl(ells, cosmo_cosmo0, clparams)
    tobe = np.array([1.98184110e-08, 3.46589943e-11, 2.10148620e-12])
    assert np.allclose(cl, tobe, atol=0, rtol=2e-9)

    cl, cl_2 = obs.cl_multi(ells, cosmo_cosmo0, [clparams, clparams])

    assert np.all(cl == cl_2)
    assert np.allclose(cl, tobe, atol=0, rtol=2e-9)

    cosmo_cosmo0.set(tabulation="bao")
    cl, cl_2 = obs.cl_multi(ells, cosmo_cosmo0, [clparams, clparams])
    assert np.all(cl == cl_2)
    assert np.allclose(cl, tobe, atol=0, rtol=1e-3)

    k_init = np.logspace(-5, 2, 2000)
    cosmo_cosmo0.set(tabulation="off")
    k_optim, *_ = optimize_grid(cosmo_cosmo0.lin_pert, k_init, 1e-4, 10)

    cosmo_cosmo0.set(tabulation="manual", tabulation_k_grid=k_init)
    cl_ip = obs.cl(ells, cosmo_cosmo0, clparams)

    cosmo_cosmo0.set(tabulation="manual", tabulation_k_grid=k_optim)
    cl_ip_optim = obs.cl(ells, cosmo_cosmo0, clparams)

    err_ip = np.abs((cl - cl_ip) / cl)
    err_ip_optim = np.abs((cl - cl_ip_optim) / cl)

    assert np.max(err_ip_optim) < 1e-3
    assert np.max(err_ip) < 1e-3


def test_cl_weak_lensing_regression_ia(obs, cosmo_cosmo0):

    ells = [10, 3000, 12000]

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.03, 1.0, 5.0]),
        "A_IA": 50000.0,
        "z0_IA": 0.0,
        "eta_IA": 10.0,
    }

    cosmo_cosmo0.set(tabulation="off")
    cl = obs.cl(ells, cosmo_cosmo0, clparams)
    tobe = np.array([60404.59405267, 852.77535493, 130.61831829])
    assert np.allclose(cl, tobe, atol=0)

    cosmo_cosmo0.set(tabulation="bao")
    cl, cl_2 = obs.cl_multi(ells, cosmo_cosmo0, [clparams, clparams])
    assert np.all(cl == cl_2)

    assert np.allclose(cl, tobe, atol=0, rtol=6e-4)


@pytest.mark.slow
def test_cl_weak_lensing(obs, cosmo_icosmo_w095, cosmo_icosmo_w1, cosmo_icosmo_cosmo1):
    """
    Tests the implementation of the weak lensing angular power spectrum
    for a Smail et al. redshift distribution against the default icosmo output
    for w0=-0.95 and w0=-1. The values for icosmo are hard-coded.

    w=-0.95 icosmo call
    IDL> fid=set_fiducial(cosmo_in={h:0.7,omega_m:.3,omega_b:0.045,n:1.,sigma8:0.8,
         omega_l:0.7,w0:-0.95},
    calc_in={fit_tk:1,fit_nl:2,n_k:50000,verbose:2,speed:0,nz_crs:400,nz_fn:800},
    expt_in={sv1_n_zbin:1,sv1_zerror:0.0,sv1_z_med:1.23,sv1_dndzp:[2.d,2.d]})
    IDL> sv=mk_survey(fid,'sv1')
    IDL> cosmo=mk_cosmo(fid)
    IDL> cl=mk_cl_tomo(fid,cosmo,sv)

    w=-1 icosmo call
    IDL> fid=set_fiducial(cosmo_in={h:0.7,omega_m:.3,omega_b:0.045,n:1.,sigma8:0.8,
         omega_l:0.7,w0:-1},
    calc_in={fit_tk:1,fit_nl:2,n_k:50000,verbose:2,speed:0,nz_crs:400,nz_fn:800},
    expt_in={sv1_n_zbin:1,sv1_zerror:0.0,sv1_z_med:1.23,sv1_dndzp:[2.d,2.d]})
    IDL> sv=mk_survey(fid,'sv1')
    IDL> cosmo=mk_cosmo(fid)
    IDL> cl=mk_cl_tomo(fid,cosmo,sv)
    """

    test = np.loadtxt(_get_abspath("comparison_files/cls_icosmo_w095_highres.txt"))
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[:, 0]
    cls_weak_lensing_icosmo_w095 = test[:, 1]
    test1 = np.loadtxt(_get_abspath("comparison_files/cls_icosmo_w1_highres.txt"))
    # thin out data to reduce memory consumption:
    test1 = test1[::2, :]

    ells1 = test1[:, 0]
    cls_weak_lensing_icosmo_w1 = test1[:, 1]
    test2 = np.loadtxt(_get_abspath("comparison_files/cls_icosmo_highres_cosmo1.txt"))
    # thin out data to reduce memory consumption:
    test2 = test2[::2, :]
    ells2 = test2[:, 0]
    cls_weak_lensing_icosmo_cosmo1 = test2[:, 1]

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 1000]),
    }

    cosmo_icosmo_w1.reset_wrapper_globals()
    cl_weak_lensing_w1 = obs.cl(ells1, cosmo_icosmo_w1, clparams)

    cosmo_icosmo_w095.reset_wrapper_globals()
    cl_weak_lensing_w095 = obs.cl(ells, cosmo_icosmo_w095, clparams)

    cosmo_icosmo_cosmo1.reset_wrapper_globals()
    cl_weak_lensing_cosmo1 = obs.cl(ells2, cosmo_icosmo_cosmo1, clparams)

    assert np.allclose(
        cl_weak_lensing_w1, cls_weak_lensing_icosmo_w1, atol=1e-16, rtol=6e-3
    )

    assert np.allclose(
        cl_weak_lensing_w095, cls_weak_lensing_icosmo_w095, atol=1e-16, rtol=6e-3
    )
    assert np.allclose(
        cl_weak_lensing_cosmo1, cls_weak_lensing_icosmo_cosmo1, atol=1e-16, rtol=6e-3
    )


@pytest.mark.slow
def test_cl_gammaxcmbkappa(obs, cosmo_camb_p13):
    """
    Test the implementation of the cross-correlation between DES SV weak lensing and CMB
    lensing against the output from Yuki Omori using CAMB power spectra. The agreement
    is mostly sub-percent expect at large scales where it is percent. Since this
    compares EH to the Boltzmann output, this seems ok.
    """

    test = np.loadtxt(_get_abspath("comparison_files/cls_YO_CAMB_gammaxCMBkappa.txt"))
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[:, 0]
    cls_camb_gammaxcmbkappa_p13 = test[:, 1]

    path2gammadist = _get_abspath("comparison_files/nofz_im3shape_r-1.txt")

    clparams = {
        "nz": ["custom", None],
        "path2zdist": [path2gammadist, None],
        "probes": ["gamma", "cmbkappa"],
        "zrecomb": 1090.0,
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 1.8, 5000]),
    }

    cl_gammaxcmbkappa_p13 = obs.cl(ells, cosmo_camb_p13, clparams)

    assert np.allclose(
        cl_gammaxcmbkappa_p13, cls_camb_gammaxcmbkappa_p13, atol=1e-16, rtol=3.2e-2
    )


@pytest.mark.slow
def test_cl_clustering(obs, cosmo_icosmo_w095, cosmo_icosmo_w1, cosmo_cosmo0):
    """
    Tests the implementation of the clustering angular power spectrum for a Smail et al.
    redshift distribution against Andrina's old code for w0=-0.95 and w0=-1. The old
    values are hard-coded.  The parameter call is the same except: 'ngauss': 1500
    """

    obsparams_lin = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["deltag", "deltag"],
        "perturb": "linear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 1000]),
    }

    obsparams_nonlin = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["deltag", "deltag"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 5000]),
    }

    test = np.loadtxt(
        _get_abspath("comparison_files/cls_galaxy_clustering_rev_halofit_cosmo0.txt")
    )
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[1:, 0]
    cls_fid_clustering_nonlin_cosmo0 = test[1:, 1]

    cl_clustering_lin_w095 = obs.cl(2000, cosmo_icosmo_w095, obsparams_lin)
    cl_clustering_nonlin_w095 = obs.cl(2000, cosmo_icosmo_w095, obsparams_nonlin)
    cl_clustering_lin_w1 = obs.cl(2000, cosmo_icosmo_w1, obsparams_lin)
    cl_clustering_nonlin_w1 = obs.cl(2000, cosmo_icosmo_w1, obsparams_nonlin)
    cl_clustering_nonlin_cosmo0 = obs.cl(ells, cosmo_cosmo0, obsparams_nonlin)

    assert np.allclose(
        cl_clustering_nonlin_cosmo0,
        cls_fid_clustering_nonlin_cosmo0,
        atol=1e-16,
        rtol=3e-4,
    )
    assert np.allclose(cl_clustering_lin_w095, 2.06567005503e-09, atol=1e-16, rtol=2e-3)
    assert np.allclose(
        cl_clustering_nonlin_w095, 5.06032399906e-09, atol=1e-16, rtol=2e-3
    )
    assert np.allclose(cl_clustering_lin_w1, 2.01940874532e-09, atol=1e-16, rtol=2e-3)
    assert np.allclose(
        cl_clustering_nonlin_w1, 4.87443220588e-09, atol=1e-16, rtol=2e-3
    )


@pytest.mark.slow
def test_cl_cmbkappaxdeltag(obs, cosmo_cosmo0):
    """
    Test the implementation of the cross-correlation between CMB kappa and deltag for
    a Smail et al., redshift distribution against Andrina's old code.
    The parameter call is the same except:
    'ngauss': 1500
    """

    test = np.loadtxt(
        _get_abspath("comparison_files/cls_cmbkappaXdeltag_rev_halofit_cosmo0.txt")
    )
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[1:, 0]
    cls_fid_cmbkappaxdeltag_cosmo0 = test[1:, 1]

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["deltag", "cmbkappa"],
        "zrecomb": 1090.0,
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 5000]),
    }

    cl_cmbkappaxdeltag_cosmo0 = obs.cl(ells, cosmo_cosmo0, clparams)

    assert np.allclose(
        cl_cmbkappaxdeltag_cosmo0, cls_fid_cmbkappaxdeltag_cosmo0, atol=1e-16, rtol=3e-4
    )


@pytest.mark.slow
def test_cl_gammaxdeltag(obs, cosmo_cosmo0):
    """
    Test the implementation of the cross-correlation between gamma and deltag for
    two Smail et al., redshift distributions against Andrina's old code.
    The parameter call is the same except:
    'ngauss': 1500
    """

    test = np.loadtxt(
        _get_abspath("comparison_files/cls_deltagXgamma_rev_halofit_cosmo0.txt")
    )
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[1:, 0]
    cls_fid_deltagxgamma_cosmo0 = test[1:, 1]

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["deltag", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 5000]),
    }

    cl_deltagxgamma_cosmo0 = obs.cl(ells, cosmo_cosmo0, clparams)

    assert np.allclose(
        cl_deltagxgamma_cosmo0, cls_fid_deltagxgamma_cosmo0, atol=1e-16, rtol=3e-4
    )


@pytest.mark.slow
def test_cl_deltagxtemp(obs, cosmo_cosmo0):
    """
    Test the implementation of the cross-correlation between deltag and CMB temperature
    for a Smail et al., redshift distribution against Andrina's old code.  The parameter
    call is the same except: 'ngauss': 1500
    """

    test = np.loadtxt(
        _get_abspath("comparison_files/cls_deltagXcmbtemp_lin_cosmo0.txt")
    )

    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[1:, 0]
    cls_fid_deltagxtemp_cosmo0 = test[1:, 1]

    clparams = {
        "nz": ["smail", None],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["deltag", "temp"],
        "perturb": "linear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 5000]),
    }

    cl_deltagxtemp_cosmo0 = obs.cl(ells, cosmo_cosmo0, clparams)
    assert np.allclose(
        cl_deltagxtemp_cosmo0, cls_fid_deltagxtemp_cosmo0, atol=1e-16, rtol=3e-4
    )


@pytest.mark.slow
def test_cl_gammaxtemp(obs, cosmo_cosmo0):
    """
    Test the implementation of the cross-correlation between gamma and CMB temperature
    for a Smail et al., redshift distribution against Andrina's old code.  The parameter
    call is the same except: 'ngauss': 1500
    """

    test = np.loadtxt(_get_abspath("comparison_files/cls_gammaXcmbtemp_lin_cosmo0.txt"))
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[1:, 0]
    cls_fid_gammaxtemp_cosmo0 = test[1:, 1]

    clparams = {
        "nz": ["smail", None],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "temp"],
        "perturb": "linear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 5000]),
    }

    cl_gammaxtemp_cosmo0 = obs.cl(ells, cosmo_cosmo0, clparams)

    assert np.allclose(
        cl_gammaxtemp_cosmo0, cls_fid_gammaxtemp_cosmo0, atol=1e-16, rtol=3e-4
    )


@pytest.mark.slow
def test_cl_II(obs, cosmo_cosmo0):
    """
    Test the implementation of the auto-correlation of intrinsic galaxy ellipticities
    for two Smail et al., redshift distributions against Andrina's old code.  The
    parameter call is the same except: 'ngauss': 1500
    """

    test = np.loadtxt(_get_abspath("comparison_files/cls_II_rev_halofit_cosmo0.txt"))
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[1:, 0]
    cls_fid_II_cosmo0 = test[1:, 1]

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 5000]),
    }

    cl_II_cosmo0 = obs.cl_II(ells, cosmo_cosmo0, clparams)

    assert np.allclose(cl_II_cosmo0, cls_fid_II_cosmo0, atol=1e-16, rtol=3e-4)


@pytest.mark.slow
def test_cl_IG(obs, cosmo_cosmo0):
    """
    Test the implementation of the cross-correlation between intrinsic galaxy
    ellipticities and shear for two.  Smail et al., redshift distributions against
    Andrina's old code.  The parameter call is the same except: 'ngauss': 1500
    """

    test = np.loadtxt(_get_abspath("comparison_files/cls_IG_rev_halofit_cosmo0.txt"))
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    ells = test[1:, 0]
    cls_fid_IG_cosmo0 = test[1:, 1]

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 5000]),
    }

    cl_IG_cosmo0 = obs.cl_IG(ells, cosmo_cosmo0, clparams)

    assert np.allclose(cl_IG_cosmo0, cls_fid_IG_cosmo0, atol=1e-16, rtol=3e-4)


# TODO: Percent-level agreement for xim is bad -> check this!


@pytest.mark.xfail
def test_xi(obs, cosmo_icosmo_w095, cosmo_icosmo_w1):
    """
    Tests the implementation of the weak lensing angular correlation function
    for a Smail et al. redshift distribution against the icosmo output
    for w0=-0.95 and w0=-1. The values for icosmo are hard-coded.
    """

    test = np.loadtxt(_get_abspath("comparison_files/corrfunc_icosmo_w095.txt"))
    # thin out data to reduce memory consumption:
    test = test[::2, :]

    thetas_w095 = test[:, 0]
    c1_icosmo_w095 = test[:, 1]
    c2_icosmo_w095 = test[:, 2]
    # Convert icosmo correlation functions to xip, xim
    xip_icosmo_w095 = 4.0 * (c1_icosmo_w095 + c2_icosmo_w095)
    xim_icosmo_w095 = 4.0 * (c1_icosmo_w095 - c2_icosmo_w095)
    xis_w095 = obs.xi(
        cosmo_icosmo_w095, thetas_w095, output_cls=True, linear=False, lmax=10**5
    )
    xip_w095 = xis_w095["xip"]
    xim_w095 = xis_w095["xim"]
    test1 = np.loadtxt(_get_abspath("comparison_files/corrfunc_icosmo_w-1.txt"))
    thetas_w1 = test1[:, 0]
    c1_icosmo_w1 = test1[:, 1]
    c2_icosmo_w1 = test1[:, 2]
    # Convert icosmo correlation functions to xip, xim
    xip_icosmo_w1 = 4.0 * (c1_icosmo_w1 + c2_icosmo_w1)
    xim_icosmo_w1 = 4.0 * (c1_icosmo_w1 - c2_icosmo_w1)
    xis_w1 = obs.xi(
        cosmo_icosmo_w1, thetas_w1, output_cls=True, linear=False, lmax=10**5
    )
    xip_w1 = xis_w1["xip"]
    xim_w1 = xis_w1["xim"]

    assert np.allclose(xip_icosmo_w095, xip_w095, rtol=7e-3)
    assert np.allclose(xim_icosmo_w095, xim_w095, rtol=2.5e-2)
    assert np.allclose(xip_icosmo_w1, xip_w1, rtol=2e-3)
    assert np.allclose(xim_icosmo_w1, xim_w1, rtol=2.5e-2)


def test_nz_custom_array(obs, cosmo_cosmo0, data_path):
    """
    Test if nz modes ``custom`` and ``custom_array`` give the same result.
    """
    ells = [10, 3000, 12000]

    clparams = {
        "nz": ["custom", "custom"],
        "path2zdist": [
            data_path("newcomparisons/nz_wl_gamma_gamma_histo.out"),
            data_path("newcomparisons/nz_wl_gamma_gamma_histo.out"),
        ],
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.03, 1, 5.0]),
        "A_IA": 0.0,
        "z0_IA": 0.0,
        "eta_IA": 0.0,
    }

    cosmo_cosmo0.set(tabulation="off")
    cl_custom = obs.cl(ells, cosmo_cosmo0, clparams)

    nz_array = np.genfromtxt(data_path("newcomparisons/nz_wl_gamma_gamma_histo.out"))
    clparams["nz"] = ["custom_array", "custom_array"]
    clparams["path2zdist"] = [nz_array, nz_array]
    cl_custom_array = obs.cl(ells, cosmo_cosmo0, clparams)

    assert np.all(cl_custom == cl_custom_array)


def test_regression_cl_mead(obs, cosmo_cosmo0):
    """
    Test the implementation of the cross-correlation between gamma and CMB temperature
    for a Smail et al., redshift distribution against Andrina's old code.  The parameter
    call is the same except: 'ngauss': 1500
    """

    ells = [1, 100, 10000]

    clparams = {
        "nz": ["smail", None],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "temp"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 3]),
    }

    cosmo_cosmo0.set(pk_nonlin_type="mead")
    cosmo_cosmo0.set(tabulation="off")

    cl = obs.cl(ells, cosmo_cosmo0, clparams)
    tobe = np.array([3.52263130e-09, 1.46403125e-12, -7.20724431e-20])
    assert np.allclose(cl, tobe, atol=1e-8, rtol=1e-5)


def test_obs_code_comparison(data_path):

    # Cosmological setup
    cosmo = PyCosmo.build("wcdm")
    cosmo.set(h=0.7, omega_b=0.06, omega_m=0.3, n=1.0, N_massless_nu=3.0, pk_norm=0.8)
    cosmo.set(ainit_growth=0.1)
    cosmo.set(pk_type="EH")
    cosmo.set(pk_nonlin_type="rev_halofit")

    cosmo_pi = PyCosmo.build()
    cosmo_pi.set(
        h=0.7, omega_b=0.06, omega_m=0.3, n=1.0, N_massless_nu=3.0, pk_norm=0.8
    )
    cosmo_pi.set(omega_suppress=True, suppress_rad=True)
    cosmo_pi.set(Tcmb=2.726)
    cosmo_pi.set(ainit_growth=1.0e-3, rtol_growth=1.0e-9)
    cosmo_pi.set(pk_type="EH")
    cosmo_pi.set(pk_nonlin_type="halofit")

    # Computation of the cls with Halofit+EH
    obs = PyCosmo.Obs()
    ells = np.loadtxt(data_path("newcomparisons/ells.txt"))

    testfile_pycosmo_ccl_eh = np.loadtxt(
        data_path("newcomparisons/cls_ccl_halofit_eh.txt")
    )
    testfile_pycosmo_ccl_bbks = np.loadtxt(
        data_path("newcomparisons/cls_ccl_halofit_bbks.txt")
    )
    testfile_pycosmo_icosmo_eh = np.loadtxt(data_path("newcomparisons/cls_icosmo.txt"))
    testfile_pycosmo_icosmo_bbks = np.loadtxt(
        data_path("newcomparisons/cls_icosmo_bbks.txt")
    )

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 1000]),
    }
    cls_pycosmo_icosmo_haloEH = obs.cl(ells, cosmo_pi, clparams)
    assert np.allclose(
        cls_pycosmo_icosmo_haloEH, testfile_pycosmo_icosmo_eh, atol=0, rtol=3e-3
    )

    clparams_ccl = {
        "nz": ["custom", "custom"],
        "path2zdist": [
            data_path("newcomparisons/nz_wl_gamma_gamma_histo.out"),
            data_path("newcomparisons/nz_wl_gamma_gamma_histo.out"),
        ],
        "probes": ["gamma", "gamma"],
        "zrecomb": 1110,
        "perturb": "nonlinear",
        "normalised": True,
        "bias": 1.0,
        "m": 0,
        "ngauss": 1000,
        "z_grid": np.array([0.0001, 5, 10000]),
    }
    cls_pycosmo_ccl_haloEH = obs.cl(ells, cosmo, clparams_ccl)
    assert np.allclose(
        cls_pycosmo_ccl_haloEH, testfile_pycosmo_ccl_eh, atol=0, rtol=3.5e-2
    )

    # Computation of the cls with Halofit+BBKS
    cosmo.set(pk_type="BBKS_CCL")
    cosmo_pi.set(pk_type="BBKS")

    clparams = {
        "nz": ["smail", "smail"],
        "z0": 1.13,
        "beta": 2.0,
        "alpha": 2.0,
        "probes": ["gamma", "gamma"],
        "perturb": "nonlinear",
        "normalised": False,
        "bias": 1.0,
        "m": 0,
        "z_grid": np.array([0.0001, 5.0, 1000]),
    }
    cls_pycosmo_icosmo_haloBBKS = obs.cl(ells, cosmo_pi, clparams)
    assert np.allclose(
        cls_pycosmo_icosmo_haloBBKS, testfile_pycosmo_icosmo_bbks, atol=0, rtol=2e-3
    )

    clparams_ccl = {
        "nz": ["custom", "custom"],
        "path2zdist": [
            data_path("newcomparisons/nz_wl_gamma_gamma_histo.out"),
            data_path("newcomparisons/nz_wl_gamma_gamma_histo.out"),
        ],
        "probes": ["gamma", "gamma"],
        "zrecomb": 1110,
        "perturb": "nonlinear",
        "normalised": True,
        "bias": 1.0,
        "m": 0,
        "ngauss": 1000,
        "z_grid": np.array([0.0001, 5, 10000]),
    }
    cls_pycosmo_ccl_haloBBKS = obs.cl(ells, cosmo, clparams_ccl)
    assert np.allclose(
        cls_pycosmo_ccl_haloBBKS, testfile_pycosmo_ccl_bbks, atol=0, rtol=4e-2
    )


if __name__ == "__main__":
    import pytest

    pytest.main(["--runslow", "--pdb", "tests/test_obs.py::test_cl_gammaxcmbkappa"])

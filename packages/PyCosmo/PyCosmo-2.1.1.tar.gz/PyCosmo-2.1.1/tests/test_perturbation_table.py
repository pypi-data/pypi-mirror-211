#!/usr/bin/env python

import numpy as np
import pytest

import PyCosmo
from PyCosmo.PerturbationTable import optimize_grid


@pytest.fixture(scope="module")
def cosmo():
    yield PyCosmo.build()


def test_interpolation_table(cosmo):
    lin_pert_non_tab = cosmo.lin_pert

    cosmo.set(tabulation="bao")
    # triggers _k_grid and _a_grid setup, needed below:
    cosmo.lin_pert.powerspec_a_k(1.0, 1e-3)

    k = cosmo.lin_pert._k_grid[-1]
    a = cosmo.lin_pert._a_grid[-1]
    assert np.isclose(
        lin_pert_non_tab.powerspec_a_k(a, k),
        cosmo.lin_pert.powerspec_a_k(a, k),
        atol=0,
        rtol=1e-15,
    )

    # the round is needed due to some weird numpy float issues:
    k_grid = np.round((10 ** np.linspace(-5, 0, 10)), 20)

    cosmo.set(tabulation="manual", tabulation_k_grid=k_grid)
    # triggers _k_grid and _a_grid setup, needed below:
    cosmo.lin_pert.powerspec_a_k(1.0, 1e-3)

    assert np.allclose(cosmo.lin_pert._k_grid, k_grid, atol=0, rtol=1e-14)

    assert np.isclose(
        lin_pert_non_tab.powerspec_a_k(a, 1.0),
        cosmo.lin_pert.powerspec_a_k(a, 1.0),
        atol=0,
        rtol=1e-15,
    )

    avec = np.array([0.2, 0.5, 1.0])
    kvec = k_grid[:-1] * 1.001
    assert np.allclose(
        lin_pert_non_tab.powerspec_a_k(avec, kvec),
        cosmo.lin_pert.powerspec_a_k(avec, kvec),
        atol=0,
        rtol=3e-4,
    )


def test_default_settings(cosmo):
    cosmo.set(tabulation="default_precise")
    cosmo.lin_pert.powerspec_a_k(1.0, 0.001)

    cosmo.set(tabulation="default_fast")
    cosmo.lin_pert.powerspec_a_k(1.0, 0.001)

    cosmo.set(tabulation_min_k=1e-4)
    # compute powersped to init ip setup incl. k_limits:
    cosmo.lin_pert.powerspec_a_k(1.0, 0.001)
    assert cosmo.lin_pert._k_limits[0] >= 1e-4

    cosmo.set(tabulation_max_k=1.0)
    # compute powersped to init ip setup incl. k_limits:
    cosmo.lin_pert.powerspec_a_k(1.0, 0.001)
    assert cosmo.lin_pert._k_limits[1] <= 1.0


def test_grid_optimization(cosmo):
    cosmo = PyCosmo.build()
    k_init = np.logspace(-4, 1, 100)
    kgrid, smoothed_error, pointwise_error = optimize_grid(
        cosmo.lin_pert, k_init, 5e-4, 10
    )

    assert len(kgrid) == 32
    assert np.isclose(smoothed_error, 0.0004202881296791694, atol=0, rtol=1e-10)
    assert np.isclose(pointwise_error, 0.0018297731838060605, atol=0, rtol=1e-10)

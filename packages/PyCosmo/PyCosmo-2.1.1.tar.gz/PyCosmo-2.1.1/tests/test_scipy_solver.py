#!/usr/bin/env python

import numpy as np
import pytest

import PyCosmo
from PyCosmo.BoltzmannSolver.ScipySolver import ScipySolver, ScipySolverRSA


@pytest.fixture(scope="module")
def cosmo():
    cosmo = PyCosmo.build(l_max=5, reorder=False)
    cosmo.set(pk_type="boltz")
    yield cosmo


@pytest.fixture(scope="module")
def cosmo_rsa():
    cosmo = PyCosmo.build(l_max=5, reorder=False, rsa=True)
    cosmo.set(pk_type="boltz")
    yield cosmo


def test_solver(cosmo):

    solver = ScipySolver(cosmo, "Radau", rtol=1e-4, atol=1e-5)

    grid, y_radau, meta = solver.solve(k=0.1, grid=[0.0])

    assert meta["status"] == 0
    assert meta["nlu"] > 0
    assert meta["njev"] > 0
    assert meta["nfev"] > 0

    grid, y_radau, meta = solver.solve(k=0.1, grid=0.0)

    assert meta["status"] == 0
    assert meta["nlu"] > 0
    assert meta["njev"] > 0
    assert meta["nfev"] > 0
    assert meta["t"].shape[0] > 2

    solver = ScipySolver(cosmo, "BDF")
    grid, y_bdf, meta = solver.solve(0.1, [0.0])
    assert meta["status"] == 0


def test_solver_rsa(cosmo_rsa):

    solver = ScipySolverRSA(cosmo_rsa, "Radau", rtol=1e-4, atol=1e-5)

    grid, y_radau, meta = solver.solve(k=0.1, grid=[0.0])

    assert meta["status"] == 0
    assert meta["nlu"] > 0
    assert meta["njev"] > 0
    assert meta["nfev"] > 0


def test_fields_interface(cosmo):
    solver = ScipySolver(cosmo, "Radau")

    grid = np.linspace(-15, 0.0, 500)
    k = 0.5

    _, y_radau, _ = solver.solve(k=k, grid=grid)

    fields = solver.fields(k=k, grid=grid, keep_lna0=True)

    assert np.all(fields._y[:-2, 1].flatten() == y_radau[1])
    assert np.all(fields.Phi == y_radau[:, 0])


def test_compare_sympy2c_solver(cosmo):
    solver = ScipySolver(cosmo, "LSODA", atol=1e-3, rtol=1e-3, first_step=1e-5)

    grid = np.linspace(-15, 0, 500)
    k = 1.0

    fields_baseline = cosmo.lin_pert.fields(k=k, grid=grid, keep_lna0=True)

    assert np.isclose(
        sum(fields_baseline.meta["step_sizes"]),
        fields_baseline.lna[-1] - fields_baseline.lna[0],
        atol=0,
        rtol=1e-8,
    )

    fields = solver.fields(k=k, grid=grid, keep_lna0=True)

    assert np.allclose(
        fields_baseline.Phi[-100:-1], fields.Phi[-100:-1], atol=0.0, rtol=5e-3
    )

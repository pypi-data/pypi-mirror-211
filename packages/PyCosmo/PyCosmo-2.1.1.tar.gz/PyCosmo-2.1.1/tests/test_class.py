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


import csv
import os

import numpy as np
import pytest

from PyCosmo import build

"""
Test of perturbations at fixed k
"""

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="module")
def cosmo():

    c = build(l_max=30)
    c.set(
        pk_type="boltz",
        initial_conditions="class",
        recomb="class",
        recomb_dir=os.path.join(HERE, "comparison_files/class_comparison/"),
        recomb_filename="lcdm_thermodynamics.dat",
        N_massless_nu=3,
        boltzmann_rtol=1e-6,
        boltzmann_atol=1e-8,
    )

    return c


def test_fields_smallk(cosmo):

    class_fields = _read_class_data()
    fields = cosmo.lin_pert.fields(
        k=class_fields["k"] / cosmo.params.h, grid=np.log(class_fields["a"])
    )

    # check that a are sufficiently close
    assert np.allclose(fields.a, class_fields["a"], atol=1e-10)

    # check fields
    assert np.allclose(fields.Theta[0], class_fields["theta_0"], atol=6e-6, rtol=0)
    assert np.allclose(fields.Theta[0], class_fields["theta_0"], atol=0, rtol=5e-5)

    # no rtol comparsion becuase we divide by values which are very close to 0:
    assert np.allclose(fields.Theta[1], class_fields["theta_1"], atol=7e-6, rtol=0)

    # no rtol comparsion becuase we divide by values which are very close to 0:
    assert np.allclose(fields.Theta[2], class_fields["theta_2"], atol=7.3e-7, rtol=0)

    assert np.allclose(fields.u_b, class_fields["u_b"], atol=2e-6, rtol=0)
    assert np.allclose(fields.u_b, class_fields["u_b"], atol=0, rtol=2.1e-5)

    assert np.allclose(fields.u, class_fields["u"], atol=2e-6, rtol=0)
    assert np.allclose(fields.u, class_fields["u"], atol=0, rtol=2e-5)

    assert np.allclose(fields.delta, class_fields["delta"], atol=2e-5, rtol=0)
    assert np.allclose(fields.delta, class_fields["delta"], atol=0, rtol=2e-5)

    assert np.allclose(fields.delta_b, class_fields["delta_b"], atol=2e-5, rtol=0)
    assert np.allclose(fields.delta_b, class_fields["delta_b"], atol=0, rtol=2e-5)

    assert np.allclose(fields.Phi, class_fields["Phi"], atol=7e-6, rtol=0)
    assert np.allclose(fields.Phi, class_fields["Phi"], atol=0, rtol=2e-5)

    assert np.allclose(fields.N[0], class_fields["N0"], atol=6e-6, rtol=0)
    assert np.allclose(fields.N[0], class_fields["N0"], atol=0, rtol=2e-5)

    assert np.allclose(fields.N[1], class_fields["N1"], atol=1.1e-6, rtol=0)
    assert np.allclose(fields.N[1], class_fields["N1"], atol=0, rtol=7e-3)


def test_recomb(cosmo):
    k_values, class_tk = _read_class_tk(cosmo, z=1080)

    lna_rec = np.log(1.0 / 1081.0)
    grid = np.linspace(np.log(1e-8), lna_rec, 100)

    rtol = 2.8e-4

    for ki, k in enumerate(k_values):
        fields = cosmo.lin_pert.fields(k / cosmo.params.h, grid)

        assert np.allclose(class_tk[0, ki], fields.Theta[0][-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[1, ki], fields.Theta[1][-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[2, ki], fields.delta_b[-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[3, ki], fields.u_b[-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[4, ki], fields.Phi[-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[5, ki], fields.N[0][-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[6, ki], fields.N[1][-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[7, ki], fields.delta[-1], atol=0, rtol=rtol)
        assert np.allclose(class_tk[8, ki], fields.u[-1], atol=0, rtol=rtol)


def _read_class_data():

    # get cosmo parameters
    # load class data
    path = os.path.join(
        HERE, "comparison_files", "class_comparison", "lcdm_perturbations_k0_s.dat"
    )
    with open(path, "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        rows = [list(filter(None, row)) for row in reader]

    data = np.array([[float(x) for x in row] for row in rows[2:]])
    k = float(rows[0][6])

    # cleanup the grid
    limit = 1e-4
    filt = np.empty(data[:, 1].shape, dtype=bool)
    lna0 = np.log(data[0, 1])
    for idx, lna in enumerate(np.log(data[:, 1])):
        if lna > np.log(1e-3) and lna - lna0 > limit:
            filt[idx] = True
            lna0 = lna
        else:
            filt[idx] = False

    # extract class fields
    fields = dict(
        {
            "a": data[:, 1][filt],
            "theta_0": (data[:, 2] / 4.0)[filt],
            "theta_1": (data[:, 3] / (3 * k))[filt],
            "theta_2": (data[:, 4] / 2.0)[filt],
            "delta_b": data[:, 8][filt],
            "u_b": (data[:, 9] / k)[filt],
            "Phi": -data[:, 11][filt],
            "N0": (data[:, 12] / 4.0)[filt],
            "N1": (data[:, 13] / (3.0 * k))[filt],
            "N2": (data[:, 14] / 2.0)[filt],
            "delta": data[:, 15][filt],
            "u": (data[:, 16] / k)[filt],
        }
    )

    fields["k"] = k

    return fields


def _read_class_tk(cosmo, z):

    # get cosmo parameters
    h = cosmo.params.h

    path = os.path.join(HERE, "comparison_files", "class_comparison", "lcdm_z2_tk.dat")

    # load class data
    with open(path, "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        rows = [list(filter(None, row)) for row in reader]
    data = np.array([[float(x) for x in row] for row in rows[11:]])
    skip = 20
    k = data[0::skip, 0] * h
    filt = k < 0.15
    k = k[filt]

    # cleanup the grid
    theta_0 = data[0::skip, 1][filt] / 4.0
    theta_1 = data[0::skip, 8][filt] / (3.0 * k)
    delta_b = data[0::skip, 2][filt]
    u_b = data[0::skip, 9][filt] / k
    Phi = -data[0::skip, 6][filt]
    N0 = data[0::skip, 4][filt] / 4.0
    N1 = data[0::skip, 11][filt] / (3.0 * k)
    delta = data[0::skip, 3][filt]
    u = data[0::skip, 10][filt] / k

    fields = np.concatenate((theta_0, theta_1, delta_b, u_b, Phi, N0, N1, delta, u))
    fields = np.reshape(fields, (9, len(theta_0)))

    return k, fields


if __name__ == "__main__":
    import pytest

    pytest.main([__file__ + "::test_odeint_solver", "-s"])

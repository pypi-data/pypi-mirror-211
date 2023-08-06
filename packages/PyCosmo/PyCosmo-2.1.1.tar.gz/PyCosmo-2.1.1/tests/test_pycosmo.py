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


import numpy as np

import PyCosmo


def test_build_lcdm(tmpdir):

    c = PyCosmo.build()
    c.load_params()

    parameters = {
        "h": 0.7,
        "omega_b": 0.06,
        "flat_universe": True,
        "omega_l": None,
        "N_massless_nu": 3.0,
    }

    c.set(**parameters)

    checks = [
        (c.background.H, [0.5, 1.0], [123.27299790425887, 70], 1e-8),
        (c.background.dist_rad_a, [0.5, 1.0], [3303.5280671, 0.0], 1e-8),
        (c.background.dist_trans_a, [0.5, 1.0], [3303.5280671, 0.0], 1e-8),
        (c.background.dist_ang_a, [0.5, 1.0], [1651.764033549148, 0.0], 1e-8),
        (c.background.dist_lum_a, [0.5, 1.0], [6607.056134196592, 0.0], 1e-8),
        (
            c.background.eta,
            [0, 0.1, 0.5, 1.0],
            [0.0, 3281.98597635555, 7414.021758241548, 9726.491520836624],
            1e-3,
        ),
    ]

    report = []
    for function, args, expected, tol in checks:
        for a, e in zip(args, expected):
            r = function(a)
            if abs(r - e) < tol:
                continue
            report.append(
                "{}({}) = {} != {}".format(function.__func__.__qualname__, a, r, e)
            )
        r = function(args)
        if not np.allclose(r, np.array(expected)):
            report.append(
                "{}({}) = {} != {}".format(
                    function.__func__.__qualname__, args, list(r), expected
                )
            )

    assert not report, "\n".join(report)


def test_build_qcdm(tmpdir):

    c = PyCosmo.build("wcdm")
    c.load_params()

    parameters = {
        "h": 0.7,
        "omega_b": 0.06,
        "flat_universe": True,
        "w0": -0.9,
        "wa": 0,
        "N_massless_nu": 3,
    }
    c.set(**parameters)

    setup = [
        ("H", 1.0, 70.0, None),
        ("H", 0.5, 126.44746468602816, None),
        ("dist_rad_a", 1.0, 0.0, None),
        ("dist_rad_a", 0.5, 3236.42647754814, None),
        ("dist_trans_a", 0.5, 3236.42647754814, None),
        ("dist_trans_a", 1, 0.0, None),
        ("dist_ang_a", 0.5, 1618.21323877407, None),
        ("dist_ang_a", 1, 0.0, None),
        ("dist_lum_a", 0.5, 6472.85295509628, None),
        ("dist_lum_a", 1, 0.0, None),
        ("eta", 0, [0.0], None),
        ("eta", 5e-100, [0.0], None),
        ("eta", 0.5, [7368.3003483], 1e-4),
        ("eta", 1.0, [9633.7993724], 1e-4),
    ]

    report = []
    for func, arg, expected, tol in setup:
        result = getattr(c.background, func)(arg)
        # print("({!r}, {}, {}),".format(func, arg, result))
        ok = abs(result - expected) < (tol or 1e-8)
        if not ok:
            report.append("{}({}) = {} != {}".format(func, arg, result, expected))

    assert not report, "\n".join(report)

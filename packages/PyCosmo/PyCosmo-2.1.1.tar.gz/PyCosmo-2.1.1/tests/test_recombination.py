#!/usr/bin/env python

import os

import numpy as np

import PyCosmo


def test_cosmics():
    c = PyCosmo.build()
    here = os.path.dirname(os.path.abspath(__file__))
    c.set(
        recomb="cosmics",
        recomb_dir=os.path.join(here, "comparison_files", "cosmics", "zend_0"),
    )

    assert np.isclose(c.background.taudot(0.1), -1.3062749e-05, atol=0)
    assert np.isclose(c.background.cs(0.1), 1.6021135e-09, atol=0)

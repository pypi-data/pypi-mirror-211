#!/usr/bin/env python

import sys

from PyCosmo.ini_handling import Bunch
from PyCosmo.model_config import model_config

# from PyCosmo.core_file_handling


def test_import_core_file():
    cosmology = Bunch(model_config("lcdm", {}))
    __builtins__["cosmology"] = cosmology
    from PyCosmo import CosmologyCore  # noqa: F401


def test_import_core_file_rsa():
    cosmology = Bunch(model_config("lcdm", dict(rsa=True)))
    __builtins__["cosmology"] = cosmology
    from PyCosmo import CosmologyCore  # noqa: F401

    sys.modules["CosmologyCore"] = CosmologyCore
    from PyCosmo import CosmologyCore_rsa  # noqa: F401


def test_import_core_file_wcdm():
    cosmology = Bunch(model_config("wcdm", {}))
    __builtins__["cosmology"] = cosmology
    from PyCosmo import CosmologyCore_wcdm  # noqa: F401


def test_import_core_file_wcdm_rsa():
    cosmology = Bunch(model_config("wcdm", dict(rsa=True)))
    __builtins__["cosmology"] = cosmology
    from PyCosmo import CosmologyCore_wcdm  # noqa: F401

    sys.modules["CosmologyCore_wcdm"] = CosmologyCore_wcdm
    from PyCosmo import CosmologyCore_wcdm_rsa  # noqa: F401


def test_import_core_file_massivenu():
    cosmology = Bunch(
        model_config("mnulcdm", dict(l_max=5, l_max_mnu=5, mnu_relerr=1e-3))
    )
    __builtins__["cosmology"] = cosmology
    from PyCosmo import CosmologyCore_massivenu  # noqa: F401


def test_import_core_file_massivenu_rsa():
    cosmology = Bunch(
        model_config("mnulcdm", dict(l_max=5, l_max_mnu=5, mnu_relerr=1e-3, rsa=True))
    )
    __builtins__["cosmology"] = cosmology
    from PyCosmo import CosmologyCore_massivenu  # noqa: F401

    sys.modules["CosmologyCore_massivenu"] = CosmologyCore_massivenu
    from PyCosmo import CosmologyCore_massivenu_rsa  # noqa: F401

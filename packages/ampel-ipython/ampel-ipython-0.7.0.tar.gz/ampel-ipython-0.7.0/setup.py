#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-ipython/setup.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 30.07.2020
# Last Modified Date: 30.07.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from setuptools import setup # type: ignore

setup(
	name='ampel-ipython',
	packages=["ampel_quick_import"],
	version='0.7.0',
	python_requires='>=3.8',
	author_email="vbrinnel@physik.hu-berlin.de"
)

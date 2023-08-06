#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012-2022 SoftBank Robotics. All rights reserved.
# Use of this source code is governed by a BSD-style license (see the COPYING file).
""" QiBuild """
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import pytest

from qibuild.test.test_qibuild_deploy import get_ssh_url


@pytest.mark.skipif(os.environ.get("LOGNAME") == "gitlab-runner", reason="does not work on the new runner")
def test_simple(qipy_action, tmpdir):
    """ Test Simple """
    python_version = "2.7" # "{}.{}".format(sys.version_info[0], sys.version_info[1])
    url = get_ssh_url(tmpdir)
    qipy_action.add_test_project("a_lib")
    qipy_action("deploy", "a", "--url", url)
    assert tmpdir.join("lib", "python{}".format(python_version), "site-packages", "a.py").check(file=True)

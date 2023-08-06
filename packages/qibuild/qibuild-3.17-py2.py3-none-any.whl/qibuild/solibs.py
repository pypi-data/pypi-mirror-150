#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012-2022 SoftBank Robotics. All rights reserved.
# Use of this source code is governed by a BSD-style license (see the COPYING file).
""" Set of tools to handle .so on ubuntu 18.04 and higher """
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import os

import qisys.sh
import qisys.command
from qisys import ui


def fix_solibs(toolchain_dir, paths=None):
    """
    Add rpath to relocate the toolchain libraries
    """
    if not os.path.exists(toolchain_dir):
        ui.error("Could not patch solib, {} not found".format(toolchain_dir))
        return
    bin_to_patch_list = []
    lib_path_list = []
    ui.info("Listing binaries to patch ...")
    for root, _, files in os.walk(toolchain_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if "/bin/" in full_path or "/lib/" in full_path:
                if _is_bin_or_solib(full_path):
                    bin_to_patch_list.append(full_path)
            if "/lib/" in full_path and root not in lib_path_list:
                lib_path_list.append(root)
    ui.info(" * binaries: {}".format(len(bin_to_patch_list)))
    ui.info(" * rpaths: {}".format(len(lib_path_list)))
    rpath_size = len(":".join(lib_path_list))
    if rpath_size < 65536:
        ui.info("Patching binaries ...")
        for lib in bin_to_patch_list:
            _add_rpath(lib, lib_path_list)
        ui.info("Checking SDK")
        not_patched_correctly = []
        for lib in bin_to_patch_list:
            if not _found_all_deps(lib):
                not_patched_correctly.append(lib)
        if len(not_patched_correctly) > 0:
            ui.warning(" * Problematic binaries: {}".format(len(not_patched_correctly)))
            for lib in not_patched_correctly:
                ui.warning("        {}".format(lib))
        else:
            ui.info(" * OK")
    else:
        ui.info("Skip patching binaries (rpath limit {})".format(rpath_size))


def _is_bin_or_solib(lib):
    """
    Check if the presented file is a shared libraries
    """
    filebin = qisys.command.find_program("file")
    if not filebin:
        ui.error("Could not find file executable")
    else:
        cmd = [filebin, lib]
        try:
            out = qisys.command.check_output(cmd)
            if b'dynamically linked' in out:
                ldd = qisys.command.find_program("ldd")
                if not ldd:
                    ui.error("Could not find ldd executable")
                else:
                    cmd = [ldd, lib]
                    try:
                        out, err = qisys.command.check_output_error(cmd)
                        if not err:
                            return True
                    except Exception as e:
                        ui.debug("Warning ldd", e)
        except Exception as e:
            ui.info("Warning file", e)
    return False


def _found_all_deps(lib):
    """
    Check if the presented file can load all dependencies
    """
    ldd = qisys.command.find_program("ldd")
    if not ldd:
        ui.error("Could not find ldd executable")
    else:
        cmd = [ldd, lib]
        try:
            out, _ = qisys.command.check_output_error(cmd)
            if b'=> not found' in out:
                return False
        except Exception as e:
            ui.debug("Warning", e)
    return True


def _add_rpath(lib, rpaths):
    """
    Add rpath to relocate the toolchain libraries
    """
    if isinstance(rpaths, list):
        rpath_str = ":".join(rpaths)
    else:
        rpath_str = rpaths
    patchelf = qisys.command.find_program("patchelf")
    if not patchelf:
        ui.error("Could not find patchelf for fixing so libraries")
    else:
        chmod = qisys.command.find_program("chmod")
        cmd = [chmod, "777", lib]
        qisys.command.call(cmd)
        cmd = [patchelf, "--set-rpath", rpath_str, lib]
        try:
            qisys.command.call(cmd, quiet=True)
        except Exception as e:
            ui.warning(lib, e)

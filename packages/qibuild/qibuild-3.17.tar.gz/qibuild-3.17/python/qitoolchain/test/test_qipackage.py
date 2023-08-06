#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012-2022 SoftBank Robotics. All rights reserved.
# Use of this source code is governed by a BSD-style license (see the COPYING file).
""" Test QiPackage """
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import os
import re
import pytest

import qitoolchain.qipackage
import qisys.archive
from qisys.test.conftest import skip_on_win, linux_only
import qibuild.worktree
import qibuild.actions.package


def test_equality():
    """ Test Equality """
    foo1 = qitoolchain.qipackage.QiPackage("foo", "1.2")
    foo2 = qitoolchain.qipackage.QiPackage("foo", "1.2")
    foo3 = qitoolchain.qipackage.QiPackage("foo", "1.3")
    bar1 = qitoolchain.qipackage.QiPackage("bar", "1.2")
    assert foo1 == foo2
    assert foo2 < foo3
    assert foo1 != bar1


def test_from_archive(tmpdir):
    """ Test From Archive """
    foo1 = tmpdir.mkdir("foo")
    foo_xml = foo1.join("package.xml")
    foo_xml.write("""<package name="foo" version="0.1"/>""")
    archive = qisys.archive.compress(foo1.strpath, flat=True)
    package = qitoolchain.qipackage.from_archive(archive)
    assert package.name == "foo"
    assert package.version == "0.1"


def test_skip_package_xml(tmpdir):
    """ Test Skip Package Xml """
    foo1 = tmpdir.mkdir("foo")
    foo_xml = foo1.join("package.xml")
    foo_xml.write("""<package name="foo" version="0.1"/>""")
    foo1.ensure("include", "foo.h", file=True)
    foo1.ensure("lib", "libfoo.so", file=True)
    package = qitoolchain.qipackage.QiPackage("foo", path=foo1.strpath)
    dest = tmpdir.join("dest")
    package.install(dest.strpath)
    assert dest.join("include", "foo.h").check(file=True)
    assert dest.join("lib", "libfoo.so").check(file=True)
    assert not dest.join("package.xml").check(file=True)


def test_reads_runtime_manifest(tmpdir):
    """ Test Read Runtime Manifest """""
    boost_path = tmpdir.mkdir("boost")
    boost_path.ensure("include", "boost.h", file=True)
    boost_path.ensure("lib", "libboost.so", file=True)
    runtime_manifest = boost_path.ensure("install_manifest_runtime.txt", file=True)
    runtime_manifest.write(b"""lib/libboost.so\n""")
    package = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    dest = tmpdir.join("dest")
    installed = package.install(dest.strpath, components=["runtime"])
    assert not dest.join("include", "boost.h").check(file=True)
    libbost_so = dest.join("lib", "libboost.so")
    assert libbost_so.check(file=True)
    assert installed == ["lib/libboost.so"]


def test_backward_compat_runtime_install(tmpdir):
    """ Test Backward Compat Runtime """
    boost_path = tmpdir.mkdir("boost")
    boost_path.ensure("include", "boost.h", file=True)
    boost_path.ensure("lib", "libboost.so", file=True)
    boost_path.ensure("package.xml", file=True)
    package = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    dest = tmpdir.join("dest")
    installed = package.install(dest.strpath, components=["runtime"])
    assert not dest.join("include", "boost.h").check(file=True)
    libbost_so = dest.join("lib", "libboost.so")
    assert libbost_so.check(file=True)
    assert installed == ["lib/libboost.so"]


def test_reads_release_mask(tmpdir):
    """ Test Reads Release Mask """
    qt_path = tmpdir.mkdir("qt")
    qt_path.ensure("include", "qt.h", file=True)
    qt_path.ensure("lib", "QtCore4.lib", file=True)
    qt_path.ensure("lib", "QtCored4.lib", file=True)
    qt_path.ensure("bin", "QtCore4.dll", file=True)
    qt_path.ensure("bin", "QtCored4.dll", file=True)
    runtime_mask = qt_path.ensure("runtime.mask", file=True)
    runtime_mask.write(b"""\n# headers\nexclude include/.*\n\n# .lib\nexclude lib/.*\\.lib\n""")
    release_mask = qt_path.ensure("release.mask", file=True)
    release_mask.write(b"""\nexclude bin/QtCored4.dll\n""")
    package = qitoolchain.qipackage.QiPackage("qt", path=qt_path.strpath)
    dest = tmpdir.join("dest")
    package.install(dest.strpath, release=True, components=["runtime"])
    assert dest.join("bin", "QtCore4.dll").check(file=True)
    assert not dest.join("lib", "QtCored4.lib").check(file=True)


def test_include_in_mask(tmpdir):
    """ Test Include in Mask """
    qt_path = tmpdir.mkdir("qt")
    qt_path.ensure("bin", "assitant.exe")
    qt_path.ensure("bin", "moc.exe")
    qt_path.ensure("bin", "lrelease.exe")
    qt_path.ensure("bin", "lupdate.exe")
    runtime_mask = qt_path.ensure("runtime.mask", file=True)
    runtime_mask.write(b"""\nexclude bin/.*\\.exe\ninclude bin/lrelease.exe\ninclude bin/lupdate.exe\n""")
    dest = tmpdir.join("dest")
    package = qitoolchain.qipackage.QiPackage("qt", path=qt_path.strpath)
    package.install(dest.strpath, release=True, components=["runtime"])
    assert dest.join("bin", "lrelease.exe").check(file=True)
    assert not dest.join("bin", "moc.exe").check(file=True)


def test_load_deps(tmpdir):
    """ Test Load Dependencies """
    libqi_path = tmpdir.mkdir("libqi")
    libqi_path.ensure("package.xml").write(b"""
<package name="libqi">
  <depends testtime="true" names="gtest" />
  <depends runtime="true" names="boost python" />
</package>
""")
    package = qitoolchain.qipackage.QiPackage("libqi", path=libqi_path.strpath)
    package.load_deps()
    assert package.build_depends == set()
    assert package.run_depends == set(["boost", "python"])
    assert package.test_depends == set(["gtest"])


def test_extract_legacy_bad_top_dir(tmpdir):
    """ Test Extract Legacy Bad Top Dir """
    src = tmpdir.mkdir("src")
    boost = src.mkdir("boost")
    boost.ensure("lib", "libboost.so", file=True)
    res = qisys.archive.compress(boost.strpath)
    dest = tmpdir.mkdir("dest").join("boost-1.55")
    qitoolchain.qipackage.extract(res, dest.strpath)
    assert dest.join("lib", "libboost.so").check(file=True)


def test_extract_legacy_ok_top_dir(tmpdir):
    """ Test Extract Legacy Ok Top Dir """
    src = tmpdir.mkdir("src")
    boost = src.mkdir("boost-1.55")
    boost.ensure("lib", "libboost.so", file=True)
    res = qisys.archive.compress(boost.strpath)
    dest = tmpdir.mkdir("dest").join("boost-1.55")
    qitoolchain.qipackage.extract(res, dest.strpath)
    assert dest.join("lib", "libboost.so").check(file=True)


def test_extract_modern(tmpdir):
    """ Test Extract Modern """
    src = tmpdir.mkdir("src")
    src.ensure("package.xml", file=True)
    src.ensure("lib", "libboost.so", file=True)
    output = tmpdir.join("boost.zip")
    res = qisys.archive.compress(src.strpath, output=output.strpath, flat=True)
    dest = tmpdir.mkdir("dest").join("boost-1.55")
    qitoolchain.qipackage.extract(res, dest.strpath)
    assert dest.join("lib", "libboost.so").check(file=True)


def test_installing_test_component(tmpdir):
    """ Test Installing Test Component """
    boost_path = make_fake_boost_package_dir(tmpdir)
    package = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    dest = tmpdir.join("dest")
    _installed = package.install(dest.strpath, components=["test", "runtime"])
    assert not dest.join("include", "boost.h").check(file=True)


def test_get_set_license(tmpdir):
    """ Test Get Set Licence """
    boost_path = tmpdir.mkdir("boost")
    boost_path.join("package.xml").write("""\n<package name="boost" version="1.58" />\n""")
    package = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    assert package.license is None
    package.license = "BSD"
    package2 = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    assert package2.license == "BSD"


def test_post_add_noop(tmpdir):
    """ Test Post Add Noop """
    boost_path = tmpdir.mkdir("boost")
    boost_path.join("package.xml").write("""\n<package name="boost" version="1.58" />\n""")
    package = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    package.post_add()  # no-op


def test_post_add_does_not_exist(tmpdir):
    """ Test Post Add Does Not Exist """
    boost_path = tmpdir.mkdir("boost")
    boost_path.join("package.xml").write(
        b"""\n<package name="boost" version="1.58" post-add="asdf" />\n"""
    )
    package = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    package.load_package_xml()
    with pytest.raises(qisys.command.NotInPath):
        package.post_add()


def make_fake_package_dir_with_so(tmpdir, name):
    """ make_fake_package_dir_with_so """
    package_dir = tmpdir.mkdir(name)
    package_dir.ensure("include", "%s.hpp" % name, file=True)
    package_dir.ensure("lib", "lib%s.so" % name, file=True)
    package_dir.ensure("package.xml", file=True)
    return package_dir


def make_fake_boost_package_dir(tmpdir):
    """ make_fake_boost_package_dir """
    return make_fake_package_dir_with_so(tmpdir, "boost")


@linux_only
@pytest.mark.skipif("True", "Need to be fixed when the feature is completed")
def test_post_add_rpath(tmpdir):
    """ Test Post Add Updates Runpath """

    # Set up a build worktree with a config
    worktree_dir = tmpdir.mkdir("worktree").strpath
    worktree = qisys.worktree.WorkTree(worktree_dir, sanity_check=True)
    build_worktree = qibuild.worktree.BuildWorkTree(worktree)
    toolchain_name = "mytoolchain"
    toolchain = qitoolchain.toolchain.Toolchain(toolchain_name)
    config_name = "myconfig"
    qibuild.config.add_build_config(config_name, toolchain=toolchain_name)
    build_worktree.set_default_config(config_name)

    # There are 3 projects to work with:
    # - alpha depends on nothing
    # - beta depends on alpha
    # - gamma depends on beta, but not directly on alpha
    this_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(this_dir, "projects")
    libalpha_name = "libalpha"
    libbeta_name = "libbeta"
    libgamma_name = "libgamma"

    def import_build_package(src_dir, project_name, worktree, toolchain):
        """Imports a project from a source directory to the worktree,
        builds it, packages it, adds it to the toolchain.
        """
        package_path = qisys.script.run_action("qibuild.actions.package", [project_name, "--worktree", worktree.root])
        qisys.script.run_action("qitoolchain.actions.add_package", ["-t", toolchain.name, package_path])
        toolchain.db.load() # Force reload the toolchain information
        return toolchain.get_package(project_name)

    def import_build_package_rm(src_dir, project_name, worktree, toolchain):
        """Imports a project from a source directory to the worktree,
        builds it, packages it, adds it to the toolchain, and then removes it.
        """
        package = import_build_package(src_dir, project_name, worktree, toolchain)
        worktree.remove_project(os.path.join(worktree.root, project_name), from_disk=True)
        return package

    # Process the libs to get them into the toolchain.
    libalpha_package = import_build_package_rm(projects_dir, libalpha_name, worktree, toolchain)
    libbeta_package = import_build_package_rm(projects_dir, libbeta_name, worktree, toolchain)
    libgamma_package = import_build_package_rm(projects_dir, libgamma_name, worktree, toolchain)

    # Check the .so files in the toolchains.
    readelf = qisys.command.find_program("readelf")
    runpath_matcher = re.compile("Library runpath: \\[(.*?)\\]")

    alpha_lib_path = os.path.join(libalpha_package.path, "lib")
    cmd = [readelf, "-d", os.path.join(alpha_lib_path, "libalpha.so")]
    output, _ = qisys.command.check_output_error(cmd)
    match = runpath_matcher.search(output.decode('utf-8'))
    assert match
    alpha_runpath = match.group()
    print("libalpha's runpath: %s" % alpha_runpath)

    beta_lib_path = os.path.join(libbeta_package.path, "lib")
    cmd = [readelf, "-d", os.path.join(beta_lib_path, "libbeta.so")]
    output, _ = qisys.command.check_output_error(cmd)
    match = runpath_matcher.search(output.decode('utf-8'))
    assert match
    beta_runpath = match.group()
    print("libbeta's runpath: %s" % beta_runpath)
    assert alpha_lib_path in beta_runpath

    gamma_lib_path = os.path.join(libgamma_package.path, "lib")
    cmd = [readelf, "-d", os.path.join(gamma_lib_path, "libgamma.so")]
    output, _ = qisys.command.check_output_error(cmd)
    match = runpath_matcher.search(output.decode('utf-8'))
    assert match
    gamma_runpath = match.group()
    print("libgamma's runpath: %s" % gamma_runpath)
    assert beta_lib_path in gamma_runpath


def test_version_str_to_int(tmpdir):
    """ Test version converter """
    assert qitoolchain.qipackage.version_str_to_int("1") == 1
    assert qitoolchain.qipackage.version_str_to_int("1.0") == 10
    assert qitoolchain.qipackage.version_str_to_int("1.0.2") == 102
    assert qitoolchain.qipackage.version_str_to_int("1.5.4") == 154
    assert qitoolchain.qipackage.version_str_to_int("1.5.0-r152") == 150


@skip_on_win
def test_post_add(tmpdir):
    """ Test Post Add """
    boost_path = tmpdir.mkdir("boost")
    boost_path.join("package.xml").write(
        b"""\n<package name="boost" version="1.58" post-add="post-add.sh hello world" />\n"""
    )
    script = boost_path.join("post-add.sh")
    script.write(
        '#!/bin/sh\n'
        'echo $@ > foobar\n'
    )
    os.chmod(script.strpath, 0o755)
    package = qitoolchain.qipackage.QiPackage("boost", path=boost_path.strpath)
    package.load_package_xml()
    package.post_add()
    with open(os.path.join(boost_path.strpath, 'foobar')) as f:
        txt = f.read()
    assert "hello world" in txt

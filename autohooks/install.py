# Copyright (C) 2019 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import shutil

from setuptools.command.develop import develop
from setuptools.command.install import install

from autohooks.config import load_config_from_pyproject_toml
from autohooks.utils import (
    get_git_hook_directory_path,
    get_autohooks_directory_path,
    get_pyproject_toml_path)


def get_pre_commit_hook_path():
    git_hook_dir_path = get_git_hook_directory_path()
    return git_hook_dir_path / 'pre-commit'


def get_pre_commit_hook_template_path():
    pyproject_toml = get_pyproject_toml_path()
    config = load_config_from_pyproject_toml(pyproject_toml)

    auto_install = config.get_auto_run()

    setup_dir_path = get_autohooks_directory_path() / 'precommit'
    if auto_install:
        return setup_dir_path / 'template_pipenv'
    return setup_dir_path / 'template'


def get_autohooks_pre_commit_hook():
    template_path = get_pre_commit_hook_template_path()
    return template_path.read_text()


def install_pre_commit_hook(pre_commit_hook, pre_commit_hook_path):
    pre_commit_hook_path.write_text(pre_commit_hook)


class AutohooksInstall:
    def install_git_hook(self):
        try:
            pre_commit_hook_path = get_pre_commit_hook_path()
            if not pre_commit_hook_path.exists():
                autohooks_pre_commit_hook = get_autohooks_pre_commit_hook()
                install_pre_commit_hook(
                    autohooks_pre_commit_hook, pre_commit_hook_path
                )
        except Exception:  # pylint: disable=broad-except
            pass


class PostInstall(install, AutohooksInstall):
    def run(self):
        super().run()
        self.install_git_hook()


class PostDevelop(develop, AutohooksInstall):
    def install_for_development(self):
        super().install_for_development()
        self.install_git_hook()

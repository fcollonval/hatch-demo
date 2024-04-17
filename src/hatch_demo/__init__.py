# SPDX-FileCopyrightText: 2024-present Frédéric Collonval <fcollonval@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
try:
    from ._version import __version__
except ImportError:
    __version__ = "dev"

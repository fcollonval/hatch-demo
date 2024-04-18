# SPDX-FileCopyrightText: 2024-present Frédéric Collonval <fcollonval@webscit>
#
# SPDX-License-Identifier: MIT
try:
    from ._version import __version__
except ImportError:
    __version__ = "dev"

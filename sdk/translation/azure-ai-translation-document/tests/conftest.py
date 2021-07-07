
# coding: utf-8
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import sys
from typing import List

# Ignore async tests for Python < 3.5
collect_ignore_glob = [] # type: List[str]
if sys.version_info < (3, 5):
    collect_ignore_glob.append("*_async.py")

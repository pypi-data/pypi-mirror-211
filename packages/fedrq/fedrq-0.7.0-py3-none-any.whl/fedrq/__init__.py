# SPDX-FileCopyrightText: 2022 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import logging

fmt = "{levelname}:{name}:{lineno}: {message}"
logging.basicConfig(format=fmt, style="{")
logger = logging.getLogger("fedrq")

"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os

## Important! This needs to not be dynamic if need to save sessions

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("QME_SERVER_KEY", "banana-banana-fo-fanna")

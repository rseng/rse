"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import random
import string


def main(args, extra):

    punctuation = "!#$%&()*+,-./:;<=>?@^_{|}~"
    choices = string.ascii_letters + string.digits + punctuation
    selected = [random.SystemRandom().choice(choices) for _ in range(50)]
    generated_key = "".join(selected)
    print(generated_key)

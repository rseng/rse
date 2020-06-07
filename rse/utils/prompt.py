"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


def confirm(prompt, response=False):
    """Used to prompt the user for a yes or no response, and returns True/False.
       This means we can use it like:
       if confirm("Would you like to do the thing?"):
          ....
    """
    prompt = "%s [%s]|%s: " % (prompt, "n", "y")
    while True:
        answer = input(prompt)
        if not answer:
            return response
        if answer not in ["y", "Y", "n", "N"]:
            print("Please respond with y or n.")
            continue
        if answer == "y" or answer == "Y":
            return True
        if answer == "n" or answer == "N":
            return False

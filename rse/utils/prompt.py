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


def choice_prompt(prompt, choices, choice_prefix=None, multiple=False):
    """Ask the user for a prompt, and only return when one of the requested
       options is provided.

       Parameters
       ==========
       prompt: the prompt to ask the user
       choices: a list of choices that are valid.   
       multiple: allow multiple responses (separated by spaces)
    """
    choice = None
    print(prompt)
    get_input = getattr(__builtins__, "raw_input", input)

    if not choice_prefix:
        choice_prefix = "/".join(choices)
    message = "[%s] : " % (choice_prefix)

    while choice not in choices:
        choice = get_input(message).strip()

        # If multiple allowed, add selection to choices if includes all vaid
        if multiple is True:
            contenders = choice.strip().split(" ")
            if all([x in choices for x in contenders]):
                choices.append(choice)
        message = "Please enter a valid option in [%s]" % (choice_prefix)
    return choice

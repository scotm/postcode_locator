__author__ = 'scotm'
import re

postcodeareas = set(
    ["AB", "DD", "DG", "EH", "FK", "HS", "IV", "KA", "KW", "KY", "ML", "PA", "PH", "TD", "ZE"] + ["G%d" % i for i in
                                                                                                  range(1, 10)])

postcodeprefix_re = re.compile("^"+"|".join(postcodeareas))
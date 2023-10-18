#!/usr/bin/env python3

import math

"""Preference function classes and generator."""


def make_pref_fct(preference_fct_type, ceils):
    """
    Returns a preference function object
    """
    if preference_fct_type == 1:
        pref_func = PreferenceType1()  # Binary preference
    elif preference_fct_type == 2:
        pref_func = PreferenceType2(ceils[0])  # Binary with threshold
    elif preference_fct_type == 3:
        pref_func = PreferenceType3(ceils[0])  # Linear starting at 0
    elif preference_fct_type == 4:
        pref_func = PreferenceType4(ceils[0], ceils[1])  # Step preference with 2 thresholds
    # elif preference_fct_type == 6:
    #     pref_func = PreferenceType6(ceils[0])  # Gaussian
    else:
        pref_func = PreferenceType5(ceils[0], ceils[1])  # Linear with 2 thresholds
    return pref_func


class PreferenceType1:
    """
    Classical-criterion.
    Total preference if any difference
    """

    def __init__(self):
        """Constructor."""
        self.p = 0
        return

    def value(self, diff):
        """Value."""
        return int(diff > 0)


class PreferenceType2:
    """
    Quasi-criterion.
    Total preference if diff > q
    """

    q, p = 0, 0

    def __init__(self, q=0):
        """Constructor."""
        self.q = q
        self.p = q

    def value(self, diff):
        """Value."""
        if (diff <= self.q):
            return 0
        return 1


class PreferenceType3:
    """
    Linear preferences and indifference zone.
    Indifference starts at 0
    """

    p = 1

    def __init__(self, p=1):
        """Constructor."""
        self.p = p

    def value(self, diff):
        """Value."""
        if (diff <= 0):
            return 0
        if (diff <= self.p):
            return diff / self.p
        return 1


class PreferenceType4:
    """
    Step function preferences and indifference zone.
    """

    q = 0
    p = 1

    def __init__(self, q=0, p=1):
        """Constructor."""
        self.q = q
        self.p = p

    def value(self, diff):
        """Value."""
        if (diff <= self.q):
            return 0
        if (diff <= self.p):
            return 0.5
        return 1


class PreferenceType5:
    """Linear preferences and indifference zone."""

    q = 0
    p = 1

    def __init__(self, q=0, p=1):
        """Constructor."""
        self.q = q
        self.p = p

    def value(self, diff):
        """Value."""
        if (diff <= self.q):
            return 0
        if (diff <= self.p):
            return (diff - self.q) / (self.p - self.q)
        return 1

    def to_string(self):
        return str(self.p) + "," + str(self.q)


'''
class PreferenceType6:

    """Gaussian preferences."""

    s = 0.5

    def __init__(self, s):
        self.s = s

    def value(self, diff):
        if (diff <= 0):
            return 0
        return 1 - math.exp(-diff * diff / (self.s*self.s*2))

class GeneralizedType5:

    """Symetric type5 criterion."""

    q = 0
    p = 1

    def __init__(self, q, p):
        """Constructor."""
        self.q = q
        self.p = p

    def value(self, diff):
        """Value."""
        if (abs(diff) <= self.q):
            return 0
        res = 0
        if(abs(diff) <= self.p):
            res = (abs(diff) - self.q)/(self.p - self.q)
        else:
            res = 1
        if (diff > 0):
            return res
        else:
            return - res

'''

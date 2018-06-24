"""This is custom dict child from
the Dict of in-build python data
type for custome access this class is been
used.
refer: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
"""


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

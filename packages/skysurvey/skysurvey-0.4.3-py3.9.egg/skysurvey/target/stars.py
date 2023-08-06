
import numpy as np
from .core import Target




class StableTarget( Target ):
    
    _KIND = "stable"
    _MODEL = dict( radec = {"model":"random",
                                "param":dict(ra_range=[0, 360], dec_range=[-30, 90]),
                                "as":["ra","dec"]},
                    magobs = {"model": "random_magobs",
                                "param": dict(zpmax=22.5)},
                   )
    
    @staticmethod
    def random_magobs(size=None, zpmax=22.5, scale=3):
        """ """
        exp_decay = np.random.exponential(scale=scale, size=size)
        return zpmax-exp_decay

    
class Star( StableTarget ):

    _KIND = "star"
    
    

# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 11:25:05 2023

@author: danie
"""
#https://engineeredjoy.com/blog/perlin-noise/

import noise
import numpy as np

def perlin_array(shape = (200, 200),
			scale=100, octaves = 6, 
			persistence = 0.5, 
			lacunarity = 2.0, 
			seed = None):

    if not seed:

        seed = np.random.randint(0, 100)
        print("seed was {}".format(seed))

    arr = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            arr[i][j] = pnoise2(i / scale,
                                        j / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=1024,
                                        repeaty=1024,
                                        base=seed)
    max_arr = np.max(arr)
    min_arr = np.min(arr)
    norm_me = lambda x: (x-min_arr)/(max_arr - min_arr)
    norm_me = np.vectorize(norm_me)
    arr = norm_me(arr)
    return arr
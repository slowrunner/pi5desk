#!/bin/env python3

# FILE:  create3_ir_dist.py

# Create3 ir_intensity values to *approximate* distance
#   using linear interpolation between empirical test values

#   The ir sensors are not albedo (surface reflectivity) independent
#   so the distances should not be granted great confidence

import numpy as np


LABELS = ["side_left", "left", "front_left", "front_center_left", \
              "front_center_right", "front_right", "right"]

# Tested with front surface of white baseboard 60mm floor to edge of dado

# Approximate distance from wall to bumper at range of 1.5cm to 40cm
DISTANCES = [ 0.400, 0.300, 0.200, 0.110, 0.050, 0.025, 0.015]

# Note Distance base_link to Bumper is 0.171 meter

# Average Reading Values For Distances
READINGS  = [
             [14   , 19   ,  73   , 336  , 1148  , 2469 , 3111],
             [21   , 35   ,  74   , 322  , 1252  , 3090 , 3481],
             [44   , 53   , 112   , 366  , 1162  , 2639 , 3412],
             [23   , 42   , 126   , 451  , 1385  , 2843 , 3514],
             [30   , 44   ,  94   , 353  , 1281  , 3118 , 3769],
             [24   , 38   ,  81   , 276  , 1176  , 2972 , 3745],
             [21   , 35   ,  88   , 410  , 1635  , 3596 , 3784],
            ]

def dist_ir_reading(sensor_idx, reading):
      UNDEF = -99.999
      dist = np.interp(reading,READINGS[sensor_idx],DISTANCES, right=UNDEF, left=UNDEF)
      return dist

def main():

  for reading in [0, 8, 10, 13, 25, 38, 57, 76, 114, 151, 366, 580, 1312, 2044, 2908, 3772, 3785, 3798, 4500] :
    print("reading: {}  dist: {:.3f} m".format(reading, dist_ir_reading(4,reading)))


if __name__ == "__main__":
  main()

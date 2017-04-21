#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 17:27:07 2017

@author: michaelsanders
"""

"""
Code for mapping every trap's relative position to every other trap in terms of a) distance (km) and b) compass bearing (in degrees).  Note, the bearing value shows bearings FROM other traps to the self trap.  This is intended to align to the wind bearing in the weather dataset, which depicts the direction the weather is coming FROM (http://www.ndbc.noaa.gov/measdes.shtml).
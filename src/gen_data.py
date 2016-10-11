#!/usr/bin/python
# -*- coding: utf-8 -*-

import random





#------------------------
# in order to generate <10's impression .
#------------------------
for i in range(1, 49):
    impression = random.randint(1, 10)
    click = random.randint(0, impression)
    print i, impression, click, click*1.0/impression

#------------------------
# ctr is in the range (0, 0.15)
#   
#------------------------
for i in range(50, 1000):
    impression = random.randint(1, 1000000)
    click = 0
    if impression > 10:
        click = random.randint(0, int(0.15*impression))
    else:
        click = random.randint(0, impression)
    print i, impression, click, click*1.0/impression

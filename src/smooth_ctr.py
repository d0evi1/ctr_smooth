#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from scipy.special import gamma
from scipy.special import digamma


#--------------------------------
# load all ad's impression/click to ciList.
#--------------------------------
def read_file():
    f = open("data.txt", "r")
    line = f.readline() 

    ciList = []
    while line:
        cols = line.strip().split(" ")
        impression = int(cols[1])
        click = int(cols[2])
        raw_ctr = cols[3]

        ciList += [(impression, click)]
        line = f.readline()

    f.close()
    
    return ciList

#----------------------------
# get one iteration's alpha/beta.
#----------------------------
def iter_once(alpha, beta, ciList):
    sum0 = 0.0
    sum1 = 0.0
    sum2 = 0.0 
    sum3 = 0.0

    for (I,C) in ciList:
        sum0 += digamma(C+alpha) - digamma(alpha)
        sum1 += digamma(I+alpha+beta) - digamma(alpha+beta)
        sum2 += digamma(I-C+beta) - digamma(beta)
        sum3 += digamma(I+alpha+beta) - digamma(alpha+beta)

    alpha = alpha * (sum0 / sum1)
    beta = beta * (sum2 / sum3)

    return alpha,beta 

#------------------------------
# smooth the raw click/impression: ciList. 
#------------------------------
def smooth_ctr(iter_num, alpha, beta, ciList):
    i = 0
    while i < iter_num:
        print "iter:%d. alpha=%s,beta=%s" % (i,alpha, beta)    
        prev_alpha = alpha 
        prev_beta = beta 
     
        alpha, beta = iter_once(alpha, beta, ciList)

        ## early-stopping
        if abs(alpha - prev_alpha) < 1E-10 \
                and abs(beta - prev_beta) < 1E-10:
            break
    
        i+=1

    return alpha, beta

#--------------------------
# save file.
#--------------------------
def save_file(ciList, alpha, beta):
    f2 = open( 'output.txt', 'w')

    f2.write("I C sctr rctr\n")
    for (I,C) in ciList:
        f2.write("%s %s %s %s\n" %(I, C, (C+alpha)/(I+alpha+beta), C*1.0/I))

    f2.close()


#-------------------------------------------
## 
## paper: http://www.cs.cmu.edu/~xuerui/papers/ctr.pdf
##
## alpha/(alpha+beta): mean of beta distribution.
## alpha/(alpha+beta) must be close to your global ctr.
## gamma(alpha, beta) must be close to your global ctr.
## get your prior alpha、beta!
##-------------------------------------------
if __name__ == '__main__':
    iter_num = 1000
    alpha = 1.0
    beta = 1000.0

    ciList = read_file()

    alpha,beta = smooth_ctr(iter_num, alpha, beta, ciList)
    print "final alpha=%s,beta=%s" % (alpha, beta)

    print "start to save file..."
    save_file(ciList, alpha, beta)


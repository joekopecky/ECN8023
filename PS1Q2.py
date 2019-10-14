#Author: Joe Kopecky
##########################################################################################
##########################################################################################
#Code to solve the deterministic neoclassical growth model with value function iteration##
##########################################################################################
##########################################################################################

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import math 




#Define Parameters Used#############
alpha = 0.3
beta  = 0.9
tol = 0.01
diff = 1
#grid of possible k 

###NB I told you to do this for a really coarse grid, that was to accommodate the possibility
#of doing this in a highly `brute force' kind of way. Here the only programming difference is 
#setting this nk to a lower number to get the same points so we might as well at least make our 
#graphs at the end look pretty. 
nk = 100
k = np.linspace(0.01,.99,nk)

#initialize vectors for the initial guesses of k', V0 and to then fill in for V1 and policy function g
guess = np.zeros(nk)
V0 = np.zeros(nk)

#number of iterations (maybe we'll use this)
nIter = 20
#Define utility function 
def utility(c):
    u = math.log(c)
    return(u)

def prod(k):
    y = k**alpha
    return(y)


def T(v):
    #implements the Bellman operator
    Tv = []
    vals = []
    ##This outer loop is going through all of our states k
    for x in range(nk):
        #This inner loop then creates a value "r" for each possible choice variable (here a) 
        for a in range(nk):
            #First define the consumption value associated with the choice of a in the utility function.
            if (prod(k[x])-k[a]>0):
                c = prod(k[x])-k[a]
            else:
                ##If you didn't do this if/else you'd find yourself with errors because you'd be including choices that violate o
                #the assumption that consumption is always positive. You could solve this another more rigorous way, but I'm just
                #choosing to assign a minimal value to c that shouldn't ever be optimal. If you do this in code you care more about
                #I think it's fine but make sure you check that you're not somehow finding a solution that comes from one of these
                #work arounds (i.e. if c=0.0001 proves optimal then something's wrong... probably in the code)
                c= 0.00000001
            r = utility(c) + beta*v[a]
            vals.append(r)
            
        #store the maximum value for this x in the list Tv
        Tv.append(max(vals))
    return Tv

ValueApprox = []
ValueApprox.append(V0)
#Because we've functionalized most of the hard work, the actual recursion now looks surprisingly straightforward. 
#we set the tolerance to 0.01 (max difference allowed), you can set one that's more/less strict if you'd like. 
while diff > tol:
    #Generate new value function by applying the T operator
    V1 = T(V0)
    #the following line just saves each iterated value function so we can graph them later
    ValueApprox.append(V1)
    #check the max difference between the two functions
    diff = max([np.abs(v1-v0) for v1, v0 in zip(V1,V0)])
    #replace V0 with the new value function V1
    V0 = V1
    #print the difference so we can keep track of the convergence
    print(diff)

print("you've just converged!")


##########################################################################
###TRUE VALUE FUNCTION
#FROM KRUEGER NOTES GUESS AND VERIFY
B = alpha/(1-alpha*beta)

A = (1/(1-beta))*(1)/(1-alpha*beta)*((alpha*beta)*math.log(alpha*beta) + (1-alpha*beta)*math.log(1-(alpha*beta)))
TrueValue = []
for i in range(nk):
    TrueValue.append(B*math.log(k[i]) + A)
#############################################################################



plt.figure(figsize=(10,7.5))
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
for i in range(len(ValueApprox)):
    plt.plot(k,ValueApprox[i],color = 'b')


plt.plot(k,TrueValue, color = 'r')
plt.xlim(0,1)
#You can save the file with: 
plt.savefig("C:/Users/Joe/Dropbox/teaching/PhDCourse/code/ValueIteration.pdf",bbox_inches ="tight")
#################################################################

    
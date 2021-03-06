# S. Zenz, Imperial College
# April 2015
# A starting script to fit a simulated Higgs boson lineshape ("pseudodata")

import numpy as np
import matplotlib.pyplot as plt

# If random seed set to None, random seed set at rantime so result is non-reproducible
#seedval = None

# Set value to get reproducible successful example (if parameters of script unchanged)
seedval = 54321

# Set value to get reproducible example of failure
#seedval = 123456

# wide, but more or less ok
#seedval = 123

# Properties of pseudodata
mh = 125
res = 2.
powerlawcutoff = 240.
powerlawpower = 3.5
nbkg = 50000
nsig = 1000

# Mass range and bin properties
min = 100.
max = 180.
binwidth = 1.
bincenters = bincenters = np.linspace(min+0.5,max-0.5,(max-min)/binwidth)
binedges=np.linspace(min,max,(max-min)/binwidth+1)

# Produce pseudodata
# Note this is a wonky model that's not the same as the fit model later
# It's more like real data that way!
np.random.seed(seedval)
signal = np.random.normal(mh,res,nsig)
signal = signal[signal < 180.]
bkg = (powerlawcutoff-(powerlawcutoff-min)*np.random.power(powerlawpower,nbkg))
bkg = bkg[bkg < 180.]
all = np.concatenate((signal,bkg))

# Build pseudodata histogram and plot axes
h_all = plt.hist(all,bins=binedges,histtype='step')
plt.clf()
plt.title("Fitting to the Higgs boson")
plt.xlabel("mass")
plt.ylabel("number of Higgs boson candidates")

# Plot pseudodata histogram 
# with uncertainty bands defined by the sqrt of number of entries per bin
xdata = bincenters
ydata = h_all[0]
ydataunc = np.sqrt(h_all[0])
plt.errorbar(xdata,ydata,xerr=binwidth,yerr=ydataunc,color="b",linestyle='none',label = "Pseudodata")
plt.xlim(min,max)

# Define functions for fitting
from scipy.optimize import leastsq
def fsig(p,m):
    fitmean = p[0]
    fitsigma = p[1]
    fitnorm = p[2]
    return (fitnorm/np.sqrt(2*np.pi*fitsigma))*(np.exp(-0.5*((m-fitmean)/fitsigma)**2))
def fbkg(p,m):
    return (p[0]/m**4+p[1]/m**5)
def ftot(p,m):
    return fsig(p[:3],m)+fbkg(p[3:],m)
def errfunc(p,m,y):
    return ftot(p,m)-y

# Initial values
# Fit is very sensitive to these - maybe you can fix this!
p0 = [130,1.,200.,10**10,10**10]

print
print "Initial guesses:"
print "\tMass:",p0[0]
print "\tWidth:",p0[1]
print "\tNumber:",p0[2]
print "\tBackground params:",p0[3:]
print

print "Fitting now, you can probably ignore sqrt errors..."
print
p1, success = leastsq(errfunc,p0[:],args=(xdata,ydata))
print
print "... done fitting."
print

print "Fit results:"
print "\tMass:",p1[0]
print "\tWidth:",p1[1]
print "\tNumber:",p1[2]
print "\tBackground params:",p1[3:]

print "True answers from pseudodata generation:"
print "\tMass:",mh
print "\tWidth:",res
print "\tNumber:",len(signal)
print

# Plot final result
xplot = bincenters
plt.plot(xplot, ftot(p1, xplot), "r-",label="Fit (Total)") 
plt.plot(xplot, fbkg(p1[3:],xplot),"r.",label="Fit (Background)")
plt.legend(numpoints=1,frameon=False)
plt.show()


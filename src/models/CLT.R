# CLT.
# a simple model meant to investigate the central limit theorem 

# the central limit theorem says that as any one-dimensional variate is sampled more
# the mean of that variate goes
# But the rate of convergence is only glossed over when it's taught
# despite that being a very useful measure.

beta = function(n) { rbeta(n, 1/2, 1) }
bernoulli = function(n, p = .3) { rbinom(n, 1, p) }
binomial = function(n, p = .3) { rbinom(n, 333, p) } # a Bin(333, p) variate with mean p*333 
normal = function(n) { rnorm(n, NORMAL.VARIANCE, NORMAL.MEAN) }

# Model Parameters
# 

dist = "binomial"
NORMAL.VARIANCE = 7
NORMAL.MEAN = -3

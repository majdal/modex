Statistics
==========

A _statistic_ is some value that can be computed from data (the statisticians distinguish statistics from other sorts of variables, especially model parameters, which cannot be computed from data). This page contains a list of all the sorts of _statistics_ our model explorer will support. This list also includes things which are not traditionally considered statistics, but which nevertheless are computed algorithmically from a dataset.


## Numerical Types

### Summary

* Mean
* Quantiles
    * Median
    * Quartiles 
* Mode(s)
* Variance

### Uncertainty

* {Confidence,Credible} intervals


### Smoothers

There are at least two kinds of smoothing: distribution (1 dimensional) smoothing and function (2 dimensional) smoothing. The basic techniques can be adapted to either purpose.

* Running averages
* Running medians
* Running variances
* Kernel density estimates

## Network Types

* Centrality
    * [all the many variations on centrality]
* (everything [pajek](http://vlado.fmf.uni-lj.si/pub/networks/Pajek/) supports) 


### Timeseries-specific


* [DW Test](https://en.wikipedia.org/wiki/Durbin%E2%80%93Watson_statistic)


## Causal Maps

* R's [dpa](http://cran.r-project.org/web/packages/dpa/) 
* [TETRAD](http://www.phil.cmu.edu/projects/tetrad/)
* [CauseEffect](http://www.causality.inf.ethz.ch/cause-effect.php?page=help) of the Kaggle Contest of the [same name](http://www.kaggle.com/c/cause-effect-pairs)


## Generic dependencies for doing statistics

* [R](http://r-project.org) (of course)
* [Pandas](http://pandas.pydata.org/)
* [Theano](http://deeplearning.net/software/theano/) (CPU and GPU compiler)
* [PyLearn2](http://deeplearning.net/software/pylearn2/) (Deep Learning research platform)
* [Hyperopt](http://hyperopt.github.io/hyperopt/) (Distributed Bayesian Optimization)


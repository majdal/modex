(todo: as we figure out the sorts of visualizations)
(check out [[Datasets]] to get a feel for the **type** of visualizations we need)

For this to be any use, this tool desperately must limit the cognitive burden on the user. That means easy-to-learn, attractive maps and plots with details-on-demand, and probably information reduction.

## Uncertainty 
In our [[Modelling]], we care deeply about compuing estimates of the uncertainty in our models (e.g. confidence intervals or credible intervals) (which we can do, see [[Modelling]] for details on that, if that section has been written yet, which it probably hasn't if this comment is still here -nick).

We have been calling these "salience plots" but you can't google that. There is some example code to do it in R and Matlab by Solomon Hsiang at [his blog](http://www.fight-entropy.com/2012/08/watercolor-regression.html). It seems like very few have seriously thought about this before, beyond including error bars, and there is simply no standard terminology for it.

But a _**warning**_: it seems that these authors are puporting to show the density, the chance that a measure is actually at a particular value, but they are doing it based on CIs. This is incorrect. A CI provides with high probability a region in which the measure is in; it does not in itself provide a weighting of where in that region the value is likely to be.  Ask @tcstewar or @kousu for more details. _(still, I think there is some merit to showing this sort of thing, we know that CIs get smaller and more accurate with more data, if there is a true value for them to be accurate around,  -nick)_

Here's an example of a timeseries plot with uncertainty listed as a heatmap ![Salience Plot](https://github.com/majdal/modex/raw/master/wiki_overflow/salience.png)
And here's the "Watercolor Regression" demo from Solomon ![Watercolor Regression](https://github.com/majdal/modex/raw/master/wiki_overflow/smooth_overlaid.jpg)

## Cartographic

 ---we need to handle zooming smoothly, going from different types, and as we do this we need maintain context for the user. googlemaps does this by fading out layers as more detailed tiles are loaded-in

## Network

(idea: check out Sheelagh Carpendale's transmogrification and Visits work)
For networks that are actually trees: [egonetwork pandemic visualization](http://rocs.hu-berlin.de/projects/hidden/index.html)
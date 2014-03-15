# Map Data

Here lies all of our static map content. GIS data is getting more open, but it is expensive to produce and the owners tend to cling to it closely.

**Thus:**

1. Non-free maps are in a zip file available from a team member after signing the appropriate data release forms.
**DO NOT ACCIDENTALLY COMMIT THEM TO THE REPO**, even as a derived file.
 See [the developer's guide](../../src/README.md#keeping-copyrighted-data-out) on our procedure for preventing this.

1. For open data we do have, the license MUST clearly be stated.
Every dataset D.xyz in this folder is shadowed by a D.xyz.license file.
**DO NOT commit a dataset without also committing its license terms.**

# Interesting Datasets Here:

Not all of these 

* elora.geo.json - the farm fields in the elora area - _this is private__
* elora.topo.json - the same in compressed topojson format (only polygons, no data fields) - _this is private__
* meatplants.geojson - abbatoirs and butchershops in Ontario
* countries.geojson - countries of the world, snitched from the ol3 examples
 

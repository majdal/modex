# Map Data

Here lies all of our static map content. GIS data is getting more open, but it is expensive to produce and the owners tend to cling to it closely.

**Thus:**

1. Non-free maps are in a zip file available from a team member after signing the appropriate data release forms.
**DO NOT ACCIDENTALLY COMMIT THEM TO THE REPO**. They are explicitly disallowed by the .gitignore in this folder,
 but you still might stuff in a descendant file, and once a piece of data is in git it is very very hard to erase.
  * if we do need to erase it, [github has a guide](https://help.github.com/articles/remove-sensitive-data)
1. For open data we do have, the license MUST clearly be stated.
Every dataset D.xyz in this folder is shadowed by a D.xyz.license file.
**DO NOT commit a dataset without also committing its license terms.**

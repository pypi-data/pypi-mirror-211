# My Favorite Things
 Convenient functions and classes I use too often. If Coltrane was a programmer (_shudder_) and much worse.

## Installation
Install with
```
pip install my-favorite-things
```

## Current Methods
### save
#### `save()`
Import by
```
from my_favorite_things import save
```
This method is used for saving data to a file. You can save as an `.npz` file for numpy array(s) or as a `.pkl` file for dictionaries and other odd python objects. By default, it will not overwrite existing files but instead append a number onto the end of file name (the keywords being, by default, `overwite=False` and `append=True`). You can save relative to your current directory (`absolute=False`) or as an absolute path (`absolute=True`). Addtionally, double check that you're saving to the correct directory with `dryrun=True`. Check the doc string for more info.

---

### ddict
#### `nested_ddict()`
Import by
```
from my_favorite_things import nested_ddict
```
This method allows for creating a nested defaultdictionary. This is useful if you have data that is dependent on multiple parameters that are heirarchical. For example, if we do
```python
d = nested_ddict(3, list)
```
then we can use it as
```python
d['zero']['one']['two']['three'].append(datum)
```

#### `format_ddict()`
Import by
```
from my_favorite_things import format_ddict
```
This method will format your (nested) defaultdictionary into dictionaries. Additionally, it can turns lists in numpy arrays and/or sort the lists too.

---

# brainwalk

::: {.cell 0=‘h’ 1=‘i’ 2=‘d’ 3=‘e’}

``` python
import sys
sys.path.append("..")
from brainwalk.core import *
```

:::

> Spatial graph embeddings for ObsidianMD

## Install

``` sh
pip install brainwalk
```

## How to use

``` python

# Find the Obsidian Vault directory and assert that it exists
import os
from pathlib import Path
vault_dir = Path(os.getcwd()) / 'vault-stub'
assert vault_dir.exists()

# Retrieve a Gensim word2vec model of your Obsidian Graph
from brainwalk.core import brainwave, jaccard_coefficient

model = brainwave(vault_dir,jaccard_coefficient)
```

``` python
model.wv.key_to_index
```

    {'Causam mihi': 0,
     'Alimenta': 1,
     'Brevissimus moenia': 2,
     'Sussudio': 3,
     'Ne fuit': 4,
     'Vulnera ubera': 5,
     'Bacchus': 6,
     'Virtus': 7,
     'Amor': 8,
     'Tarpeia': 9,
     'American Psycho (film)': 10,
     'Tydides': 11,
     'Manus': 12,
     'Vita': 13,
     'Aras Teucras': 14,
     'Dives': 15,
     'Aetna': 16,
     'Isolated note': 17,
     'lipsum/Isolated note': 18,
     'Caelum': 19}

``` python
model.wv.most_similar("Vulnera ubera")
```

    [('Sussudio', 0.9991790056228638),
     ('Aetna', 0.9991780519485474),
     ('Tydides', 0.9991397857666016),
     ('Bacchus', 0.9991208910942078),
     ('Virtus', 0.9990988373756409),
     ('Brevissimus moenia', 0.9990975260734558),
     ('Ne fuit', 0.9990928769111633),
     ('Dives', 0.9990816116333008),
     ('Alimenta', 0.9990617036819458),
     ('Amor', 0.9990396499633789)]

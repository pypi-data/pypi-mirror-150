[![PyPI version](https://badge.fury.io/py/keras-bcr.svg)](https://badge.fury.io/py/keras-bcr)
[![PyPi downloads](https://img.shields.io/pypi/dm/keras-bcr)](https://img.shields.io/pypi/dm/keras-bcr)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/satzbeleg/keras-bcr.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/keras-bcr/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/satzbeleg/keras-bcr.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/keras-bcr/context:python)

# keras-bcr : Batch Correlation Regularizer for TF2/Keras
The batch correlation regularization (BCR) technique adds a penalty loss
if the inputs and outputs before the skip-connection of a specific feature element are correlated.
The correlation coefficients are computed for each feature element seperatly across the current batch.

~~For further information please read Ch.??? in [link to paper]().~~

## Usage

```py
from keras_bcr import BatchCorrRegulizer
import tensorflow as tf

# The BCR layer is added before the addition of the skip-connection
def build_resnet_block(inputs, units=64, activation="gelu",
                       dropout=0.4, bcr_rate=0.1):
    h = tf.keras.layers.Dense(units=units)(inputs)
    h = h = tf.keras.layers.Activation(activation=activation)(h)
    h = tf.keras.layers.Dropout(rate=dropout)(h)
    h = BatchCorrRegulizer(bcr_rate=bcr_rate)([h, inputs])  # << HERE
    outputs = tf.keras.layers.Add()([h, inputs])
    return outputs

# An model with 3 ResNet blocks
def build_model(input_dim):
    inputs = tf.keras.Input(shape=(input_dim,))
    h = build_resnet_block(inputs, units=input_dim)
    h = build_resnet_block(h, units=input_dim)
    outputs = build_resnet_block(h, units=input_dim)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model

INPUT_DIM = 64
model = build_model(input_dim=INPUT_DIM)
model.compile(optimizer=tf.keras.optimizers.Adam(), loss="mean_squared_error")

BATCH_SZ = 128
X_train = tf.random.normal([BATCH_SZ, INPUT_DIM])
y_train = tf.random.normal([BATCH_SZ])

history = model.fit(X_train, y_train, verbose=1, epochs=2)
```


## Citation
Please considering citing 

```
Forthcoming
```


## Appendix

### Installation
The `keras-bcr` [git repo](http://github.com/satzbeleg/keras-bcr) is available as [PyPi package](https://pypi.org/project/keras-bcr)

```sh
pip install keras-bcr
pip install git+ssh://git@github.com/satzbeleg/keras-bcr.git
```

### Install a virtual environment

```sh
python3.7 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/satzbeleg/keras-bcr/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/keras-bcr/compare/).

[![PyPI version](https://badge.fury.io/py/keras-cor.svg)](https://badge.fury.io/py/keras-cor)
[![PyPi downloads](https://img.shields.io/pypi/dm/keras-cor)](https://img.shields.io/pypi/dm/keras-cor)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/satzbeleg/keras-cor.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/keras-cor/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/satzbeleg/keras-cor.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/keras-cor/context:python)

# keras-cor : Correlated Outputs Regularization
Add a regularization if the features/columns/neurons the hidden layer or output layer should be correlated. The vector with target correlation coefficient is computed before the optimization, and compared with correlation coefficients computed across the batch examples.

## Usage
See [demo notebook](demo/Correlated%20Outputs%20Regularization.ipynb)

```py
from keras_cor import CorrOutputsRegularizer
import tensorflow as tf

# Simple regression NN
def build_mymodel(input_dim, target_corr, cor_rate=0.1, 
                  activation="sigmoid", output_dim=3):
    inputs = tf.keras.Input(shape=(input_dim,))
    h = tf.keras.layers.Dense(units=output_dim)(inputs)
    h = tf.keras.layers.Activation(activation)(h)
    outputs = CorrOutputsRegularizer(target_corr, cor_rate)(h)  # <= HERE
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model

# Gneerate toy dataset
BATCH_SZ = 128
INPUT_DIM = 64
OUTPUT_DIM = 3

X_train = tf.random.normal([BATCH_SZ, INPUT_DIM])
y_train = tf.random.normal([BATCH_SZ, OUTPUT_DIM])

# Normally you should comput `target_corr` based on your target outputs `y_train`
# e.g., target_corr = tf.constant(y_train)
# However, you can also use subjective correlations (aka expert opinions), e.g.,
target_corr = tf.constant([.5, -.4, .9])

# Optimization
model = build_mymodel(input_dim=INPUT_DIM, target_corr=target_corr, output_dim=OUTPUT_DIM)
model.compile(optimizer=tf.keras.optimizers.Adam(), loss="mean_squared_error")
history = model.fit(X_train, y_train, verbose=1, epochs=2)

# Inference
yhat = model.predict(X_train)
rhos = pearson_vec(yhat)
rhos
```

## Appendix

### Installation
The `keras-cor` [git repo](http://github.com/satzbeleg/keras-cor) is available as [PyPi package](https://pypi.org/project/keras-cor)

```sh
pip install keras-cor
pip install git+ssh://git@github.com/satzbeleg/keras-cor.git
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
Please [open an issue](https://github.com/satzbeleg/keras-cor/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/keras-cor/compare/).

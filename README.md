
<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/python.svg" width="100" />
<br>
Python Reinsurance Computation
</h1>

<img src="https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=NumPy&logoColor=white" alt="" />
<img src="https://img.shields.io/badge/Dask-FDA061.svg?style=for-the-badge&logo=Dask&logoColor=black" alt="cloudpickle" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="packaging" />
</p>

</div>

---

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Basic example](#basic-example)
  - [Running Tests](#running-tests)
- [Future Development](#future-development)
- [Contributing](#contributing)
- [License](#license)

---


## Overview

Reinsurance is a python package that intends to provide a framework for reinsurance computation. It is built on top of [NumPy](https://numpy.org/) and [Dask](https://dask.org/). It is designed to be modular, fast and easy to use. Leveraging the power of Dask, it can perform parallel and distributed computation to allow for large scale reinsurance computation. It is still in very early development.

## Features

* `N-dimensional array computation`
* `Parallel computation`
* `Distributed computation`
* `Lazy evaluation`
* `Visualization using network graphs`

---


<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-github-open.svg" width="80" />

## Project Structure

```
src
   |-- reinsurance
   |   |-- __init__.py
   |   |-- layers
   |   |   |-- core.py
   |   |   |-- non_proportional.py
   |   |   |-- proportional.py
   |   |-- models
   |   |   |-- model.py
.gitignore
LICENSE
Makefile
pyproject.toml
requirements-dev.txt
requirements.txt
```

---

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-src-open.svg" width="80" />

## Getting Started

### Installation

1. Clone the reinsurance repository:
```sh
git clone https://github.com/cbalona/reinsurance
```

2. Change to the project directory:
```sh
cd reinsurance
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### Basic example

```python
import numpy as np
from reinsurance.layers.core import Input, Recovery, ReinstatementPremium
from reinsurance.layers.non_proportional import ExcessOfLossLayer
from reinsurance.layers.proportional import QuotaShare
from reinsurance.models.model import Model

# Define the input layers
gross_losses = np.array([[100, 100, 100], [50, 50, 50], [20, 20, 20]])
losses = Input(name="losses")(gross_losses)

# Define the structure
qs = QuotaShare(name="qs", cession=0.4, commission=0.1)(losses)
qs_recovery = Recovery()(qs)

xol_1 = ExcessOfLossLayer(
    name="xol_1", attachment=25, width=25, rate_on_line=0.1, reinstatements=2
)(losses - qs_recovery)
xol_2 = ExcessOfLossLayer(
    name="xol_2", attachment=50, width=100, rate_on_line=0.1, reinstatements=2
)(losses - qs_recovery)

xol_recovery = Recovery()(xol_1) + Recovery()(xol_2)
xol_premium = ReinstatementPremium()(xol_1) + ReinstatementPremium()(xol_2)

# Get net losses
net = losses - qs_recovery - xol_recovery - xol_premium

# Define the model and compute the result
model = Model(
    input_layers=[losses], output_layers=[net]
)
net_result = model.compute()
print(np.array(net_result[0]))
model.visualize()
```

```sh
[[21.5 21.5 24. ]
 [24.5 24.5 24.5]
 [12.  12.  12. ]]
```
<img src="https://imgur.com/mYtD3HP" height=1080>


### Running Tests
```sh
TBD
```

<hr />


## Future Development
Still in very early development. The following features are planned for future releases:
- [ ] Add more layers
- [ ] Add more tests
- [ ] Add more documentation
- [ ] Add more examples
- [ ] Add more visualizations
- [ ] Add more features
- [ ] Add more...


---

## Contributing
Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a pull request to the original repository.
Open a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.

The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## License

This project is licensed under the `MPL 2.0` License. See the LICENSE file for additional info.

---



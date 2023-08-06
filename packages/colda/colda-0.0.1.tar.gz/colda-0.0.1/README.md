## Introduction
ColDA  is an open source project aimed at providing distributed machine learning tools for data analysis and machine learning based on [Assisted Learning](https://assisted-learning.org/).

## Package

### Getting Started

### Use case

- Examples and Instructions can be found in `examples/`

### Package Stucture

- Basic package structure can be found in [Github repository](https://github.com/AlexIoannides/py-package-template)

- Compared to the Basic package structure, ``docs/`` will contain different element. But at this point, you can follow the template

- ``py-pkg`` is the main part of the package, you can add more modules (with ``__init__.py``) in this part. For example, if you add ``temp`` module, you can import ``temp`` module by:

```bash
import temp from py-pkg
```

- This package structure can be improved by learning [PyTorch](https://github.com/pytorch/pytorch) package structure.

- Basic Structure: 

```bash
py-package-tempate/
 |-- docs/
 |-- |-- build_html/
 |-- |-- build_latex/
 |-- |-- source/
 |-- py-pkg/
 |-- |-- __init__.py
 |-- |-- __version__.py
 |-- |-- curves.py
 |-- |-- entry_points.py
 |-- tests/
 |-- |-- test_data/
 |-- |   |-- supply_demand_data.json
 |-- |   __init__.py
 |-- |   conftest.py
 |-- |   test_curves.py
 |-- .env
 |-- .gitignore
 |-- Pipfile
 |-- Pipfile.lock
 |-- README.md
 |-- setup.py
```


### How to Manage Package Environment

- ``pipenv`` is used to manage package. You can install ``pipenv`` by:

```bash
pip3 install pipenv
```

- Use ``pipenv`` to install package. The first command is to install the package for development. The second command is to install the package for production.

```bash
pipenv install --dev
pipenv install 
```

- Use ``pipenv`` to uninstall package:

```bash
pipenv uninstall
```

### Pipenv Shells

- Entering into a Pipenv-managed shell. Remeber doing this **every time** before running the project. 

```bash
cd py-package-tempate
pipenv install
pipenv shell
```


## License

ColDA is licensed under the [Apache 2.0 License](LICENSE).  

## Code of Conduct

Please review and adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) when contributing to ColDA.  



## Reference
Please use the following reference
```bibtex
@article{diao2022gal,
  title={GAL: Gradient Assisted Learning for Decentralized Multi-Organization Collaborations},
  author={Diao, Enmao and Ding, Jie and Tarokh, Vahid},
  journal={Advances in Neural Information Processing Systems},
  volume={35},
  pages={11854--11868},
  year={2022}
}
```



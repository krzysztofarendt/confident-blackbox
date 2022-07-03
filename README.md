# confident-blackbox

This package is under development and not ready to be used.

## Installation

Please note, that currently the dependencies are listed only in `requirements.in` and must by compiled with `pip-compile`.
There are no dependencies in `setup.py` at the moment.

```
git clone https://github.com/krzysztofarendt/confident-blackbox
cd confident-blackbox
virtualenv -p python3 venv
source venv/bin/activate
pip install pip-tools
pip-compile
pip-sync
pip install -e .
```

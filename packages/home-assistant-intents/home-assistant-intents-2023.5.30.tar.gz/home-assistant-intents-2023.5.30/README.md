# Home Assistant Intents Package

Packaging for [intents](https://github.com/home-assistant/intents/)


## Install

Clone the repo and create a virtual environment:

``` sh
git clone --recursive https://github.com/home-assistant/intents-package
cd intents-package
python3 -m venv venv
venv/bin/pip3 install --upgrade pip
venv/bin/pip3 install -r requirements.txt
```


## Package

Update the submodule

``` sh
git submodule update --remote
```

Bump the version in `pyproject.toml` to `YYYY.M.D`

Generate dist:

``` sh
script/package
```

Upload `.tar.gz` and `.whl` to PyPI.

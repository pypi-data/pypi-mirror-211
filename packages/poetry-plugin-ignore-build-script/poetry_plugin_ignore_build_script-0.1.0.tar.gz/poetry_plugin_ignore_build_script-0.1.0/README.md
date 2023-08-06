# poetry-plugin-ignore-build-script

## Description

*poetry-plugin-ignore-build-script* is a
[plugin](https://python-poetry.org/docs/master/plugins/) for
[poetry](https://python-poetry.org/), the Python packaging and dependency
manager. It enables creating either plaform specific or pure python wheels.

### Installation

Follow poetry's [plugin installation instructions](https://python-poetry.org/docs/master/plugins/#using-plugins), replacing `poetry-plugin` with `poetry-plugin-ignore-build-script`.


## Usage

If you set up a build script in your pyproject.toml files as follows:

```toml
...

[tool.poetry.build]
script = "build.py"
generate-setup-file = true

...
```

and corrresponding build script which uses [mypycify](https://mypyc.readthedocs.io/en/latest/getting_started.html) or [cythonize](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiling-with-the-cythonize-command):

```python
from mypyc.build import mypycify

modules = [
    "my_package/submod1/foo.py",
    ...
    "my_package/submodn/bar.py",
]
extensions = mypycify(modules)

# from Cython.Build import cythonize
#extensions = cythonize("my_package/*.pyx", include_path=[...])

def build(setup_kwargs):
    setup_kwargs.update(
        {
            "ext_modules": extensions,
        }
    )
```

To build a non platform specific wheel (e.g. "my-package-0.1.1-py3-none-any.whl") then use the following command:

```sh
poetry build --ignore-build-script
```

To build a platform specific wheel (e.g. "my-package-0.1.1-cp310-cp310-manylinux_2_35_x86_64.whl") then use the standard poetry command:

```sh
poetry build
```


## Notes

This plugin is a way to workaround poetry limitation [#8039](https://github.com/python-poetry/poetry/issues/8039).
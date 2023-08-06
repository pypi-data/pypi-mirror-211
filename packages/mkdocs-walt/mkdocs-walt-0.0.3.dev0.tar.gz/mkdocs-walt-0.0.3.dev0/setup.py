from setuptools import setup, find_packages

VERSION = '0.0.3-dev'

LONG_DESCRIPTION = '''
# mkdocs-walt: a minimal documentation theme for MkDocs

Walt is a minimal documentation theme that is best suited for single page websites.

## Installation

```sh
pip install mkdocs-walt
```

## Usage

Create a new MkDocs project with the `mkdocs` CLI and add the following your
project's `mkdocs.yml`:

```yaml
theme:
  name: walt
```

See the [full usage example](https://github.com/codesue/walt/examples/mkdocs).

## Acknowledgements

Walt uses [writ.css](https://github.com/programble/writ/tree/master) for styles
and [Catppuccin](https://github.com/catppuccin/catppuccin) for dark mode
color palettes.
'''

setup(
    name='mkdocs-walt',
    version=VERSION,
    author='Suzen Fylke',
    author_email='codesue@users.noreply.github.com',
    description='A minimal theme for MkDocs',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/codesue/walt',
    license='GPLv3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['mkdocs'],
    entry_points={
        'mkdocs.themes': [
            'walt = walt',
        ]
    },
    zip_safe=False
)

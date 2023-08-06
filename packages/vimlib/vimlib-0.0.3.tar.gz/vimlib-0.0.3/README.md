[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A friendly interface for interacting with Vim using Python.

# Installation

`pip install vimlib`

**Recommended**: Using your chosen virtual environment, that's been setup for
Vim, or Neovim, to use, install `vimlib` using that.

Examples:

* `~/vimfiles/.venv/bin/pip.exe install --upgrade vimlib`
* `cd ~/vimfiles && poetry install vimlib`
<!--
*
``` sh
cd ~/vimfiles \
&& python3 -m venv .venv \
&& ~/vimfiles/.venv/bin/pip.exe install --upgrade vimlib
```
-->

# Usage

```python
from pyvim import current


# String with the current, or last, selection.
# Support basic, linewise, and block visual highlights
selection = pyvim.current.selection

# Boolean. Check if a highlight group is available
has_highlight = 'MyHighlightGroup' in pyvim.current.highlights
```

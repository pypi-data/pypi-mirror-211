# Scikit-HEP repo-review

[![Actions Status][actions-badge]][actions-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)

This tool can check the style of a repository. Use like this:

```bash
pipx run 'scikit-hep-repo-review[cli]' <path to repository>
```

This will produce a list of results - green checkmarks mean this rule is
followed, red x’s mean the rule is not. A yellow warning sign means that the
check was skipped because a previous required check failed. Some checks will
fail, that’s okay - the goal is bring all possible issues to your attention,
not to force compliance with arbitrary checks. Eventually there might be a way
to mark checks as ignored.

For example, `GH101` expects all your action files to have a nice `name:`
field. If you are happy with the file-based names you see in CI, you should
feel free to simply ignore this check (just visually ignore it for the moment,
a way to specify ignored checks will likely be added eventually).

All checks are mentioned at least in some way in the [Scikit-HEP Developer
Guidelines][]. You should read that first - if you are not attempting to follow
them, some of the checks might not work. For example, the guidelines specify
pytest configuration be placed in `pyproject.toml`. If you place it somewhere
else, then all the pytest checks will be skipped.

You are not required to be in Scikit-HEP to find this useful, however -
examples of repositories that at least partially follow the guidelines include
`pypa/cibuildwheel`, `pypa/build`, and `pybind/pybind11`.

### Development

This repository is intended to be fun to develop - it requires and uses Python
3.10, and uses a lot of the new features in 3.9 and 3.10. It's maybe not
entirely conventional, but it's fun.

There are a few key designs that are very useful and make this possible. First,
all paths are handled as Traversables. This allows a simple Traversable
implementation based on `open_url` to provide a web interface for use in the
webapp. It also would allow `zipfile.Path` to work just as well, too - no need
to extract.

Checks can request fixtures (like pytest) as arguments. Check files can add new
fixtures as needed. Fixtures are are specified with entry points, and take any
other fixture as arguments as well - the `package` fixture represents the root
of the package you are checking, and is the basis for all other fixtures.
Checks are specified via an entrypoint that returns a dict of checks; this also
can accept fixtures, allowing dynamic check listings.

Check files do not depend on the main library, and can be extended (similar to
Flake8). You register new check files via entry-points - so extending this is
with custom checks or custom fixtures is easy and trivial. There's no need to
subclass or do anything with the base library - no dependency required.

Checks are as simple as possible so they are easy to write. A check is a class
with the name (1-2 letters + number) and a docstring (the check message). It
should define a set of `requires` with any checks it depends on (by name), and
have a check classmethod. The docstring of this method is the failure message,
and supports substitution. Arguments to this method are fixtures, and `package`
is the built-in one providing the package directory as a Traversable. Any other
fixtures are available by name. A new fixture is given the package Traversable,
and can produce anything; fixtures are topologically sorted, pre-computed and
cached.

The runner will topologically sort the checks, and checks that do not run will
get a `None` result and the check method will not run. The front-end (Rich
powered CLI or Pyodide webapp) will render the markdown-formatted check
docstring only if the result is `False`.

# Links

This project inspired [Try-PyHF](https://kratsg.github.io/try-pyhf/), an
interface for a High Energy Physics package in Scikit-HEP.

This project inspired [abSENSE](https://princetonuniversity.github.io/abSENSE/), an
web interface to abSENSE.

[actions-badge]: https://github.com/scikit-hep/repo-review/workflows/CI/badge.svg
[actions-link]: https://github.com/scikit-hep/repo-review/actions
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]: https://github.com/psf/black
[pypi-link]: https://pypi.org/project/scikit-hep-repo-review/
[pypi-platforms]: https://img.shields.io/pypi/pyversions/scikit-hep-repo-review
[pypi-version]: https://badge.fury.io/py/scikit-hep-repo-review.svg
[sk-badge]: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
[scikit-hep developer guidelines]: https://scikit-hep.org/developer

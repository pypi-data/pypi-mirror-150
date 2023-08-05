![Parscival](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/docs/_static/logo.png)

## Description

Parscival is a data parsing and transformation tool. Even though it can potentially
interpret any input format and subsequently produce any output format, it was originally
designed to process PubMed ``.nbib`` files and export them to the CorText Graph format.

Data parsing and transforming is performed according to an experimental specification
described in a YAML file. For an example see [here](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/src/parscival_specs/pubmed-nbib.yaml).

The output parsed data is saved by default using the
[HDF5](https://www.hdfgroup.org/solutions/hdf5/) binary data format. HDF5
is an open source file format that supports large, complex, heterogeneous data.
It is designed for fast I/O processing and storage.

To enable parallel (on-the-fly) access to the HDF5 data produced, Parscival
uses [klepto](https://github.com/uqfoundation/klepto), a python library that
provides fast and flexible access to large amounts of storage.

In order to define how to transform the parsed data into an arbitrary output
format, Parscival implements a lightweight plugin architecture. For example, by using
the [render-template](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/src/parscival_plugins/transform/render_template.py) plugin, the output
result can be simple described as a [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
template. For an example on how to transform the parsed data into ``json``
see [here](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/src/parscival_specs/cortext.json.tpl).

## Install

```console
pip install parscival
```

## Usage

```console
usage: parscival [-h] [--version] [-v] [-vv] FILE_PARSER_SPEC FILE_OUTPUT FILE_DATASET [FILE_DATASET ...]

A modular framework for parsing, mapping and transforming data

positional arguments:
  FILE_PARSER_SPEC     parser specification
  FILE_OUTPUT          parsed data output
  FILE_DATASET         input dataset

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  -v, --verbose        set loglevel to INFO
  -vv, --very-verbose  set loglevel to DEBUG
```

### Examples

```console
# converts documents from pesticides-s.nbib into pesticides.cortext.json as described by pubmed-nbib.yaml
parscival -v src/parscival_specs/pubmed-nbib.yaml /tmp/pesticides.cortext.json tests/datasets/pesticides-s.nbib

# converts documents from both pesticides-s.nbib and hetercat-s.nbib into pesticides.db as described by pubmed-nbib.yaml
parscival -v src/parscival_specs/pubmed-nbib.yaml /tmp/pesticides.cortext.db tests/datasets/pesticides-s.nbib tests/datasets/hetercat-s.nbib
```

## Supported formats

### Input

- ``PubMed nbib``: PubMed is a free search engine accessing primarily the MEDLINE
database of references and abstracts on life sciences and biomedical topics. The
parsing spec is avalaible [here](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/src/parscival_specs/pubmed-nbib.yaml). You can find a more
detailed description in the related [documentation](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/docs/formats/nbib.md).

### Parsing

The intermediate parsing data is stored usign the CorText Graph format:

| Field       | Value                                | Type             | Description              |
| ----------- | ------------------------------------ | ---------------- | ------------------------ |
| `file`      | `sourceFile(fieldName)`              | `text`           | source file for the data |
| `id`        | `fieldName.doc[0,n-1]`               | `integer`        | ID of each document      |
| `rank`      | `fieldName.doc[id][0,m-1]`           | `integer`        | field cardinal index     |
| `parserank` | `fieldName.doc[id][rank][0,p-1]`     | `integer`        | parsed cardinal index    |
| `data`      | `fieldName.doc[id][rank][parserank]` | `[text,integer]` | parsed data              |

### Output

- ``cortext.json``: Parsed data is converted to ``json`` using the [cortext.json template](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/src/parscival_specs/cortext.json.tpl) 

- ``cortext.sqlite``: Parsed data is converted to a ``sqlite`` script using
the [cortext.sqlite template](https://gitlab.com/cortext/cortext-methods/parscival/-/raw/master/src/parscival_specs/cortext.sqlite.tpl). If requested by the
parsing spec, the resulting ``sqlite`` script can be intepreted and thus converted
to a binary database.

## Requirements

Parscival has been set up using PyScaffold, a project generator for
bootstrapping high-quality Python packages. For details and usage information
on PyScaffold see <https://pyscaffold.org>.

This project uses PyScaffold in combination with Tox, a generic virtualenv management
and test command line tool acting as frontend to Continuous Integration servers.
A list with all the available tasks is obtained via the ``tox -av`` command.

To prepare your environment you will need to install the following dependencies:

```console
pip install -U pip setuptools
pip install -U tox
```

## Deployment

```console
virtualenv .venv
source .venv/bin/activate
# ... edit setup.cfg to add dependencies ...
pip install -e .
tox

# to compile docs
tox -e docs

# to build distribution
tox -e build
```

## Credits

Parscival is being developed by the [CorTexT Platform](https://www.cortext.net) and
[Cogniteva SAS](https://cogniteva.com).

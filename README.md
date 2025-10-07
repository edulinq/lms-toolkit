# LMS Tools

A suite of tools and Python interface for different
[Learning Management Systems (LMSs)](https://en.wikipedia.org/wiki/Learning_management_system).

This project is not affiliated with any LMS developer/provider.

Documentation Table of Contents:
 - [Installation](#installation)
 - [CLI Configuration](#cli-configuration)
 - [Usage Notes](#usage-notes)
    - [Name Resolution and Labels](#name-resolution-and-labels)
    - [Output Formats](#output-formats)
 - [CLI Tools](#cli-tools)
      - [List Course Users](#list-course-users)
      - [Get Course Users](#get-course-users)
      - [List Assignments](#list-assignments)
      - [Get Assignments](#get-assignments)

## Installation

The project (tools and API) can be installed from PyPi with:
```
pip install edq-lms-toolkit
```

Standard Python requirements are listed in `pyproject.toml`.
The project and Python dependencies can be installed from source with:
```
pip3 install .
```

### Cloning

This repository includes submodules.
To fetch these submodules on clone, add the `--recurse-submodules` flag.
For example:
```sh
git clone --recurse-submodules git@github.com:edulinq/lms-toolkit.git
```

To fetch the submodules after cloning, you can use:
```sh
git submodule update --init --recursive
```

## Usage Notes

### Name Resolution and Labels

The LMS Toolkit is able to resolve most objects that have a name,
so you can refer to that object by name instead of by ID.
Fields with this resolution will be referred to as "queries".
The exact attributes that can be used as a query depend on the underlying object,
for example users can use their name or email in a user query.

A "label" is a formatted field that the LMS Toolkit will use in certain cases that includes both the name and id in a single field:
"name (id)".

For example, a user may be identified by any of the following:

| Query Type    | Query                          |
|---------------|--------------------------------|
| Email         | `sslug@test.edulinq.org`       |
| Name          | `Sammy Slug`                   |
| ID            | `123`                          |
| Label (Email) | `sslug@test.edulinq.org (123)` |
| Label (Name)  | `Sammy Slug (123)`             |

### Output Formats

Many commands can output data in three different formats:
 - Text (`--format text`) -- A human-readable format (usually the default).
 - Table (`--format table`) -- A tab-separated table.
 - JSON (`--format json`) -- A [JSON](https://en.wikipedia.org/wiki/JSON) object/list.

## CLI Tools

All CLI tools can be invoked with `-h` / `--help` to see the full usage and all options.

### List Course Users

Course users can be listed using the `lms.cli.courses.users.list` tool.
For example:
```
python3 -m lms.cli.courses.users.list
```

#### Get Course Users

To fetch information about course users, use the `lms.cli.courses.users.get` tool.
For example:
```
python3 -m lms.cli.courses.users.get sslug@test.edulinq.org
```

Any number of user queries may be specified.

#### List Assignments

Course assignments can be listed using the `lms.cli.courses.assignments.list` tool.
For example:
```
python3 -m lms.cli.courses.assignments.list
```

#### Get Assignments

To fetch information about course assignments, use the `lms.cli.courses.assignments.get` tool.
For example:
```
python3 -m lms.cli.courses.assignments.fetch 'Homework 1'
```

Any number of assignment queries may be specified.

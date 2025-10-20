# LMS Tools

A suite of tools and a Python interface for interacting with different
[Learning Management Systems (LMSs)](https://en.wikipedia.org/wiki/Learning_management_system).

This project is not affiliated with any LMS developer/provider.

Links:
 - [API Reference](https://edulinq.github.io/lms-toolkit)
 - [Development Notes](docs/development.md)
 - [Installation](#installation)
 - [CLI Configuration](#cli-configuration)
 - [Usage Notes](#usage-notes)
    - [Object Queries](#object-queries)
    - [Output Formats](#output-formats)
    - [Retrieval Operations](#retrieval-operations)
 - [CLI Tools](#cli-tools)
      - [List Course Users](#list-course-users)
      - [Get Course Users](#get-course-users)
      - [List Assignments](#list-assignments)
      - [Get Assignments](#get-assignments)
- [LMS Coverage](#lms-coverage)

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

### Object Queries

LMS's typically require that you refer to objects using their specified identifier.
Because this may be difficult,
the LMS Toolkit provides a way for users to instead refer to object by other identifying fields.
Fields with this behavior are referred to as "queries".
Unless specified, all inputs into the CLI can be assumed to be queries.

A query can be the LMS identifier, another identifying field, or a combination of the two (referred to as a "label").
The allowed identifying fields varies depending on the object you are referring to,
but is generally straightforward.
For example, a user can also be identified by their email or full name,
while an assignment can be identified by its full name.
Labels combine the identifying field with the LMS id,
and are most commonly used by the LMS Toolkit when outputting information.
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

### Retrieval Operations

When retrieving data from the LMS,
this project tends to use three different types of operations:
 - **list** -- List out all the available entries, e.g., list all the users in a course.
 - **fetch** -- Fetch one specific entry by identifier (not by query), e.g., fetch a specific user by id.
 - **get** -- Get a collection of entries by query, e.g., get several users by their email.

Fetch operations have the potential to be the fastest,
but are also the hardest to use (since you will need to know the LMS identifier for an object).
Fetch operations may not be exposed in the CLI.

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

## LMS Coverage

The LMS Toolkit is constantly expanding its support with hopes for supporting all major LMSs.

Legend:
 - `+` -- Supported
 - `-` -- Not Yet Supported
 - `x` -- Support Impossible (See Notes)

| Feature                                 | Canvas | Moodle |
|-----------------------------------------|--------|--------|
| lms.cli.courses.get                     | `+`    | `-`    |
| lms.cli.courses.list                    | `+`    | `-`    |
| lms.cli.courses.assignments.get         | `+`    | `-`    |
| lms.cli.courses.assignments.list        | `+`    | `-`    |
| lms.cli.courses.assignments.scores.get  | `+`    | `-`    |
| lms.cli.courses.assignments.scores.list | `+`    | `-`    |
| lms.cli.courses.users.get               | `+`    | `-`    |
| lms.cli.courses.users.list              | `+`    | `-`    |
| lms.cli.courses.users.scores.get        | `+`    | `-`    |
| lms.cli.courses.users.scores.list       | `+`    | `-`    |
| lms.cli.server.identify                 | `+`    | `+`    |

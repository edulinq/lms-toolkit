# LMS Tools

A suite of tools and a Python interface for interacting with different
[Learning Management Systems (LMSs)](https://en.wikipedia.org/wiki/Learning_management_system).

This project is not affiliated with any LMS developer/provider.

Links:
 - [API Reference](https://edulinq.github.io/lms-toolkit)
 - [Development Notes](docs/development.md)
 - [Installation](#installation)
 - [Usage Notes](#usage-notes)
   - [Authentication](#authentication)
   - [Object Queries](#object-queries)
   - [Output Formats](#output-formats)
   - [Retrieval Operations](#retrieval-operations)
   - [Groups vs Group Sets](#groups-vs-group-sets)
 - [CLI Tools](#cli-tools)
   - Courses
     - [Retrieve Courses](#retrieve-courses)
     - Assignments
       - [Retrieve Assignments](#retrieve-assignments)
       - Scores
         - [Retrieve Assignment Scores](#retrieve-assignment-scores)
         - [Upload Assignment Scores](#upload-assignment-scores)
     - Gradebook
       - [Retrieve Gradebook](#retrieve-gradebook)
       - [Upload Gradebook](#upload-gradebook)
     - Syllabus
       - [Retrieve Syllabus](#retrieve-syllabus)
     - User Groupings
       - Group Sets
         - [Retrieve Group Sets](#retrieve-group-sets)
         - [Create Group Sets](#create-group-sets)
         - [Delete Group Sets](#delete-group-sets)
         - Memberships
           - [Retrieve Group Set Memberships](#retrieve-group-set-memberships)
           - [Add Users to a Group Set](#add-users-to-a-group-set)
           - [Subtract Users from a Group Set](#subtract-users-from-a-group-set)
           - [Set Memberships for a Group Set](#set-memberships-for-a-group-set)
       - Groups
         - [Retrieve Groups](#retrieve-groups)
         - [Create Groups](#create-groups)
         - [Delete Groups](#delete-groups)
         - Memberships
           - [Retrieve Group Memberships](#retrieve-group-memberships)
           - [Add Users to a Group](#add-users-to-a-group)
           - [Subtract Users from a Group](#subtract-users-from-a-group)
           - [Set Users for a Group](#set-users-for-a-group)
     - Users
       - [Retrieve Users](#retrieve-users)
       - Scores
         - [Retrieve User Scores](#retrieve-user-scores)
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

### Authentication

Different LMSs may require different information for authentication.
The below table lists what each LMS needs.
Note that values only need to be provided once (in the config or CLI).

| LMS        | Config Keys                  | CLI Options                      |
|------------|------------------------------|----------------------------------|
| Blackboard | `auth_user`, `auth_password` | `--auth-user`, `--auth-password` |
| Canvas     | `token`                      | `--token`                        |

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
this project tends to use two different types of operations:
 - **list** -- List out all the available entries, e.g., list all the users in a course.
 - **get** -- Get a collection of entries by query, e.g., get several users by their email.

### Groups vs Group Sets

When dealing with groups, there are two structures you need to be familiar with: Groups and Group Sets.
A group is a collection of students.
A group set (sometimes denoted as "groupset") is a collection of groups, often created for a single purpose
(e.g., a set of groups created for a specific assignment).
All groups must exist within a group set.

### TSV Files

Various operations may require [TSV files](https://en.wikipedia.org/wiki/Tab-separated_values) (tab-separated) files as input.
When used, they are usually paired with a `--skip-rows` option to allow you to skip the desired number of header rows
(the default value is generally 0).
Empty lines are ignored, and will not be counted against the `--skip-rows` count.

## CLI Tools

All CLI tools can be invoked with `-h` / `--help` to see the full usage and all options.

Examples listed here will assume that your authentication information is already defined in your global config file
(use `--help` for more information on that).

Examples listed here are not exhaustive in terms of the available tools or the full functionality of each comment.

The data used in these examples are part of the official test data used for this repo (and other LMS test images).

### Retrieve Courses

List all courses associated with a user with `lms.cli.courses.list`:
```sh
python3 -m lms.cli.courses.list
```

You can get a single course with `lms.cli.courses.get`:
```sh
python3 -m lms.cli.courses.get 'Course 101'
```

### Retrieve Assignments

List all assignments associated with a course with `lms.cli.assignments.list`:
```sh
python3 -m lms.cli.assignments.list --course 'Course 101'
```

You can get a single assignment with `lms.cli.assignments.get`:
```sh
python3 -m lms.cli.assignments.get --course 'Course 101' 'Homework 0'
```

### Retrieve Assignment Scores

List all student scores for an assignment with `lms.cli.assignments.scores.list`:
```sh
python3 -m lms.cli.assignments.scores.list --course 'Course 101' --assignment 'Homework 0'
```

The `table` format is especially useful for listing scores:
```sh
python3 -m lms.cli.assignments.scores.list --course 'Course 101' --assignment 'Homework 0' --format table
```

### Upload Assignment Scores

Upload a single score for an assignment and user with `lms.cli.assignments.scores.upload-score`.
For example, to upload a score of `1.0` for user `course-student` and assignment `Homework 0', use:
```sh
python3 -m lms.cli.assignments.scores.upload-score --course 'Course 101' --assignment 'Homework 0' --user 'course-student' 1.0
```

To upload multiple scores for a single assignment, use `lms.cli.assignments.scores.upload`.
This tool takes a TSV file as input.
Each data row can have two or three columns (different rows can have different number of columns).
The values are as follows:
 1) User Query
 2) Numeric Score
 3) (**Optional**) Comment

For example, assume we have a file `scores.txt` with the following contents:
```
User	Score	Comment
extra-course-student-1@test.edulinq.org	1
extra-course-student-2@test.edulinq.org	1.5
extra-course-student-3@test.edulinq.org	2	foo
extra-course-student-4@test.edulinq.org	2.5	foo
```

We can upload these scores for `Assignment 1` in the course `Extra Course` using:
```sh
python3 -m lms.cli.assignments.scores.upload --course 'Extra Course' --assignment 'Assignment 1' scores.txt
```

### Retrieve Gradebook

List all gradebook entries associated with a course with `lms.cli.courses.gradebook.list`:
```sh
python3 -m lms.cli.courses.gradebook.list --course 'Course 101'
```

Gradebooks are always output as TSV tables.

### Upload Gradebook

Upload a gradebook with `lms.cli.courses.gradebook.upload`.
The gradebook file must be the same format that is outputted by `lms.cli.courses.gradebook.list`.

For example, assume we have a file `gradebook.txt` with the following contents:
```
User	Assignment 1 (130000100)	Assignment 2 (130000200)
extra-course-student-1@test.edulinq.org (100060000)	1.0	1.0
extra-course-student-2@test.edulinq.org (100070000)		0.5
```

We can upload these three scores to course `Extra Course` with:
```sh
python3 -m lms.cli.courses.gradebook.upload --course 'Extra Course' gradebook.txt
```

A gradebook does not need to represent all assignments or students in a course.
Only the assignments and students of interest need to be included.
An empty cell (missing score) will be ignored,
but all rows must have the correct number of cells (tabs).

### Retrieve Syllabus

Get a course's syllabus with `lms.cli.courses.syllabus.get`:
```sh
python3 -m lms.cli.courses.syllabus.get --course 'Course 101'
```

If a course has no syllbus, a message like the following will be output:
```
<No syllabus found for course: 'Course 101'.>
```

### Retrieve Group Sets

List all groups sets in a course `lms.cli.courses.groupsets.list`:
```sh
python3 -m lms.cli.courses.groupsets.list --course 'Extra Course'
```

### Create Group Sets

Create a new group set with: `lms.cli.courses.groupsets.create`:
```sh
python3 -m lms.cli.courses.groupsets.create --course 'Extra Course' 'My New Group Set'
```

### Delete Group Sets

Delete group sets with: `lms.cli.courses.groupsets.delete`:
```sh
python3 -m lms.cli.courses.groupsets.delete --course 'Extra Course' --groupset 'Group Set 1'
```

### Retrieve Group Set Memberships

List all memberships in a group set with: `lms.cli.courses.groupsets.memberships.list`:
```sh
python3 -m lms.cli.courses.groupsets.memberships.list --course 'Extra Course' --groupset 'Group Set 1'
```

### Add Users to a Group Set

Add users to a group set with: `lms.cli.courses.groupsets.memberships.add`.
This tool takes a TSV file as input.
Each data row must have two columns: group query and user query.
If a group does not exist, it will be created.

For example, assume we have a file `groupset-members.txt` with the following contents:
```
Group	User
My New Group 1	extra-course-student-1@test.edulinq.org
My New Group 1	extra-course-student-2@test.edulinq.org
My New Group 2	extra-course-student-3@test.edulinq.org
My New Group 2	extra-course-student-4@test.edulinq.org
```

We can add these user to the specified groups using:
```sh
python3 -m lms.cli.courses.groupsets.memberships.add --course 'Extra Course' --groupset 'Group Set 3' groupset-members.txt
```

### Subtract Users from a Group Set

Add users to a group set with: `lms.cli.courses.groupsets.memberships.subtract`.
This tool takes a TSV file as input.
Each data row must have two columns: group query and user query.

For example, assume we have a file `groupset-members.txt` with the following contents:
```
Group	User
Group 1-1	extra-course-student-1@test.edulinq.org
Group 1-2	extra-course-student-3@test.edulinq.org
```

We can subtract these users from the specified groups using:
```sh
python3 -m lms.cli.courses.groupsets.memberships.subtract --course 'Extra Course' --groupset 'Group Set 1' groupset-members.txt
```

### Set Memberships for a Group Set

Set the memberships for an entire group set with: `lms.cli.courses.groupsets.memberships.set`.
This tool takes a TSV file as input.
Each data row must have two columns: group query and user query.
The group set will be modfied to match your file exactly.
This may involve creating or deleting groups.

For example, assume we have a file `groupset-members.txt` with the following contents:
```
Group	User
New Group 1	extra-course-student-1@test.edulinq.org
New Group 2	extra-course-student-2@test.edulinq.org
New Group 3	extra-course-student-3@test.edulinq.org
New Group 4	extra-course-student-4@test.edulinq.org
```

We can use this file to set the group set memberships with:
```sh
python3 -m lms.cli.courses.groupsets.memberships.set --course 'Extra Course' --groupset 'Group Set 1' groupset-members.txt
```

This command will do several things in this case:
 - Create new groups.
 - Remove users from their current groups.
 - Add users to their new groups.
 - Delete old (now empty) groups.

### Retrieve Groups

List all the groups for a group set with `lms.cli.courses.groups.list`:
```sh
python3 -m lms.cli.courses.groups.list --course 'Extra Course' --groupset 'Group Set 1'
```

### Create Groups

Create a new group with: `lms.cli.courses.groups.create`:
```sh
python3 -m lms.cli.courses.groups.create --course 'Extra Course' --groupset 'Group Set 1' 'My New Group'
```

### Delete Groups

Delete groups with: `lms.cli.courses.groups.delete`:
```sh
python3 -m lms.cli.courses.groups.delete --course 'Extra Course' --groupset 'Group Set 1' --group 'Group 1-1'
```

### Retrieve Group Memberships

List all memberships in a group with: `lms.cli.courses.groups.memberships.list`:
```sh
python3 -m lms.cli.courses.groups.memberships.list --course 'Extra Course' --groupset 'Group Set 1' --group 'Group 1-1'
```

### Add Users to a Group

Add users to a group with: `lms.cli.courses.groups.memberships.add`:
```sh
python3 -m lms.cli.courses.groups.memberships.add --course 'Extra Course' --groupset 'Group Set 3' --group 'Group 3-1' extra-course-student-1
```

You can specify as many users as you want.

### Subtract Users from a Group

Subtract users from a group with: `lms.cli.courses.groups.memberships.subtract`:
```sh
python3 -m lms.cli.courses.groups.memberships.subtract --course 'Extra Course' --groupset 'Group Set 1' --group 'Group 1-1' extra-course-student-1
```

You can specify as many users as you want.

### Set Users for a Group

Set the users in a group with: `lms.cli.courses.groups.memberships.set`:
```sh
python3 -m lms.cli.courses.groups.memberships.set --course 'Extra Course' --groupset 'Group Set 1' --group 'Group 1-1' extra-course-student-2 extra-course-student-3
```

This operation will add and subtract any users necessary to make the group have exactly the users specified.

### Retrieve Users

List all users associated with a course with `lms.cli.users.list`:
```sh
python3 -m lms.cli.users.list --course 'Course 101'
```

You can get a single user with `lms.cli.users.get`:
```sh
python3 -m lms.cli.users.get --course 'Course 101' 'course-student'
```

### Retrieve User Scores

List all scores for a student with `lms.cli.users.scores.list`:
```sh
python3 -m lms.cli.users.scores.list --course 'Extra Course' --user 'extra-course-student-1'
```

The `table` format is especially useful for listing scores:
```sh
python3 -m lms.cli.users.scores.list --course 'Extra Course' --user 'extra-course-student-1' --format table
```

## LMS Coverage

The LMS Toolkit is constantly expanding its support with hopes for supporting all major LMSs.

Legend:
 - `+` -- Supported
 - `-` -- Not Yet Supported
 - `x` -- Support Impossible (See Notes)

| Tool                                            | Blackboard | Canvas | Moodle |
|-------------------------------------------------|------------|--------|--------|
| lms.cli.courses.get                             | `+`        | `+`    | `-`    |
| lms.cli.courses.list                            | `+`        | `+`    | `-`    |
| lms.cli.courses.assignments.get                 | `-`        | `+`    | `-`    |
| lms.cli.courses.assignments.list                | `-`        | `+`    | `-`    |
| lms.cli.courses.assignments.scores.get          | `-`        | `+`    | `-`    |
| lms.cli.courses.assignments.scores.list         | `-`        | `+`    | `-`    |
| lms.cli.courses.assignments.scores.upload       | `-`        | `+`    | `-`    |
| lms.cli.courses.assignments.scores.upload-score | `-`        | `+`    | `-`    |
| lms.cli.courses.gradebook.get                   | `-`        | `+`    | `-`    |
| lms.cli.courses.gradebook.list                  | `-`        | `+`    | `-`    |
| lms.cli.courses.gradebook.upload                | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.create                   | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.delete                   | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.get                      | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.list                     | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.memberships.add          | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.memberships.list         | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.memberships.set          | `-`        | `+`    | `-`    |
| lms.cli.courses.groups.memberships.subtract     | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.create                | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.delete                | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.get                   | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.list                  | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.memberships.add       | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.memberships.list      | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.memberships.set       | `-`        | `+`    | `-`    |
| lms.cli.courses.groupsets.memberships.subtract  | `-`        | `+`    | `-`    |
| lms.cli.courses.syllabus.get                    | `-`        | `+`    | `-`    |
| lms.cli.courses.users.get                       | `+`        | `+`    | `-`    |
| lms.cli.courses.users.list                      | `+`        | `+`    | `-`    |
| lms.cli.courses.users.scores.get                | `-`        | `+`    | `-`    |
| lms.cli.courses.users.scores.list               | `-`        | `+`    | `-`    |
| lms.cli.server.identify                         | `+`        | `+`    | `+`    |

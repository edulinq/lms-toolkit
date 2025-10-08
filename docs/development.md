# Development Notes

This document contains notes for developers.

## Test Data

The majority of the data needed for testing takes the form of
[HTTP Exchanges](https://github.com/edulinq/python-utils/blob/main/edq/util/net.py) from LMS servers.
These test exchanges are generally provided by repos that specialize in creating a Docker image for a specific LMS and loading it with data.
For example, the [lms-docker-canvas-testdata repo](https://github.com/edulinq/lms-docker-canvas-testdata)
creates a Docker image with a running Canvas instance loaded with standardized test data.
These repos are included in the [testdata](../testdata) directory as submodules.
Therefore, each backend should have a full set of test HTTP Exchanges
(verified against a real LMS server instance).

### Generating Test Data

Generating new test data (HTTP exchanges) is a simple, but multi-stage process.
(Note that there are various possible processes for generating test data,
the procedure listed here is just one example.)

**Step 0: Develop the Backend/API Code**

Generating test data is much simpler if you can leverage the rest of the LMS Toolkit.
Therefore, a good starting point is to implement the code that calls the backend and the CLI interface to call that code.
It's fine if the code is not 100% implemented right away, it can be just enough for you to start with.

**Step 1: Manually Start your LMS Backend**

Start your LMS backend instance.
This is typically the standard LMS testdata Docker image
(like [lms-docker-canvas-testdata repo](https://github.com/edulinq/lms-docker-canvas-testdata)),
but can be whatever you choose.

For example:
```sh
docker run --rm -it -p 3000:3000 --name canvas ghcr.io/edulinq/lms-docker-canvas-testdata
```

**Step 2: Run your LMS Toolkit Command against your LMS Server**

Use the `--server` and (possibly) `--server-type` options to run your commands against your newly-started server.
Additionally, use the `--http-exchanges-out-dir` options to write out your HTTP exchanges.

For example, you can write out test data to a `test` directory with:
```sh
python -m lms.cli.courses.users.list \
    --http-exchanges-out-dir test \
    --config-file testdata/lms-docker-canvas-testdata/testdata/edq-lms.json
```

Note that the LMS testdata repos should also provide a config file (`edq-lms.json`) for easily connecting to the test server.

**Step 3: Inspect you Data**

Look at your data and make sure everything looks fine.

**Step 4: Finish Development**

Once you have your test data, you can finish developing any code and/or tests.

**Step 5: Push Data to the LMS Test Data Repo**

Add your test data to the test data repo.

You can do this manually, or by using local installations of your `lms-tooklit` package and running the
data generating script in your LMS test data repo.

Once the data is there, run the verification script in your LMS test data repo and push the change.

This will probably also involve a PR to get your changes in.

**Step 6: Update the Submodule and Push Your Changes**

Now that the test data lives in the appropriate repo, you can pull those changes in this repo's submodule.
You can now push the updated submodule along with all your changes.

If you are making a PR, you should include a link to your data changes along with your code changes to this repo.

### Verifying Test Data

HTTP exchanges can be programmatically verified using a few recommended methods:

#### edq.cli.http.verify-exchanges

The [EduLinq Python Utils](https://github.com/edulinq/python-utils)
creates the definition for HTTP exchanges,
and provides tooling for them.
The provided `edq.cli.http.verify-exchanges` CLI allows you to verify an exchange against an arbitrary server
(which must already be running).

For example:
```sh
python3 -m edq.cli.http.verify-exchanges 127.0.0.1:3000 testdata/lms-docker-canvas-testdata/testdata/http
```

This is the most basic verification method (since it does not know anything about LMSs or restarting servers),
but is quick and easy.

#### lms.cli.lib.verify-test-data

The `lms.cli.lib.verify-test-data` CLI is a more powerful method that is specifically built for this project.
It understands starting and stopping servers, and different configurations.

For example:
```sh
python3 -m lms.cli.lib.verify-test-data \
    --server-stop-command 'docker kill canvas' \
    --config-file testdata/lms-docker-canvas-testdata/testdata/edq-lms.json \
    'docker run --rm -p 3000:3000 --name canvas lms-docker-canvas-base-testdata' \
    testdata/lms-docker-canvas-testdata/testdata/http
```

Take careful note of the quotations in this command.
Part of this command is giving information about how to start (`docker run ...`) and stop (`docker kill ...`) the LMS server.
Note that you can still use the pre-provided config files for information on how to connect to the server.

#### LMS Image Specific Scripts

The LMS test data images should provide their own scripts for verifying their respective tests data.
These are usually build upon `lms.cli.lib.verify-test-data`, but with all the settings already defaulted for that LMS/repo.
For example, the [lms-docker-canvas-testdata has one](https://github.com/edulinq/lms-docker-canvas-testdata/blob/main/scripts/verify-test-data.py).

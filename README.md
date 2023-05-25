# tap-circle-ci

`tap-circle-ci` is a Singer tap for [CircleCI][circleci].

Built with the [Meltano Tap SDK][sdk] for Singer Taps.

## Streams
  - [Pipelines](https://circleci.com/docs/api/v2/#operation/listPipelines)
  - [Workflows](https://circleci.com/docs/api/v2/#operation/listWorkflowsByPipelineId)
  - [Jobs](https://circleci.com/docs/api/v2/#operation/listWorkflowJobs)

WARNING: You must follow the projects in CircleCI to obtain their pipelines.

## Installation

You can install this repository directly from the Github repo. For example, by running:

```bash
pipx install https://github.com/MeltanoLabs/tap-circle-ci.git
```

## Configuration

### Accepted Config Options

The following configuration options are available:

| Field         | Description                                                                             | Type           | Required | Default                                                  |
|---------------|-----------------------------------------------------------------------------------------|----------------|----------|----------------------------------------------------------|
| `token`       | Personal API Token you have generated that can be used to access the CircleCI API       | `string`       | yes      |                                                          |
| `org_slug`    | Organization slug in the form vcs-slug/org-name. Example: `org-slug=gh/CircleCI-Public` | `string`       | yes      |                                                          |
| `user_agent`  | User-Agent to make requests with                                                        | `string`       | no       | `tap-circle-ci/<version> Singer Tap for the CircleCI API` |
| `base_url`    | Base URL for the CircleCI API                                                           | `string`       | no       | `https://circleci.com/api/v2`                            |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-circle-ci --about
```

### Source Authentication and Authorization

Login to your Circle CI account, go to the [Personal API Tokens](https://circleci.com/account/api) page,
and generate a new token.

## Usage

You can easily run `tap-circle-ci` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-circle-ci --version
tap-circle-ci --help
tap-circle-ci --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_circle_ci/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-circle-ci` CLI interface directly using `poetry run`:

```bash
poetry run tap-circle-ci --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-circle-ci
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-circle-ci --version
# OR run a test `elt` pipeline:
meltano elt tap-circle-ci target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

[circleci]: https://app.circleci.com/
[sdk]: https://sdk.meltano.com
[apidocs]: https://circleci.com/docs/2.0/api-developers-guide/
[meltano]: https://www.meltano.com

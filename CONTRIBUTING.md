# Contribution Guidelines

Thanks for your interest in contributing to `app-simulator`! This document
contains guidelines for how to contribute and some suggestions what you can
contribute to the project.

## How to Contribute

Here are a few general guidelines on contributing and reporting bugs that we ask
you to review. Following these guidelines helps to communicate that you respect
the time of the contributors managing and developing this open source project.
In return, they should reciprocate that respect in addressing your issue,
assessing changes, and helping you finalize your pull requests. In that spirit
of mutual respect, we endeavor to review incoming issues and pull requests
within 10 days, and will close any lingering issues or pull requests after 60
days of inactivity.

Please note that all of your interactions in the project are subject to our
[Code of Conduct](/CODE_OF_CONDUCT.md). This includes creation of issues or pull
requests, commenting on issues or pull requests, and extends to all interactions
in any real-time space e.g., Slack, Discord, etc.

### Reporting Issues

Before reporting a new issue, please ensure that the issue was not already
reported or fixed by searching through our
[issues list](https://github.com/cisco-open/app-simulator/issues).

When creating a new issue, please be sure to include a **title and clear
description**, as much relevant information as possible, and, if possible, a
test case.

**If you discover a security bug, please do not report it through GitHub.
Instead, please see security procedures in [SECURITY.md](/SECURITY.md).**

### Sending Pull Requests

Before sending a new pull request, take a look at existing pull requests and
issues to see if the proposed change or fix has been discussed in the past, or
if the change was already implemented but not yet released.

We expect new pull requests to include tests for any affected behavior, and, as
we follow semantic versioning, we may reserve breaking changes until the next
major version release.

### Other Ways to Contribute

We welcome anyone that wants to contribute to `app-simulator` to triage and
reply to open issues to help troubleshoot and fix existing bugs. Here is what
you can do:

- Help ensure that existing issues follows the recommendations from the
  _[Reporting Issues](#reporting-issues)_ section, providing feedback to the
  issue's author on what might be missing.
- Review existing pull requests, and testing patches against real existing
  applications that use `app-simulator`.
- Write a test, or add a missing test case to an existing test.

Thanks again for your interest on contributing to `app-simulator`!

:heart:

## Where we need help

If you have an idea already, what you want to contribute, great! Please review
the guidelines above and get started. If you are looking for ideas, what you
could contribute, you find a set of suggestions from the maintainers, where help
is needed.

### Add documentation

A good way to get started with a project and contributing to it at the same
time, is reading the documentation and suggesting changes to the project while
doing so!

Additionally, you may have your own use cases in mind for using application
simulator, and we are happy to see if we can add it to the
[tutorials](./docs/tutorial/).

### Add tests

Since this project is a port of the existing project
[APM Game](https://github.com/appdynamics/apm-game), some components lack proper
test coverage. This is also a great way to get involved with the project!

### Modernize components

The components ported from APM Game are using some outdated technology, so a
good way to contribute is modernizing them.

### Write specification

The [specification](./docs/specification/) is work in progress. You can help to
make it better!

### Add components

If you want to have a service, database or loader using your preferred
programming language or technology, we are happy to accept a pull request (PR)
for them. You can use the [specification](./docs/specification/README.md) or
existing components ([services](./src/services/), [databases](./src/databases/),
[loaders](./src/loaders/)) as implementation reference. If you'd like to add a
new service, we recommend that you start with the support of HTTP calls to other
endpoints, such that your service can be added into a simulation easily.

Furthermore, if you'd like to add a new component type (like a message queue or
a cache), you can do tht as well! However, we recommend that you raise an issue
first and we discuss how such a component could be added.

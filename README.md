# Application Simulator

[![Contributor-Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-fbab2c.svg)](CODE_OF_CONDUCT.md)
[![License](https://img.shields.io/github/license/cisco-open/app-simulator?label=License)](LICENSE)
[![Maintainer](https://img.shields.io/badge/Maintainer-Cisco-00bceb.svg)](https://opensource.cisco.com)
[![Release](https://img.shields.io/github/v/release/cisco-open/app-simulator?label=Release)](https://github.com/cisco-open/app-simulator/releases)

Application Simulator allows you to rapidly create a set of interacting
services, databases and load generators to simulate application deployments of
any size and form.

Unlike other simulators or demo applications it is not focused around a specific
kind of application, like a blog, task list, web shop or banking app. Instead,
Application Simulator is driven by configuration files that define the behavior
of the components of your application.

This is especially useful for use cases, where you care less about the business
logic to be mimicked, but the interaction of the different components that make
up an application.

This includes the following use cases:

- Tailored demo environments for observability, e.g. instrumenting all services
  with OpenTelemetry and visualizing the data in your preferred backend.
- Complex simulated environments for in-cluster network experiments, e.g.
  testing out new features of cilium.

## Quick Start

You can use application simulator with your preferred container orchestration,
since all components are available as container images. We provide the best
experience for docker compose and kubernetes. Pick one of them for a quick
start!

- [kubernetes quick start](./docs/quick-start/kubernetes.md)
- [docker compose quick start](./docs/quick-start/docker-compose/README.md)

> [!NOTE]
>
> You can use the
> [container images](https://github.com/orgs/cisco-open/packages?repo_name=app-simulator)
> published as part of this project without the generators for kubernetes and
> docker compose. Both are convenience functions!
>
> If you only need a container image that simulates the behavior of an
> application, check out the
> [standalone container quick start](./docs/quick-start/standalone-container/README.md).

## Tutorial

After you have tried out application simulator with the quick start, you can
learn using it with the step by step tutorial:

1. [Two services](./docs/tutorial/1-two-services.md)
2. [A database and more services](./docs/tutorial/2-a-database-and-more-services.md)
3. [Errors and randomness](./docs/tutorial/3-errors-and-randomness.md)
4. [Observability with OpenTelemetry](./docs/tutorial/4-observability-with-opentelemetry.md)

## Configuration specification

Application simulator is driven by configuration files that allow you to
describe a microservice architecture and then run it with your preferred
container orchestration. The configuration file follows a
[specification](./docs/specification/README.md).

## Contribute

If you'd like to contribute to this project, check out our
[contribution guidelines](./CONTRIBUTING.md).

## Support

If you have any questions or concerns, get in touch with us by
[raising an issue](https://github.com/cisco-open/app-simulator/issues). If you
want to report a security issue, please follow our
[security policy](./SECURITY.md)

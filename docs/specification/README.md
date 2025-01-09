# Application Simulator Configuration Specification

The following document outlines the technical specification for the
configuration files used by different components of
[cisco-open/app-simulator](https://github.com/cisco-open/app-simulator).

## Components

There are two groups of components:

- **generators** are convenience functions that translate an application
  simulator configuration file for multiple containers into the format
  recognized by popular container orchestration engines, like Kubernetes or
  docker compose. An application simulator configuration file is for the most
  part independent of the orchestration engine, such that it is possible to
  reuse a configuration with different orchestration engines.
- **containers** are the building blocks of application simulator. They
  encapsulate **services**, **databases** and **loaders** which can be combined
  to represent a complex microservice architecture. Containers share some of
  their configuration, but they also have some domain-specific settings.

Component configurations MAY contain elements that are specific to one
orchestration engine. They are grouped in under a key that identified the
engine, i.e. `k8s` for Kubernetes and `dockerCompose` for docker compose.

## Generator configuration

The configuration file that can be read by a generator is called "application
simulator configuration file" (or short "app sim config"), since it represents
the top-level structure of a simulated microservice application.

A generator MUST support reading an app sim config in YAML format. A generator
MAY support other formats like JSON, TOML, etc.

The top level element of an app sim config file MUST be
[mapping](https://yaml.org/spec/1.2.2/#mapping) and MAY contain sections
represented by the following keys:

- **global**: the value node MUST either be empty, or a mapping that contains
  configurations that are either relevant for the generation process or applied
  to all **containers**.
- **services**: the value node MUST either be empty, or a mapping of
  **services** by their name.
- **databases**: the value node MUST either be empty, or a mapping of
  **databases** be their name.
- **loaders**: the value node MUST either be empty, or a mapping of **loaders**
  by their name.

The structure of the mappings for the different **container** components
(**services**, **databases**, **loaders**) are described below in the chatper
[Container configuration](#container-configuration).

The **global** configuration MAY have the following child nodes:

- **imageNamePrefix**:
- **imageNameSuffix**:
- **serviceDefaultPort**:

## Container configuration

### Common configuration

All **container** configurations share the following settings:

- **type** (required)
- **name**
- **exposedPort**
- **aliases**
- **enabled**

### Service configuration

- **endpoints**

### Call sequence configuration

- **call**
- **probability**
- **schedule**

Available **commands** for **call**:

- **sleep**
- **slow**
- **cache**
- **error**
- **log**

### Database configuration

- **databases**

### Loader configuration

- **wait**
- **sleep**
- **urls**

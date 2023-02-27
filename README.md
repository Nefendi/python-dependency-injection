# dependency-injection

This repository contains a collection of files showing what Dependency Injection
is and how to use it in Python with and without a special framework. The
framework used is
[dependency-injector](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html).
Another notable option is
[injector](https://injector.readthedocs.io/en/latest/), but the former looks
more mature and better maintained.

## Overview

The purpose of this project is not to describe Dependency Injection and
Inversion of Control patterns in a very detailed way. This is left to the reader
as homework (the documentation of the **dependency-injector** package is an
especially good website to visit). The project should be instead considered a
set of examples which can act as an extension of theory found in other sources.

## Structure

The project is organised into a few files and one package (`api`). The
recommended order of reading the source code is the following:

1. no_dependency_injection.py
2. dependency_injection.py
3. using_dependency_injector.py
4. api package

The whole project revolves around three classes, namely:

- `WebClient`, which pretends to make requests to an external service
- `UserService`, which uses `WebClient` in its method for registering a user
- `ManagementFacade`, which uses `UserService` and does something else on top of
  calling the function exposed by `UserService`

In the `no_dependency_injection.py`, a fragment of code without using the
Dependency Injection idea at all is presented. The design is not flexible at
all, every dependency is hardcoded, but constructing the `ManagementFacade`
object is simple.

In the `dependency_injection.py`, the same code is written with the Dependency
Injection pattern in mind. Every dependency must be passed as an argument to
each function and `__init__` initialisation method. Flexibility is gained, but
constructing the `ManagementFacade` objects is verbose and gets complicated even
though, there are not many parameters involved.

In the `using_dependency_injector.py`, the **dependency-injector** package is
used for the first time. Declaring a container is verbose, but every dependency
is kept in a single place and the dependencies from the IoC container are
automatically injected into functions and classes that need them. It is also
very easy to override any dependency in the chain with a different
implementation. This is especially useful when testing. In general, a completely
different container can be used to run an application in a test mode by
replacing every dependency making external calls with ones which simply do not
do that.

In the `api` package, every idea is presented once more, but the code better
resembles a real-world application with unit tests in place. Additionally, it is
shown how to achieve Dependency Injection with mechanisms built into the FastAPI
framework. It is a nice feature, but still, **dependency-injector** is more
powerful as it is not tied to FastAPI.

## Running the examples

The first three files are standalone, and you can pass the paths to them
directly to the `python3` (or `python`) command to obtain the results.

To run the FastAPI application, issue `uvicorn api.application:app` in the root
of the whole project (add the `--reload` flag if you would like Uvicorn to watch
for file changes and restart the server).

To run the tests, use the `pytest` command in the root of the project. You can
add the `-s` flag to let **Pytest** know that you want to see what is printed to
standard output while running the tests.

## Dependencies

The code was written using Python 3.10.6. All the needed dependencies are in the
`pyproject.toml` file. Simply run `poetry install --no-root` in a virtual
environment to download everything. If you are not currently using a virtual
environment, Poetry will create it automatically for you.

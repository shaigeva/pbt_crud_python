

<br/>
<br/>
<br/>

# NOTE - THIS IS WORK IN PROGRESS
The examples in the repo work, but there are some things missing:
- Documentation needs some improvements.
- Code cleanup is still necessary.
- Mostly - this repo is actually a companion to a blog post explaining this
  technique, and the blog post has not been published yet.



# Property-Based Testing a stateful web application.
This is an example of using Property-Based Testing to test a CRUD web 
application.

The example uses Stateful Testing (AKA model-based testing) to model the
correct behavior of the application and find (minimal) sequences of actions
that exponse functional bugs.

The testing code is implemented using the excellent Hypothesis Python library.

The server application (code under test) is a python Flask application (see
attributions at bottom of README)<br>
The client frontend is implemented in Vue.js (see attributions at bottom of
README).

# How to use this repo
To support gradual learning, this repo has 4 different versions of the code and
tests at, and each version contains different bugs and tests with different
levels of complexity.


To run the tests, you'll need to (there are exact instructions below - this is
so you understand the basic flow)
- Run the client application (also common to all versions). 
- Activate a python virtualenv (common to all
versions)
- Run the server for a specific version
- **Play
    with the application using the client and reproduce all bugs manually,
    to get a feeling for how PBT helps you**
- Run the tests for the same version
Each version has its own directory with its own README file that shows what
you can expect the test to show you, and explains the bug.

The version directories are prefixed with a number - start from 01 and move up.

The last version (correct_code) contains the same tests as the previous
version, but with the correct code.


# How to run
## Run the client frontend
Prerequisite: **have nvm installed**.

Start at repository root directory, and:

```sh
cd client
nvm use
npm install
npm run serve
```
Point your browser to http://localhost:8080

## Set up Python virtualenv
(start at repository root directory)

### Note for non-pythonists
A virtualenv is a python sandbox, where you can install packages in isolation
from the global python installation.<br>
To run the server and tests, you will create a virtualenv, and the scripts that run the server and the tests are aware of the virtualenv and will use it (you don't need to do this yourself).<br>
Pipenv is a helpful tool - a python package that helps manage virtualenvs.<br>

### Install Python, virtualenv and Pipenv
**Missing**

### Install python packages
(this also creates the virtualenv if needed)
```sh
./devtools/reinstall_pipenv_packages.sh
```

## Run the server
```sh
cd server_versions/server_01_incorrect_id
./devtools/run_app.sh
```
(or any of the other directories under `server_versions`)<br>

Note: the server serves on port 5001 (why? because there's a conflict with apple AirPlay)

## Run the tests
```sh
cd server_versions/server_01_incorrect_id
./devtools/run_tests.sh
```
(of course - `cd` into the same directory as you have for running the server)


# Attributions
The current client and server implementation has originally been copied from (and slightly modified):  https://github.com/testdrivenio/flask-vue-crud

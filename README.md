[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Unit tests](https://github.com/nicolasteodosio/popular-repo/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/nicolasteodosio/popular-repo/actions/workflows/unit-tests.yml)


### Installation ###
* [Install the docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)
* [Install docker-compose](https://docs.docker.com/compose/install/#install-compose)


### Env files ###
- Add you github access token to the `env.docker`

    
### Running the tests

- Move to the `app` directory
- Execute `chmod +x test.sh`
- To run the tests execute `./test.sh`
- Any commit at the master branch trigger a github action that run the unit tests


### Docs

- Since the application was built using `fastapi`, it comes with `OPENAPI` and `SWAGGER` docs
- With the server running go to `http://localhost:8083/docs`

### Comments ###
* The application was built with `fastapi` , mainly due to the speed of its implementation and the possibility of using the framework asynchronously*
* I choose to use redis to cache the response from the api, this improved the response time from around 500 milliseconds to about 15 milliseconds
* The application is using [pre-commit](https://pre-commit.com/) git hooks, with `black`, `flake8`, `isort`. So there is no need to worry about the code pattern during development
* The application also has a `CI` using github-actions.

### Backlog ###
* Would use [bandit](https://github.com/PyCQA/bandit) for security check
* Integrate the project with [Sentry](https://sentry.io/welcome/) for security check
* Add the project to a [SonarQube](https://www.sonarqube.org/) or [Codacy](https://www.codacy.com/), to track code smells, bugs etc.
* Make all the code works with async using asyncio and aiohttp and fastapi with async views to check if response would be better


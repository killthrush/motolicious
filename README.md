# motolicious
Repo for tinkering with moto and localstack.

Requirements:
* Docker daemon
* Python 3.6 (ideally in virtualenv)

This works in 1.3.2, but is broken in 1.3.1:
```
cd motolicious
pytest tests
```

-OR-

```
cd motolicious
tox
```

Running tests in PyCharm's pytest runner are currently broken.

If you end up with a docker container conflict (409) for some reason (usually due to an error in setup/teardown), run the following:
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

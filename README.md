# motolicious
Repo for tinkering with moto and localstack.

Requirements:
* Docker daemon
* Python 3.6 (ideally in virtualenv)

To run tests:
```
cd motolicious
pytest tests
```

If you end up with a docker container conflict (409), run the following:
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

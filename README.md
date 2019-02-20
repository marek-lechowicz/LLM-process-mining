# Prepare solutions for example problems

```
$ ./build-and-copy-solutions
```

# Build image

```
$ docker build --tag=tpaszun/thesis:latest .
```

Run bash in container

```
$ docker run --rm -i -t thesis bash
```

Copy files from container

```
$ docker cp <containerId>:/thesis/solutions solutions
```

Build image

```
docker build --tag=thesis .
```

Run bash in container

```
docker run --rm -i -t thesis bash
```

Copy files from container

```
docker cp <containerId>:/file/path/within/container /host/path/target
```

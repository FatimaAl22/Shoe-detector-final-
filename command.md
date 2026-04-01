# Shoe Detection API (YOLO)

## Build Docker Image 

```sh
docker build -t shoe-detector/api-server  -f Dockerfile .
```

## When it's fininshed you can run the server with 


```sh
docker run -p8000:8000 -it --rm shoe-detector/api-server
```


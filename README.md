# Stock Market Analysis with fin

This is a web-based tool to help you with analyzing and comparing different stocks.
The data will be provided by the beautiful [yfinance](https://pypi.org/project/yfinance/) project.

![alt text](getting_started.gif?raw=true "Title")

## Getting started

1. Build prod image

    ```
    docker-compose build --no-cache prod
    ```

2. After successfully building the image, create a container using

    ```
    docker-compose up -d --force-recreate prod
    ```

3. Open your browser at [http://localhost:8050](http://localhost:8050) .



## Dev Setup

You can create your dev container setup for development inside that container similar to the "Getting started" setup above:

1. Build dev image

    ```
    docker-compose build --no-cache dev
    ```

2.  After successfully building the image, start and stop the container once via command line.

    ```bash
    docker-compose up -d --force-recreate dev
    ```

3. You can use VsCode now to attach the dev container

4. Attach to your container using VSCode or via CLI

    ```
    docker exec -it fin_dev bash
    ```

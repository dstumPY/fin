# finance_book

This is a playground to work on financial python applications.

## Dev Setup

1. Build dev image

    ```
    docker-compose build --no-cache dev
    ```

2.  After successfully building the image, start and stop the container once via command line.

    ```bash
    docker-compose up -d --force-recreate dev
    ```

3. You can use VsCode now to attach the dev container
    
4. Install required pre-commits before your first commit.
    ```bash
    pre-commit install
    ```
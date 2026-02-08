# Contributions Documentation
This area is for all documentation neeeded to do contributions.

Contributions would include any steps needed to change the code, integrate modules, accept code changes and release the package.


# Package Release
1. ```uv run mypy --strict python```
2. ```uv run pytest```
3. ``` uv tool run licenseheaders -t ./docs/apache2.tmpl -o ftorres7382 -y 2026 -E py -E rs``` 
4. ```rm -r target/```
5. ```uv run maturin build --release --zig --compatibility pypi```
6. ```uv run maturin sdist```
7. For Windows: ```uv run maturin build --release --target x86_64-pc-windows-msvc --interpreter python3.12```
    1. REQUIREMENT: ```rustup target add x86_64-pc-windows-msvc```
8. (While having the ~/.pypirc set up) uv publish target/wheels/*

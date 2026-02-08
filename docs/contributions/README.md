# Contributions Documentation
This area is for all documentation neeeded to do contributions.

Contributions would include any steps needed to change the code, integrate modules, accept code changes and release the package.


# Package Release
1. ```uv run mypy --strict python```
2. ```uv run pytest```
3. ```rm -r target/```
3. ```uv run maturin build --release --zig --compatibility pypi```
4. ```uv run maturin sdist```
5. For Windows: ```uv run maturin build --release --target x86_64-pc-windows-msvc```
    1. ```rustup target add x86_64-pc-windows-msvc``` is needed
6. (While having the ~/.pypirc set up) uv publish target/wheels/*

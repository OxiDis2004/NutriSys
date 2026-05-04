# Generate documentation

This project uses Sphinx to generate documentation from Python docstrings.

### 1. Install dependencies

```bash
pip install sphinx sphinx-rtd-theme
```

### 2. Generate API documentation

```bash
cd ./server
sphinx-apidoc -o docs/source ./src
```

This command scans the Python source code and creates .rst files for modules.

### 3. Build HTML documentation

```bash
sphinx-build -b html docs/source docs/build/html
```

Generated documentation will be available in: `docs/build/html/index.html`

### 4. Create documentation archive

```bash
cd docs/build
zip -r nutrísys-documentation.zip html
```


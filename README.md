## 🥗 Food Recognition & Nutrition Analysis System

NutriSys is an intelligent system for recognizing food from images and calculating nutritional values.
It combines computer vision, backend processing, and scalable infrastructure to provide fast and accurate results.

### Features

- 📸 Food Recognition using AI
- 🍽 Nutritional Analysis (calories, proteins, fats, carbs)
- 🤖 Telegram Bot Integration for user interaction
- 🌐 Web Application interface
- Scalable Backend with Kubernetes

### ⚙️ Installation & Setup

1. Requirements

        kubectl
        helm

2. Clone repository

        git clone https://github.com/OxiDis2004/NutriSys.git
        cd NutriSys

3. Insert you data

    - Copy the configuration script:

             cp public-local-helm.sh local-helm.sh

    - Edit <code>local-helm.sh</code> and insert your data:
        - Replace <code><TELEGRAM-BOT></code> with your Telegram bot token
        - Configure access to GitHub Container Registry

4. Run cluster with Helm

    chmod +x local-helm.sh
    ./local-helm.sh

5. Verify deployment

    - Check if all pods are running:

            kubectl get pods

    - Check services:

          kubectl get services

### Running project as dev engineer

#### 1. Requirements

- git
- python 3.12 <
- docker
- kubectl
- helm

#### 2. Project clone

```bash
git clone https://github.com/OxiDis2004/NutriSys.git
cd NutriSys
```

#### 3. Project configuration

##### 3.1 Main System Configuration File

Create the following file in the user’s home directory:

```bash
touch ~/.nutri-system.properties
```

This file stores the primary confidential configuration values required for project startup

Example structure:

    TELEGRAM_BOT_TOKEN=your_telegram_token
    GHCR_USERNAME=your_registry_username
    GHCR_PASSWORD=your_registry_password

##### 3.2 Separate Dependency Environments for Each Subproject

Create a dedicated Python virtual environment for the backend server:

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a separate Python virtual environment for the Telegram bot:

```bash
cd telegram-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Node.js dependencies for the web frontend:

```bash
cd web
npm install
```

##### 3.3 Local `.env` File for Docker Compose

For convenient local development and testing, create a file named:

```bash
touch .env
```

Basic config file:

    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=nutrisys
    DB_USER=nutrisys_user
    DB_PASSWORD=strong_password

    TELEGRAM_BOT_TOKEN=your_telegram_token
    SERVER_HOST=server

### Code Documentation

The project uses Python docstrings according to PEP 257 and Google-style
docstring conventions.

All public modules, classes, functions and methods must contain docstrings.
Docstrings should explain not only what the code does, but also why it is
needed and how it should be used.

#### Required docstring structure

For functions and methods:

```python
def example_function(value: int) -> str:
    """Short description of the function.

    More detailed explanation of the logic if needed.

    Args:
        value (int): Input value.

    Returns:
        str: Result of processing.

    Raises:
        ValueError: If the input value is invalid.
    """
```

For classes:

```python
class ExampleClass:
    """Short description of the class.

    Describes the responsibility of the class and its role in the system.
    """
```

Documentation rules

- Public functions, classes and methods must have docstrings.
- Private helper methods may use short comments if their logic is not obvious.
- Docstrings must use triple double quotes: `"""`.
- Each docstring must start with a short summary sentence.
- Arguments, return values and exceptions must be documented.
- Documentation must be updated when the public interface changes.

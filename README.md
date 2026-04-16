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

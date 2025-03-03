# LLM-WLB-Classifier

## Overview
LLM-WLB-Classifier is a framework that classifies content related to **work-life balance** using an LLM (Large Language Model). It can analyze **tweets and articles** to determine opinions on work-life balance.

This framework supports:
- **Docker deployment** via GHCR (GitHub Container Registry).
- **Standalone usage** via GitHub Releases.

---

## Installation & Setup

### ** Install Required Software**
#### **A. Install Ollama** (Required for LLM Processing)
[Ollama](https://ollama.com) is a local LLM runner that must be installed on your system.
```bash
# Mac
brew install ollama

# Linux (Debian/Ubuntu)
curl -fsSL https://ollama.com/install.sh | sh

# Windows (via WSL)
wsl --install -d Ubuntu
curl -fsSL https://ollama.com/install.sh | sh
```

#### **B. Download Llama 3 Model** (Required for Classification)
Once Ollama is installed, download the **Llama 3** model:
```bash
ollama pull llama3
```

---

## Usage

### **Option 1: Using Docker (Recommended)**
You can run the framework **without installing dependencies manually** using Docker.

#### ** Pull & Run the Docker Image**
```bash
docker pull ghcr.io/YOUR_GITHUB_USERNAME/llm-wlb-classifier:latest
docker run --rm ghcr.io/YOUR_GITHUB_USERNAME/llm-wlb-classifier --tweet "work-life balance"
```

#### ** Run with Environment Variables** (For Credentials)
If you need to set environment variables (e.g., Twitter API keys):
```bash
docker run --rm \
  -e TWITTER_USERNAME="your_username" \
  -e TWITTER_PASSWORD="your_password" \
  ghcr.io/YOUR_GITHUB_USERNAME/llm-wlb-classifier --tweet "work-life balance"
```


---

### **Option 2: Using the GitHub Release (Manual Installation)**
If you don’t want to use Docker, you can download the framework manually.

#### ** Download the Latest Release**
Go to the **[Releases Page](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/releases)** and download `LLM-WLB-Classifier.tar.gz`.

#### ** Extract & Install Dependencies**
```bash
tar -xvzf LLM-WLB-Classifier.tar.gz
cd LLM-WLB-Classifier
pip install -r requirements.txt
```

#### ** Run the Framework**
```bash
python run.py --tweet "work-life balance"
```

---

## Setting Environment Variables
For secure authentication (e.g., Twitter login credentials), set environment variables before running the framework.

### **Linux & Mac**
```bash
export TWITTER_USERNAME="your_username"
export TWITTER_PASSWORD="your_password"
```

### **Windows (PowerShell)**
```powershell
$env:TWITTER_USERNAME="your_username"
$env:TWITTER_PASSWORD="your_password"
```

These variables will be used automatically when running the framework.

---

## Available Commands
### **Classify Tweets**
```bash
python run.py --tweet "work-life balance"
```

### **Classify Articles**
```bash
python run.py --article "https://example.com/article"
```

---

## Development & Testing
### **Run Automated Tests**
```bash
pytest -v tests/
```

---

## Contributing
If you’d like to contribute, fork this repository and submit a pull request! 🚀

---

## License
This project is licensed under the MIT License.


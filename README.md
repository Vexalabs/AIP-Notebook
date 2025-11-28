# AIP Notebooks - ML Model Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node 16+](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)

> **Empowering AI Innovation** - A complete, self-contained ML model development environment with automated deployment workflows.

---

## 🎯 What is AIP Notebooks?

AIP Notebooks is a downloadable development environment that enables data scientists and ML engineers to build, test, and deploy custom ML models without complex infrastructure setup. Get from idea to production in minutes, not days.

### ✨ Key Features

- 🚀 **One-Click Installation** - Automated setup for Windows and Mac
- 📓 **Integrated Jupyter Environment** - Pre-configured notebooks with sample models
- 🔄 **Live API Testing** - Each model runs as its own FastAPI endpoint
- 🎨 **Modern UI** - React-based interface for model selection and management
- 🔧 **Sample Models Included** - Crypto price prediction and soccer match outcomes
- 📦 **Structured Templates** - Professional code organization out of the box
- ✅ **Built-in Testing** - API compliance tests ensure deployment readiness
- 🐳 **Docker Ready** - Containerize your models with included Dockerfiles

---

## 🚀 Quick Start

### Installation

#### Windows
1. Download `AIP-Model-Builder-Installer.tar.gz` from [Releases](https://github.com/Vexalabs/AIP-Notebook/releases)
2. Extract the archive
3. Right-click `Install_Windows.bat` and select "Run as Administrator"
4. Double-click `AIP-Notebook.bat` on your desktop to launch

#### Mac/Linux
1. Download `AIP-Model-Builder-Installer.tar.gz` from [Releases](https://github.com/Vexalabs/AIP-Notebook/releases)
2. Extract the archive
3. Run: `bash Install_Mac.sh`
4. Launch the application

### First Steps

1. **Select a Sample Model** - Choose from Crypto or Soccer prediction models
2. **Start Building** - Jupyter notebook opens with your selected model
3. **Develop & Test** - Modify the model and test via the local API
4. **Deploy** - Package your model for production deployment

---

## 📋 What's Included

### Sample Models

#### 🪙 Crypto Price Prediction
- Predict cryptocurrency price movements
- FastAPI endpoint with `/predict` route
- Structured with schemas, model logic, and tests
- Docker-ready configuration

#### ⚽ Soccer Match Prediction
- Predict soccer match outcomes (Win/Draw/Loss)
- Complete API implementation
- Professional code organization
- Built-in compliance tests

### Development Tools

- **Frontend**: React application for model management
- **Backend**: FastAPI orchestration service
- **Jupyter**: Interactive development environment
- **Testing**: pytest framework with API compliance tests
- **Linting**: Black code formatter
- **Docker**: Containerization support

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Local Machine                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   React      │◄────►│   FastAPI    │◄────►│  Jupyter  │ │
│  │   Frontend   │      │   Backend    │      │  Notebook │ │
│  │ (Port 3000)  │      │ (Port 8000)  │      │           │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│                                │                             │
│                                ▼                             │
│                     ┌──────────────────┐                     │
│                     │   Your Model     │                     │
│                     │   API (FastAPI)  │                     │
│                     │   (Port 8080)    │                     │
│                     └──────────────────┘                     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AIP-Notebooks/
├── frontend/                # React UI application
│   ├── src/
│   └── package.json
├── backend/                 # FastAPI orchestration
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── sample_models/           # Model templates
│   ├── crypto/
│   │   ├── src/            # Model code
│   │   ├── tests/          # API tests
│   │   ├── Makefile        # Task automation
│   │   ├── Dockerfile      # Container config
│   │   └── README.md
│   └── soccer/
│       └── (same structure)
├── workspace/               # Your workspace
├── docs/                    # Documentation
├── install.ps1              # Windows installer
├── install_mac.sh           # Mac/Linux installer
└── README.md
```

---

## 🔧 Development

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Vexalabs/AIP-Notebook.git
cd AIP-Notebook

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Run the application
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Working with Sample Models

Each sample model includes a `Makefile` for common tasks:

```bash
cd sample_models/crypto

make install    # Install dependencies
make run        # Run the model API
make test       # Run compliance tests
make lint       # Format code with black
make build      # Build Docker image
make docker-run # Run in Docker
```

---

## 📚 Documentation

- **[Quick Start Guide](QUICK_START_GUIDE.md)** - Get up and running fast
- **[User Manual](USER_MANUAL.md)** - Complete feature documentation
- **[Distribution Guide](DISTRIBUTION_GUIDE.md)** - Package and deploy
- **[API Documentation](docs/API.md)** - Backend API reference
- **[Architecture](docs/ARCHITECTURE.md)** - Technical deep-dive

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ for the AI community
- Powered by FastAPI, React, and Jupyter
- Inspired by the need for simpler ML workflows

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Vexalabs/AIP-Notebook/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Vexalabs/AIP-Notebook/discussions)
- **Documentation**: [Full Docs](https://github.com/Vexalabs/AIP-Notebook/tree/main/docs)

---

**Ready to build your next ML model?** [Download the latest release](https://github.com/Vexalabs/AIP-Notebook/releases) and get started in minutes! 🚀

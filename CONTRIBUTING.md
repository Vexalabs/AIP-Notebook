# Contributing to AIP Notebooks

Thank you for your interest in contributing to AIP Notebooks! We welcome contributions from the community.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in [GitHub Issues](https://github.com/Vexalabs/AIP-Notebook/issues)
2. If not, create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Add relevant labels

### Submitting Changes

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/AIP-Notebook.git
   cd AIP-Notebook
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Test backend
   cd backend
   pytest

   # Test sample models
   cd sample_models/crypto
   make test
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature

   - Detailed description of what changed
   - Why the change was needed
   - Any breaking changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Wait for review

## 📋 Development Setup

See the [README.md](README.md#development) for detailed setup instructions.

### Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## 🎨 Code Standards

### Python
- Follow [PEP 8](https://pep8.org/)
- Use `black` for formatting: `black .`
- Use type hints where appropriate
- Write docstrings for functions and classes

### JavaScript/React
- Use ES6+ syntax
- Follow React best practices
- Use functional components with hooks
- Keep components small and focused

### General
- Write clear commit messages
- Keep PRs focused on a single feature/fix
- Update tests when changing functionality
- Update documentation when adding features

## ✅ Testing

### Backend Tests
```bash
cd backend
pytest
```

### Sample Model Tests
```bash
cd sample_models/crypto
make test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📝 Documentation

When adding new features:
- Update the README.md if user-facing
- Add/update docstrings in code
- Update relevant documentation in `docs/`
- Include examples where helpful

## 🐛 Bug Reports

A good bug report should include:
- **Title**: Clear, descriptive summary
- **Description**: What happened vs. what you expected
- **Steps to Reproduce**: Numbered list of steps
- **Environment**: OS, Python version, Node version
- **Screenshots**: If applicable
- **Logs**: Relevant error messages

## 💡 Feature Requests

A good feature request should include:
- **Title**: Clear description of the feature
- **Problem**: What problem does this solve?
- **Solution**: How should it work?
- **Alternatives**: Other solutions you've considered
- **Examples**: Similar features in other tools

## 🔍 Code Review Process

1. **Automated Checks**: CI/CD runs tests and linters
2. **Maintainer Review**: A maintainer reviews the code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged
5. **Release**: Changes are included in the next release

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior includes:**
- Being respectful and inclusive
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

### Enforcement

Violations may result in temporary or permanent ban from the project.

## 🎯 Good First Issues

Look for issues labeled `good first issue` - these are great for newcomers!

## 📞 Questions?

- **Discussions**: [GitHub Discussions](https://github.com/Vexalabs/AIP-Notebook/discussions)
- **Issues**: [GitHub Issues](https://github.com/Vexalabs/AIP-Notebook/issues)

---

Thank you for contributing to AIP Notebooks! 🚀

# Contributing to Visiting Card OCR Scanner

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Be respectful, inclusive, and collaborative. We welcome all contributions from the community.

## How to Contribute

### 1. Fork the Repository

```bash
# Fork the repo on GitHub by clicking the Fork button
git clone https://github.com/YOUR_USERNAME/Visiting-Card-OCR-Scanner.git
cd Visiting-Card-OCR-Scanner
git remote add upstream https://github.com/1509Shubham/Visiting-Card-OCR-Scanner.git
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Follow PEP 8 for Python code
- Write clear, descriptive commit messages
- Add comments for complex logic
- Test your changes locally

### 4. Commit Your Changes

```bash
git add .
git commit -m "Add feature: description of changes"
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

- Go to the original repository
- Click "New Pull Request"
- Select your branch
- Provide a clear description of changes
- Reference any related issues

## Development Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
```

## Code Style

- Use 4 spaces for indentation
- Follow PEP 8 guidelines
- Use type hints for functions
- Write docstrings for classes and modules

## Types of Contributions

### Bug Reports
- Use the GitHub Issues tracker
- Provide detailed reproduction steps
- Include error messages and logs
- Specify your environment (OS, Python version, etc.)

### Feature Requests
- Describe the feature clearly
- Explain the use case
- Provide examples if possible
- Discuss implementation approach

### Documentation
- Fix typos and improve clarity
- Add examples and clarifications
- Update outdated information
- Improve code comments

## Commit Message Guidelines

```
type: brief description

Detailed explanation of changes (if needed)

Types:
- feat: A new feature
- fix: A bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- perf: Performance improvements
- test: Adding or updating tests
```

## Questions?

Feel free to:
- Open an issue for discussion
- Start a GitHub discussion
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉

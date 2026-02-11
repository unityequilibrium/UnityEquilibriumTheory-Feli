# Contributing to UET Harness

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Install dependencies: `py -m pip install -r requirements.txt`
4. Run verification: `powershell -ExecutionPolicy Bypass -File .\verify_release.ps1`

## Making Changes

1. Create a branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test locally: `py scripts/run_suite.py --help`
4. Commit with clear message: `git commit -m "Add: your feature description"`

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Open a PR against `main` branch
4. Describe what your PR does and why

## Code Style

- Python: Follow PEP 8
- PowerShell: Use approved verbs where possible
- Keep functions focused and documented

## Reporting Issues

Open an issue with:
- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Python version (`py -V`)

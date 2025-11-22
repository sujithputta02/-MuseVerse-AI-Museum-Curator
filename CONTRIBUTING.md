# Contributing to MuseVerse AI Museum Curator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages or logs

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its benefits
3. Provide use cases and examples
4. Discuss implementation approach

### Code Contributions

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/sujithputta02/-MuseVerse-AI-Museum-Curator.git
cd -MuseVerse-AI-Museum-Curator

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GOOGLE_API_KEY=your_key_here" > .env
```

#### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow coding standards**
   - Use meaningful variable names
   - Add docstrings to functions and classes
   - Keep functions focused and small
   - Follow PEP 8 style guide

3. **Test your changes**
   ```bash
   python -m pytest tests/
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

#### Pull Request Process

1. Update documentation if needed
2. Ensure all tests pass
3. Update CHANGELOG.md with your changes
4. Push to your fork
5. Create a Pull Request with:
   - Clear title and description
   - Reference related issues
   - Screenshots (if UI changes)
   - Testing steps

## Project Structure

```
ai-museum-curator/
├── agents/          # AI agent implementations
├── tools/           # Utility tools (search, graphs, etc.)
├── utils/           # Helper functions
├── app.py           # Main Streamlit application
├── orchestrator.py  # Agent coordination
└── config.py        # Configuration settings
```

## Agent Development

When creating new agents:

1. Inherit from `BaseAgent`
2. Implement `_process()` method
3. Add proper error handling
4. Include logging
5. Update orchestrator integration

Example:
```python
from agents.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyNewAgent")
    
    def _process(self, input_data):
        # Your logic here
        return {"result": "data"}
```

## Testing Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use meaningful test names

## Documentation

- Update README.md for major features
- Add inline comments for complex logic
- Create guides for new capabilities
- Keep CHANGELOG.md current

## Code Review

All submissions require review. We look for:

- Code quality and readability
- Test coverage
- Documentation completeness
- Performance considerations
- Security best practices

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Celebrate contributions

## Questions?

- Open a discussion in Issues
- Check existing documentation
- Review closed PRs for examples

Thank you for contributing to MuseVerse! 🏛️✨

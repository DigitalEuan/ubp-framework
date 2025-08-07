# GLR Telecom SDK Development Guide

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   python -m pytest
   ```

## Code Structure

- `glr_core.py`: Core GLR implementation
- `telecom_core.py`: Telecom-specific components
- `test_telecom.py`: Test cases
- `docs/`: Documentation

## Adding New Features

1. Create a new branch
2. Implement your changes
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## Testing Guidelines

- Write unit tests for all new code
- Maintain >90% test coverage
- Use pytest for testing
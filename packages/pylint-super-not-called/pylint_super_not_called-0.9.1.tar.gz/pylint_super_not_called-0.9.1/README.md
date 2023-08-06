# Pylint super-not-called plugin

A Pylint plugin that enforces methods to call the parent method with super.

## Installation

```bash
# Install the package into your virtual environment:
pip install pylint_super_not_called

# Launch Pylint with the load-plugin option
pylint --load-plugin pylint_super_not_called .
```

Use pylintrc to automatically load the plugin if needed


## Configuration

- `super-enforced-methods`: a list of methods to check (default: 'setUp')

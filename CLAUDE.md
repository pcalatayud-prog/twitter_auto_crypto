# Code Style Guidelines

This document outlines the coding standards and style guidelines for the Bitcoin Twitter Bot project.

## Naming Conventions

- **Variables/Functions**: Use `snake_case` for all variable names and functions
  ```python
  def calculate_returns():
      daily_price = 1000
  ```

- **Classes**: Use `PascalCase` for all class names
  ```python
  class CryptoTracker:
      pass
  ```

## Import Order

Organize imports in the following order, with a blank line between each section:

1. Standard library imports
2. Third-party library imports 
3. Local/project imports

```python
# Standard library
import os
from datetime import datetime, timedelta

# Third-party libraries
import pandas as pd
import tweepy
import requests

# Local imports
from config.api_keys import TwitterCredentials
from config.constants import Emojis
```

## Type Annotations

Use type annotations for all function parameters and return values.

```python
def format_price(price: float) -> str:
    return f"{int(price):,}"

def get_historical_data() -> pd.DataFrame:
    # Implementation
    pass
```

## Docstrings

Write descriptive docstrings for all classes and functions. Use the following format:

```python
def function_name(param1: type, param2: type) -> return_type:
    """Short description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When and why this exception is raised
    """
```

## Error Handling

Use loguru for logging errors, warnings, and info messages:

```python
from loguru import logger

# Log levels
logger.debug("Detailed information for debugging")
logger.info("Confirmation that things are working as expected")
logger.warning("Something unexpected happened, but the program still works")
logger.error("The program couldn't perform some function due to a problem")
logger.critical("The program cannot continue running")
```

## Environment

Use conda for environment management:

```bash
# Create environment
conda create -n bitcoin_twitter python=3.9

# Activate environment
conda activate bitcoin_twitter

# Install packages
pip install -r requirements.txt
```

## Command-line Tools

For running the bot:

```bash
# Run the bot
python main.py
```

## Code Testing

When running any tests or checking your code, use:

```bash
# Run the bot with mock mode
python main.py
```
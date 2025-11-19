"""Input validation utilities."""

from typing import Any, Dict


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_input(
    value: Any,
    value_type: type,
    min_value: float = None,
    max_value: float = None,
    allowed_values: list = None
) -> tuple[bool, str]:
    """
    Validate input value.
    
    Args:
        value: Value to validate
        value_type: Expected type
        min_value: Minimum allowed value (for numbers)
        max_value: Maximum allowed value (for numbers)
        allowed_values: List of allowed values
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Type check
    if not isinstance(value, value_type):
        return False, f"Expected {value_type.__name__}, got {type(value).__name__}"
    
    # Range check for numbers
    if value_type in (int, float):
        if min_value is not None and value < min_value:
            return False, f"Value {value} below minimum {min_value}"
        if max_value is not None and value > max_value:
            return False, f"Value {value} above maximum {max_value}"
    
    # Allowed values check
    if allowed_values is not None and value not in allowed_values:
        return False, f"Value {value} not in allowed values: {allowed_values}"
    
    return True, ""


def validate_cli_components(components: Dict[str, float]) -> tuple[bool, str]:
    """
    Validate CLI component dict.
    
    Args:
        components: Dict with CLI component keys
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_keys = [
        'text_vagueness',
        'judicial_activism',
        'treaty_hierarchy',
        'precedent_weight',
        'amendment_difficulty'
    ]
    
    # Check all keys present
    missing_keys = set(required_keys) - set(components.keys())
    if missing_keys:
        return False, f"Missing required keys: {missing_keys}"
    
    # Validate each component
    for key in required_keys:
        value = components[key]
        is_valid, error = validate_input(value, float, 0.0, 1.0)
        if not is_valid:
            return False, f"Invalid {key}: {error}"
    
    return True, ""

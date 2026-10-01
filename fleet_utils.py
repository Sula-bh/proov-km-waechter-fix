# fleet_utils.py
# Helper functions for the KM-Waechter fleet service.

KM_PER_MILE = 1.60934


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km / KM_PER_MILE


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list, or 0 if the list is empty."""
    if not values:
        return 0
    return sum(values) / len(values)

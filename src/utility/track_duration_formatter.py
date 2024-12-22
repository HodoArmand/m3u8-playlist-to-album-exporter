""" Format track duration to hh:mm:ss """

def format_duration(seconds: int) -> str:
    """Format track duration to hh:mm:ss.

    Args:
        seconds (int): The duration in seconds.

    Returns:
        str: The formatted duration as a string in hh:mm:ss format.
    """

    # Reason: Even if truly an int is passed to the function, apparently it is not int enough for python, typecast again for correct behavior.
    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"

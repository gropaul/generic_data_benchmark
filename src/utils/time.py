def seconds_to_time(seconds: float) -> str:
    days = int(seconds // 86400)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'

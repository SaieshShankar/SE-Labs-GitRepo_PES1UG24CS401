import math


def parse_zone(text):
    """Return a title-cased zone and its area, or None for invalid input."""
    if not isinstance(text, str):
        return None
    try:
        name, area_text = text.split(':')
        area = float(area_text)
    except ValueError:
        return None

    name = name.strip()
    if not name or not math.isfinite(area) or area < 0:
        return None
    return name.title(), area


def moisture_average(readings_csv):
    """Return the floor of the average of integer percentages, or None."""
    if not isinstance(readings_csv, str):
        return None
    try:
        values = [int(reading) for reading in readings_csv.split(',')]
    except ValueError:
        return None

    if any(not 0 <= reading <= 100 for reading in values):
        return None
    return sum(values) // len(values)


def water_needed(text):
    """Return the finite, nonnegative water estimate, or None."""
    if not isinstance(text, str):
        return None
    try:
        area, rain = (float(field) for field in text.split('|'))
    except ValueError:
        return None

    if any(not math.isfinite(value) or value < 0 for value in (area, rain)):
        return None
    need = area * 5 - rain
    if not math.isfinite(need):
        return None
    return max(need, 0)


def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    result = parse_zone(user_input)
    print("Zone and Area:", result if result is not None else "Invalid input")

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    result = moisture_average(user_input)
    print("Average Moisture:", result if result is not None else "Invalid input")

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    result = water_needed(user_input)
    print("Water Needed:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()

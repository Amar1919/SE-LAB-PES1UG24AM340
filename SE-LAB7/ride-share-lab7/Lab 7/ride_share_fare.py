
def parse_trip(text):
    if not isinstance(text, str):
        raise ValueError("Trip input must be a string")

    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("Input must be in cab:distance format")

    cab, km = parts

    if not cab.strip():
        raise ValueError("Cab name cannot be empty")

    try:
        km = float(km)
    except ValueError:
        raise ValueError("Distance must be a valid number")

    if not math.isfinite(km) or km <= 0:
        raise ValueError("Distance must be positive and finite")

    return cab.strip().title(), km


def fare_average(fares_csv):
    if not isinstance(fares_csv, str) or not fares_csv.strip():
        raise ValueError("Fares must be a non-empty string")

    try:
        values = [int(r.strip()) for r in fares_csv.split(',')]
    except ValueError:
        raise ValueError("Fares must contain valid integers")

    if not values:
        raise ValueError("At least one fare is required")

    if any(value < 0 for value in values):
        raise ValueError("Fares cannot be negative")

    return int(sum(values) / len(values))

def payable_fare(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("Input must be in fare|promo format")

    fare, promo = parts

    try:
        fare = float(fare)
        promo = float(promo)
    except ValueError:
        raise ValueError("Fare and promo must be valid numbers")

    if not math.isfinite(fare) or not math.isfinite(promo):
        raise ValueError("Fare and promo must be finite")

    if fare < 0 or promo < 0:
        raise ValueError("Fare and promo cannot be negative")

    if promo > fare * 1.18:
        raise ValueError("Promo cannot exceed the tax-inclusive fare")

    return fare * 1.18 - promo


import math


def main():
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    try:
        result = parse_trip(user_input)
        print("Cab and Distance:", result)
    except ValueError as e:
        print("Invalid trip:", e)

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    try:
        result = fare_average(user_input)
        print("Average Fare:", result)
    except ValueError as e:
        print("Invalid fares:", e)

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    try:
        result = payable_fare(user_input)
        print("Payable Fare:", result)
    except ValueError as e:
        print("Invalid payment:", e)


if __name__ == "__main__":
    main()

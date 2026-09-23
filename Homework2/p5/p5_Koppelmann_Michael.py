# Question 5 and combined all chats into one file
import datetime
import math
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def read_observations(lines):
    result = {"observations": {}, "errors": []}
    seen = set()

    for line_number, line in enumerate(lines, start=1):
        parts = line.strip().split(",")

        if len(parts) != 3:
            result["errors"].append({
                "line_number": line_number,
                "error_message": "Malformed line",
            })
            continue

        station, date_text, temperature_text = (
            part.strip() for part in parts
        )

        try:
            observation_date = datetime.datetime.fromisoformat(date_text)
        except ValueError:
            result["errors"].append({
                "line_number": line_number,
                "error_message": "Invalid date",
            })
            continue

        try:
            temperature = float(temperature_text)
            if not math.isfinite(temperature):
                raise ValueError
        except ValueError:
            result["errors"].append({
                "line_number": line_number,
                "error_message": "Invalid temperature",
            })
            continue

        station_date = (station, observation_date)

        if station_date in seen:
            result["errors"].append({
                "line_number": line_number,
                "error_message": "Duplicate station/date combination",
            })
            continue

        seen.add(station_date)
        result["observations"].setdefault(station, []).append({
            "date": observation_date,
            "temperature": temperature,
        })

    return result


def station_statistics(observations):
    return {
        station: {
            "min": min(item["temperature"] for item in readings),
            "max": max(item["temperature"] for item in readings),
            "mean": sum(item["temperature"] for item in readings)
            / len(readings),
        }
        for station, readings in observations.items()
        if readings
    }


def station_temperature_outliers(observations):
    means = {
        station: sum(item["temperature"] for item in readings) / len(readings)
        for station, readings in observations.items()
        if readings
    }

    return {
        station: {
            item["date"]: (item["temperature"], means[station])
            for item in readings
            if item["temperature"] > means[station]
        }
        for station, readings in observations.items()
        if any(item["temperature"] > means[station] for item in readings)
    }


def write_statistics(statistics, outliers, errors):
    lines = ["Statistics:"]

    for station in sorted(statistics):
        values = statistics[station]
        lines.append(
            f"{station}: min={values['min']:.1f}, "
            f"max={values['max']:.1f}, mean={values['mean']:.1f}"
        )

    lines.append("")
    lines.append("Outliers:")

    for station in sorted(outliers):
        for date, (temperature, mean) in sorted(
            outliers[station].items(),
            key=lambda item: item[0].isoformat(),
        ):
            lines.append(
                f"{station}, {date.isoformat()}, "
                f"{temperature:.1f}, mean={mean:.1f}"
            )

    lines.append("")
    lines.append("Errors:")

    for error in errors:
        lines.append(
            f"line {error['line_number']}: {error['error_message']}"
        )

    return "\n".join(lines)


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python weather.py INPUT_FILE [OUTPUT_FILE]")
        return 2

    input_name = Path(sys.argv[1])
    output_name = (
        Path(sys.argv[2])
        if len(sys.argv) == 3
        else input_name.with_suffix(input_name.suffix + ".out")
    )

    try:
        with input_name.open("r", encoding="utf-8") as input_file:
            parsed = read_observations(input_file)

        statistics = station_statistics(parsed["observations"])
        outliers = station_temperature_outliers(parsed["observations"])
        output = write_statistics(
            statistics,
            outliers,
            parsed["errors"],
        )

        print(output)

        with output_name.open("w", encoding="utf-8") as output_file:
            output_file.write(output + "\n")

        return 0

    except OSError as error:
        print(f"File error: {error}", file=sys.stderr)
        return 1


class WeatherTests(unittest.TestCase):

    def test_multiple_stations_are_read(self):
        result = read_observations([
            "Alpha,2026-01-01T10:00:00,10",
            "Beta,2026-01-01T10:00:00,20",
        ])
        self.assertEqual(set(result["observations"]), {"Alpha", "Beta"})

    def test_minimum_temperature(self):
        observations = read_observations([
            "Alpha,2026-01-01T10:00:00,10",
            "Alpha,2026-01-01T11:00:00,5",
        ])["observations"]
        self.assertEqual(station_statistics(observations)["Alpha"]["min"], 5)

    def test_maximum_temperature(self):
        observations = read_observations([
            "Alpha,2026-01-01T10:00:00,10",
            "Alpha,2026-01-01T11:00:00,15",
        ])["observations"]
        self.assertEqual(station_statistics(observations)["Alpha"]["max"], 15)

    def test_mean_temperature(self):
        observations = read_observations([
            "Alpha,2026-01-01T10:00:00,10",
            "Alpha,2026-01-01T11:00:00,20",
        ])["observations"]
        self.assertEqual(station_statistics(observations)["Alpha"]["mean"], 15)

    def test_outlier_above_mean(self):
        observations = read_observations([
            "Alpha,2026-01-01T10:00:00,10",
            "Alpha,2026-01-01T11:00:00,20",
        ])["observations"]
        outliers = station_temperature_outliers(observations)
        self.assertIn("Alpha", outliers)
        self.assertEqual(len(outliers["Alpha"]), 1)

    def test_station_without_outliers_is_omitted(self):
        observations = read_observations([
            "Alpha,2026-01-01T10:00:00,10",
            "Alpha,2026-01-01T11:00:00,10",
        ])["observations"]
        self.assertEqual(station_temperature_outliers(observations), {})

    def test_malformed_line_is_rejected(self):
        result = read_observations(["invalid line"])
        self.assertEqual(len(result["errors"]), 1)

    def test_invalid_temperature_is_rejected(self):
        result = read_observations([
            "Alpha,2026-01-01T10:00:00,hot"
        ])
        self.assertEqual(result["errors"][0]["error_message"], "Invalid temperature")

    def test_duplicate_station_date_is_rejected(self):
        result = read_observations([
            "Alpha,2026-01-01T10:00:00,10",
            "Alpha,2026-01-01T10:00:00,20",
        ])
        self.assertEqual(
            result["errors"][0]["error_message"],
            "Duplicate station/date combination",
        )

    def test_output_is_sorted_and_formatted(self):
        output = write_statistics(
            {
                "Zulu": {"min": 1, "max": 2, "mean": 1.5},
                "Alpha": {"min": 3, "max": 4, "mean": 3.5},
            },
            {},
            [],
        )
        self.assertLess(output.index("Alpha"), output.index("Zulu"))
        self.assertIn("mean=1.5", output)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith("test"):
        unittest.main()
    else:
        raise SystemExit(main())
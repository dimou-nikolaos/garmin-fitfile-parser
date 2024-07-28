"""fitfile pace plotter"""
import argparse
import fitparse
from datetime import datetime
import matplotlib.pyplot as plt
import mplcursors

def strip_date_and_split_time(timestamps):
    """Function that strips date and splits time"""
    hours = []
    minutes = []
    seconds = []

    for timestamp in timestamps:
        dt = timestamp
        hours.append(dt.hour)
        minutes.append(dt.minute)
        seconds.append(dt.second)

    return hours, minutes, seconds

def normalize_time(datetime_objects):
    """Function that normalizes time - subtracts starting time"""
    start_time = datetime_objects[0]
    normalized_times = []

    for dt in datetime_objects:
        delta = dt - start_time
        total_seconds = delta.total_seconds()
        normalized_times.append(total_seconds)

    return normalized_times

def format_time(seconds):
    """Function that formats the time"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Process some strings.")
    parser.add_argument('file_name', type=str, help='The string to be processed')
    args = parser.parse_args()
    fit_file_string = args.file_name

    fitfile = fitparse.FitFile(fit_file_string)

    timestamps = []
    speeds = []

    for record in fitfile.get_messages("record"):
        for data in record:
            if data.name == "enhanced_speed":
                speeds.append(data.value)
            if data.name == "timestamp":
                timestamps.append(data.value)

    hours, minutes, seconds = strip_date_and_split_time(timestamps)
    normalized_times = normalize_time(timestamps)

    paces = [60 / (speed * 60 * 60 / 1000) for speed in speeds]
    paces_minutes = [int(pace) for pace in paces]
    paces_seconds = [(pace - int(pace)) * 60 for pace in paces]
    paces_combined = [f"{int(pace)}:{int((pace - int(pace)) * 60):02d}" for pace in paces]

    formatted_times = [format_time(t) for t in normalized_times]

    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(normalized_times, paces, marker='o')
    ax.set_xlabel('Time [hh:mm:ss]')
    ax.set_ylabel('Pace [min:sec per km]')
    ax.set_title('Pace over Time')
    ax.grid(True)

    # Select a subset of x-tick positions and labels
    num_ticks = min(10, len(normalized_times))  # Limit to 10 or fewer ticks
    tick_positions = normalized_times[::max(1, len(normalized_times) // num_ticks)]
    tick_labels = formatted_times[::max(1, len(formatted_times) // num_ticks)]

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')

    # Invert the y-axis for paces
    ax.invert_yaxis()

    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{formatted_times[sel.target.index]}\n"
        f"{paces_minutes[sel.target.index]}:{int(paces_seconds[sel.target.index]):02d} min/km"
    ))

    plt.show()

if __name__ == "__main__":
    main()

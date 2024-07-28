import argparse
import matplotlib.pyplot as plt
import mplcursors
import fitparse
from gmplot import gmplot

def normalize_time(datetime_objects):
    """Function that normalizes time - subtracts starting time"""
    start_time = datetime_objects[0]
    return [(dt - start_time).total_seconds() for dt in datetime_objects]

def format_time(seconds):
    """Function that formats the time"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Process a FIT file and plot paces over time.")
    parser.add_argument('file_name', type=str, help='The FIT file to be processed')
    return parser.parse_args()

def parse_fitfile_timestamps(fitfile):
    """Parse timestamps from the FIT file"""
    timestamps = []
    for record in fitfile.get_messages("record"):
        for data in record:
            if data.name == "timestamp":
                timestamps.append(data.value)
    return timestamps

def parse_fitfile_speeds(fitfile):
    """Parse speeds from the FIT file"""
    speeds = []
    for record in fitfile.get_messages("record"):
        for data in record:
            if data.name == "enhanced_speed":
                speeds.append(data.value)
    return speeds

def parse_fitfile_longitude(fitfile):
    """Parse longitude from the FIT file"""
    longitude = []
    for record in fitfile.get_messages("record"):
        for data in record:
            if data.name == "position_long":
                # convert semicycles to degrees
                longitude.append(data.value * ( 180 / 2**31))
    return longitude

def parse_fitfile_latitude(fitfile):
    """Parse latitude from the FIT file"""
    latitude = []
    for record in fitfile.get_messages("record"):
        for data in record:
            if data.name == "position_lat":
                # convert semicycles to degrees
                latitude.append(data.value * ( 180 / 2**31))
    return latitude

def parse_fitfile_altitude(fitfile):
    """Parse altitude from the FIT file"""
    altitude = []
    for record in fitfile.get_messages("record"):
        for data in record:
            if data.name == "enhanced_altitude":
                # convert semicycles to degrees
                altitude.append(data.value)
    return altitude

def calculate_paces_minutes(speeds):
    """Calculate paces in minutes per km"""
    paces = [60 / (speed * 60 * 60 / 1000) for speed in speeds]
    return [int(pace) for pace in paces]

def calculate_paces_seconds(paces):
    """Calculate paces in seconds"""
    return [(pace - int(pace)) * 60 for pace in paces]

def plot_paces(normalized_times, paces, formatted_times, paces_minutes, paces_seconds):
    """Plot paces over time"""
    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(normalized_times, paces, marker='o')
    ax.set_xlabel('Time [hh:mm:ss]')
    ax.set_ylabel('Pace [min:sec per km]')
    ax.set_title('Pace over Time')
    ax.grid(True)

    num_ticks = min(10, len(normalized_times))  # Limit to 10 or fewer ticks
    tick_positions = normalized_times[::max(1, len(normalized_times) // num_ticks)]
    tick_labels = formatted_times[::max(1, len(formatted_times) // num_ticks)]

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')

    ax.invert_yaxis()

    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{formatted_times[sel.target.index]}\n"
        f"{paces_minutes[sel.target.index]}:{int(paces_seconds[sel.target.index]):02d} min/km"
    ))

    plt.show()

def create_map_html(latitude, longitude):
    """Creates html with activity on Google Maps"""

    # Initialize the map at a given point
    gmap = gmplot.GoogleMapPlotter(latitude[1], longitude[1], 14, 'cornflowerblue')

    for i in range(1, len(latitude)):
        # Add a marker
        gmap.marker(latitude[i], longitude[i], 'cornflowerblue')

    # Draw map into HTML file
    gmap.draw("my_map.html")

def main():
    """Main function"""
    args = parse_arguments()
    fitfile = fitparse.FitFile(args.file_name)

    timestamps = parse_fitfile_timestamps(fitfile)
    speeds = parse_fitfile_speeds(fitfile)
    altitude = parse_fitfile_altitude(fitfile)
    latitude = parse_fitfile_latitude(fitfile)
    longitude = parse_fitfile_longitude(fitfile)

    # Draw activity on map in html
    create_map_html(latitude, longitude)

    normalized_times = normalize_time(timestamps)
    paces = [60 / (speed * 60 * 60 / 1000) for speed in speeds]
    paces_minutes = calculate_paces_minutes(speeds)
    paces_seconds = calculate_paces_seconds(paces)

    formatted_times = [format_time(t) for t in normalized_times]

    plot_paces(normalized_times, paces, formatted_times, paces_minutes, paces_seconds)

if __name__ == "__main__":
    main()


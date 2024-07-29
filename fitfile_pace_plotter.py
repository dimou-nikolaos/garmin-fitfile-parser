import argparse
import matplotlib.pyplot as plt
import mplcursors
from gmplot import gmplot
import folium
import geopy.distance

from fitfile_parser import (
    parse_fitfile,
    parse_fitfile_timestamps,
    parse_fitfile_speeds,
    parse_fitfile_longitude,
    parse_fitfile_latitude,
    parse_fitfile_altitude
    )

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

def calculate_paces_minutes(paces):
    """Calculate paces in minutes per km"""
    return [int(pace) for pace in paces]

def calculate_paces_seconds(paces):
    """Calculate paces in seconds"""
    return [(pace - int(pace)) * 60 for pace in paces]

def plot_paces(normalized_times, paces, my_paces, my_pace_normalized, formatted_times, paces_minutes, paces_seconds, my_paces_minutes, my_paces_seconds, my_paces_normalized_minutes, my_paces_normalized_seconds):
    """Plot paces over time"""
    fig, ax = plt.subplots(figsize=(10, 5))
    scatter1 = ax.scatter(normalized_times, paces, marker='o', color='red', label='Original Paces')
    scatter2 = ax.scatter(normalized_times, my_paces, marker='o', color='blue', label='My Paces')
    scatter3 = ax.scatter(normalized_times, my_pace_normalized, marker='o', color='green', label='My Paces Normalized')

    ax.set_xlabel('Time [hh:mm:ss]')
    ax.set_ylabel('Pace [min:sec per km]')
    ax.set_title('Pace over Time')
    ax.grid(True)
    ax.legend()

    num_ticks = min(10, len(normalized_times))  # Limit to 10 or fewer ticks
    tick_positions = normalized_times[::max(1, len(normalized_times) // num_ticks)]
    tick_labels = formatted_times[::max(1, len(formatted_times) // num_ticks)]

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')

    ax.invert_yaxis()

    cursor = mplcursors.cursor([scatter1, scatter2, scatter3], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{formatted_times[sel.target.index]}\n"
        f"Original: {paces_minutes[sel.target.index]}:{int(paces_seconds[sel.target.index]):02d} min/km\n"
        f"My Pace: {my_paces_minutes[sel.target.index]}:{int(my_paces_seconds[sel.target.index]):02d} min/km\n"
        f"My Pace normalized: {my_paces_normalized_minutes[sel.target.index]}:{int(my_paces_normalized_seconds[sel.target.index]):02d} min/km"
    ))

    plt.show()


def create_map_html(latitude, longitude):
    """Creates html with activity on Google Maps"""

    # Initialize the map at a given point
    gmap = gmplot.GoogleMapPlotter(latitude[0], longitude[0], 14, 'cornflowerblue')

    for i in range(1, len(latitude)):
        # Add a marker
        gmap.marker(latitude[i], longitude[i], 'cornflowerblue')

    # Draw map into HTML file
    gmap.draw("activity_on_google_map.html")

def create_folium_map(latitude, longitude):
    """Creates map using folium"""

    # Initialize the map at a given point
    map=folium.Map(location=[latitude[1], longitude[1]])

    for i in range(1, len(latitude)):
        # Add a marker
        map.add_child(folium.Marker(location=[latitude[i], longitude[i]]))

    # save map
    map.save("activity_on_folium_map.html")

def main():
    """Main function"""
    args = parse_arguments()

    timestamps, speeds, altitude, latitude, longitude = parse_fitfile(args.file_name)

    strides = []
    # add manually one element to match other arrays
    strides.append(0)
    for elem in range(1, len(latitude)):
	    coord0=(latitude[elem-1], longitude[elem-1])
	    coord1=(latitude[elem], longitude[elem])
	    strides.append(geopy.distance.geodesic(coord0, coord1).m)

    my_pace = []
    my_pace.append(0)
    for elem in range(1, len(strides)):
        my_pace.append(1000/(60*strides[elem]))
    my_paces_minutes = calculate_paces_minutes(my_pace)
    my_paces_seconds = calculate_paces_seconds(my_pace)

    #normalize
    my_pace_normalized = [0] * len(my_pace)
    ROLLING_WINDOW = 20
    for i in range(ROLLING_WINDOW):
        my_pace_normalized[i] = 0

    for i in range(ROLLING_WINDOW-1, len(my_pace)):
        for j in range(ROLLING_WINDOW):
            my_pace_normalized[i] += my_pace[i-j]
        my_pace_normalized[i] /=ROLLING_WINDOW
    my_paces_normalized_minutes = calculate_paces_minutes(my_pace_normalized)
    my_paces_normalized_seconds = calculate_paces_seconds(my_pace_normalized)

    # Draw activity on map in html
    create_map_html(latitude, longitude)

    # Create folium map
    create_folium_map(latitude, longitude)
    

    normalized_times = normalize_time(timestamps)
    paces = [60 / (speed * 60 * 60 / 1000) for speed in speeds]
    paces_minutes = calculate_paces_minutes(paces)
    paces_seconds = calculate_paces_seconds(paces)

    formatted_times = [format_time(t) for t in normalized_times]

    plot_paces(normalized_times, paces, my_pace ,my_pace_normalized, formatted_times, paces_minutes, paces_seconds, my_paces_minutes, my_paces_seconds, my_paces_normalized_minutes, my_paces_normalized_seconds)

if __name__ == "__main__":
    main()


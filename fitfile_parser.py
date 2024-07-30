import fitparse

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

def parse_fitfile(filename):
    """"Fitfile parset"""
    fitfile = fitparse.FitFile(filename)
    timestamps = parse_fitfile_timestamps(fitfile)
    speeds = parse_fitfile_speeds(fitfile)
    altitude = parse_fitfile_altitude(fitfile)
    latitude = parse_fitfile_latitude(fitfile)
    longitude = parse_fitfile_longitude(fitfile)
    return timestamps, speeds, altitude, latitude, longitude

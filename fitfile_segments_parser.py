import argparse
import fitparse

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process some strings.")
 
    # Add an argument to parse a string
    parser.add_argument('file_name', type=str, help='The string to be processed')

    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed string
    fit_file_string = args.file_name

    # Load the FIT file
    fitfile = fitparse.FitFile(fit_file_string)

    # Iterate over all messages of type "record"
    # (other types include "device_info", "file_creator", "event", etc)
    for record in fitfile.get_messages("record"):

        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in record:

            # Print the name and value of the data (and the units if it has any)
            if data.units:
                print(" * {}: {} ({})".format(data.name, data.value, data.units))
            else:
                print(" * {}: {}".format(data.name, data.value))

        print("---")

if __name__ == "__main__":
    main()

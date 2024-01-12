from PIL import Image
from PIL import ExifTags
from math import sin, cos, sqrt, atan2, radians


def open_file(file_name):
    """Open txt files to read the content"""
    with open(file_name, "r") as f:
        return f.read()


def geonames_matrix(file_name):
    """Open the Geonames database and turn it into a matrix, making a list of every row"""
    data = open_file(file_name)
    data = data.rstrip()
    data_list = data.split("\n")
    data_matrix = [line.split("\t") for line in data_list]
    return data_matrix


def coordinate_converter(degrees, minutes, seconds, direction):
    """convert DMS coordinares to DD coordinares for easier distance calculations"""
    decimal_degrees = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)

    if direction == 'S' or direction == 'W':
        decimal_degrees *= -1

    return float(decimal_degrees)


def distance(latitude_tomb, longitude_tomb, latitude_data, longitude_data):
    '''math formula for distance between 2 coordinates
    
    mathematic formula turned to python code by Michael0x2a edited by Peter Mortensen
    on stackoverflow

    link:
    https://stackoverflow.com/a/19412565'''

    # Approximate radius of earth in km
    R = 6373.0

    lon = longitude_data - longitude_tomb
    lat = latitude_data - latitude_tomb

    a = sin(lat / 2)**2 + cos(latitude_tomb) * cos(latitude_data) * sin(lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return float(distance)


def main():
    # open files for data
    all_tombs = open_file("tombs_no_geo.txt")
    all_tombs_list = all_tombs.split("\n\n")

    geo_matrix = geonames_matrix("NL.txt")

    # geotagging code
    for tomb_data in all_tombs_list:
        tomb_id = tomb_data[1:7]
        tomb_img = Image.open('TombReader-1.0.0/in/'+tomb_id+'.jpg')

        # get only the coordinates of the metadata and convert it
        tomb_meta = {ExifTags.TAGS[k]: v for k, v in tomb_img._getexif().items() if k in ExifTags.TAGS and ExifTags.TAGS[k] == 'GPSInfo'}

        try:
            k = 'GPSInfo'
            long_tomb = coordinate_converter(tomb_meta[k][2][0], tomb_meta[k][2][1], tomb_meta[k][2][2], tomb_meta[k][1])
            lat_tomb = coordinate_converter(tomb_meta[k][4][0], tomb_meta[k][4][1], tomb_meta[k][4][2], tomb_meta[k][3])
        except:
            long_tomb = 0
            lat_tomb = 0

        # same name baseline
        previous_line = ""
        for line in tomb_data.split("\n"):
            if "geo" in line:
                place = previous_line.strip()[6:-1]
                for row in geo_matrix:
                    if row[1].lower() == place.lower():
                        line = line.replace('""', '"'+row[0]+'"')
                        break
            
            # uncomment line below for baseline 1
            # print(line)

            previous_line = line

        # closest distance baseline
        shortest = 99999999
        geocode = ""
        for row in geo_matrix:
            long_data = float(row[4])
            lat_data = float(row[5])

            new_dis = distance(lat_tomb, long_tomb, lat_data, long_data)
            if new_dis == min(shortest, new_dis):
                shortest = new_dis
                geocode = row[0]

        for item in tomb_data.split("\n"):
            if "geo" in item:
                item = item.replace('""', '"'+geocode+'"')
            
            # uncomment line below for baseline 2
            # print(item)

        # final code
        previous_line = ""
        for line in tomb_data.split("\n"):
            if "geo" in line:
                place = previous_line.strip()[6:-1]

                name_matches = [row for row in geo_matrix if row[1].lower() == place.lower()]

                shortest = 99999999
                geocode = ""

                for row in name_matches:
                    long_data = float(row[4])
                    lat_data = float(row[5])

                    new_dis = distance(lat_tomb, long_tomb, lat_data, long_data)
                    if new_dis == min(shortest, new_dis):
                        shortest = new_dis
                        geocode = row[0]

                line = line.replace('""', '"'+str(geocode)+'"')
            
            # uncomment line below for results
            # print(line)

            previous_line = line

        print()


if __name__ == '__main__':
    main()

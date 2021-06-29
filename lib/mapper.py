# Import Modules
import requests
import xlsxwriter
from shapely.geometry import Polygon
from shapely.geometry import Point


# Grab Sector from Combine's Web Services
def api_call(query_type, query_id):
    headers = {"Accept": "application/json"}
    r = requests.get(f'https://www.swcombine.com/ws/v2.0/galaxy/{query_type}/{query_id}', headers=headers)
    json = r.json()
    if query_type[:-1] in json['swcapi']:
        return json['swcapi'][query_type[:-1]]
    else:
        return None


# Get a list of points where Systems exist
def get_systems(systems_list):
    if 'system' not in systems_list:
        return []

    multipoint = []
    for system in systems_list['system']:
        query = api_call('systems', system['attributes']['uid'])
        coordinates = query['location']['coordinates']['galaxy']['attributes']
        multipoint.append(Point(coordinates['x'], coordinates['y']))
    return multipoint


# Make the Polygon Object based on the points provided by Combine's API
def make_polygon(point_list):
    points = [(point['attributes']['x'], point['attributes']['y']) for point in point_list]
    return Polygon(points)


# Function to create the Spreadsheet
def make_spreadsheet(sector_name, sector_shape, systems_list, path):

    # Define the Spreadsheet's settings
    workbook = xlsxwriter.Workbook(f'{path}/{sector_name}.xlsx')
    worksheet = workbook.add_worksheet()
    coordinate_header = workbook.add_format({
        'font_color': 'white',
        'font_size': '7',
        'bg_color': 'black',
        'align': 'center'})
    empty_grid = workbook.add_format({'bg_color': '#0201ff'})
    occupied_grid = workbook.add_format({'bg_color': '#48ff00'})
    outside_grid = workbook.add_format({'bg_color': '#666666'})

    # Define columns and rows based on the Sector's polygon
    minx, miny, maxx, maxy = sector_shape.bounds
    columns = int(maxx - minx)
    rows = int(maxy - miny)

    # Create the Headers (top row and left column)
    worksheet.write_blank(0, 0, None, coordinate_header)
    worksheet.write_row(0, 1, range(int(minx), int(maxx)), coordinate_header)
    worksheet.write_column(1, 0, reversed(range(int(miny), int(maxy))), coordinate_header)
    worksheet.set_column_pixels(0, columns+1, 24)
    worksheet.freeze_panes(1, 1)

    # Format cells based on the Sector's Polygon and the known Systems
    column = 1
    while column <= columns:
        row = 1
        x_coord = int(minx + column - 1)
        while row <= rows:
            y_coord = int(maxy - row)
            cell = Point(x_coord, y_coord)
            if sector_shape.contains(cell):
                if cell in systems_list:
                    worksheet.write_blank(row, column, None, occupied_grid)
                else:
                    worksheet.write_blank(row, column, None, empty_grid)
            else:
                worksheet.write_blank(row, column, None, outside_grid)
            row += 1
        column += 1

    # Save and close the Spreadsheet
    workbook.close()

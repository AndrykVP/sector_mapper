# Sector Mapper
A python script to create a spreadsheet file from coordinates received from [Star Wars Combine](https://www.swcombine.com/) web services.

## Dependencies

- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pyinstaller](https://www.pyinstaller.org/)
- [XlsxWriter](https://xlsxwriter.readthedocs.io/getting_started.html)
- [Shapely](https://shapely.readthedocs.io/en/stable/manual.html)

## Usage

Download the latest version from Releases, based on your Operating System.

The executable will open a window asking for a Sector ID. You can get this ID by going to the [Galaxy Map](https://www.swcombine.com/rules/?Galaxy_Map) in Star Wars Combine, and check the URL after clicking/searching for the desired sector.

By default, the script will use the user's `home` folder but there is a button so selected a different output directory.

After clicking the "Generate Map" button, a .xlsx file will be created in the output directory, using the Sector's name as the filename.

Note: The limitations from the XlsxWriter module prevent the script from creating the .xlsx file if there's already a file with the same name in the selected directory.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

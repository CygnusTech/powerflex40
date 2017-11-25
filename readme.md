# Powerflex40 Config Backup

This is a basic python script which uses the modbus RTU connectivity of Rockwell Automation PowerFlex 40 variable frequency drives (VFDs) to pull the current configuration parameters and store them as CSV files.

The motivation was that a customer's control panel had 25 VFDs, but they did not have the configurations for them.  When a VFD required replacement it was difficult to have it configured correctly.  The CSVs produced by this script offer a snapshot view of the current configurations.

The script could be augmented with the ability to write to/configure the VFDs as well, but this was outside the scope of this project.  It could also be changed to constantly poll the current operational charactersitics of the VFDs (the 'd' parameters).

The usage is basic.  Edit the script to configure all the VFDs and their modbus addresses.  When the script is run it will attempt to connect to each VFD and then perform a modbus read of each parameter, and then store them to an appropriately named CSV file.  After the list of VFDs has been traversed, the script also outputs a results file to show which VFDs were connected to successfully.

A sample of the output CSV is provided.

## License
powerflex40.py
Copyright (C) 2017  Cygnus Technical Services Ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

# RangeMap
CSV recordkeeping for signal strength mapping with Sideband

Piggybacks on an existing NomadNet identity, outputs to CSV in the same directory. Is not tested for robustness, but was set up for simplicity and expediency. 

Unless you want to know the distance to O'Hare International Airport, make sure to change your base station address. Elevation and distance are in meters. There is basically no error handling.

CSV format:
LXMF Address, Time (UTC), Latitude, Longitude, Altitude, Accuracy, Distance to Base Station, RSSI, SNR 

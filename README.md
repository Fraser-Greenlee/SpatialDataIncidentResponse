# Spatial Data for Incident Response (Cave Rescue)



# Rationale

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations. This provides the opportunity to accurately record these locations and make them readily accessible in advance of incidents occurring, allowing incident controllers access to detailed location information ready for rapid and error-free sharing with team members and other emergency services. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs).

![alt text](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Map.png?raw=true)

# Code
The following script uses data available only for mainland Great Britain, therefore areas outside mainland Great Britain are unsupported.

\
```AugmentLocations.py```

**Dependencies:** Numpy, Pandas, Geopandas, GPXpy, ODF

**Function:**
- ingests APs and RVs recorded in spreadsheets (spreadsheet and QGIS mapping templates are provided)
- APs and RVs - adds accurate spatial conversions from longitude and latitude coordinates to:
  - British National Grid easting and northing
  - Ordnance Survey 1m grid reference
  - What3Words address
  - Google Maps URL (cross-platform app integration)
- RVs - adds metadata:
  - road access type
  - nearest postcode
  - mobile phone coverage for all providers
- exports this information in a variety of useful formats (.csv, .gpkg, .gpx) for serving within online maps, GIS software or on handheld devices

**Example Transformations:**

Inputs:
| ID   | Name           | Longitude | Latitude | VerifiedDate | Notes |
|------|----------------|-----------|----------|--------------|-------|
| AP_1 | Cwmorthin Adit | -3.96894  | 52.99787 | 11/11/21     | Gated |

| ID   | Name                 | Longitude   | Latitude    | VerifiedDate | ParkingType    | Notes                                                                                               |
|------|----------------------|-------------|-------------|--------------|----------------|-----------------------------------------------------------------------------------------------------|
| RV_1 | NWCRO Llanrwst Store | -3.80048028 | 53.13997834 | 07/08/21     | Police Station | Needs police presence |

Outputs:
| Name                  | Notes | Verified | VerifiedDate | Longitude | Latitude | Easting | Northing | OSGridRef1m    | What3Words                   | GoogleMapsURL                                                       |
|-----------------------|-------|----------|--------------|-----------|----------|---------|----------|----------------|------------------------------|---------------------------------------------------------------------|
| Cwmorthin Adit (AP_1) | Gated | True     | 2021-11-11   | -3.96894  | 52.99787 | 267958  | 346317   | SH 67958 46317 | blanking.simulates.processor | https://www.google.com/maps/search/?api=1&query=52.99787%2C-3.96894 |

| Name                        | ParkingType    | Notes                                                                                               | Verified | VerifiedDate | RoadAccessType    | Postcode | MobileCoverage                                          | Longitude   | Latitude    | Easting | Northing | OSGridRef1m    | What3Words           | GoogleMapsURL                                                             |
|-----------------------------|----------------|-----------------------------------------------------------------------------------------------------|----------|--------------|-------------------|----------|---------------------------------------------------------|-------------|-------------|---------|----------|----------------|----------------------|---------------------------------------------------------------------------|
| NWCRO Llanrwst Store (RV_1) | Police Station | Needs police presence | True     | 2021-08-07   | Local Access Road | LL260DF  | EE (Green), Three (Green), Vodafone (Green), O2 (Green) | -3.80048028 | 53.13997834 | 279659  | 361827   | SH 79659 61827 | saying.lousy.elevate | https://www.google.com/maps/search/?api=1&query=53.13997834%2C-3.80048028 |



# Templates

```Mapping.qgz``` - [QGIS](https://qgis.org/en/site/) project containing various web map services for remote mapping

```APs_Master.ods``` - spreadsheet for recording APs

```RVs_Master.ods``` - spreadsheet for recording RVs

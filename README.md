# Spatial Data for Incident Response (Cave Rescue)



# Rationale

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations in addition to locating specific team members best positioned to respond. This provides the opportunity to accurately record these locations and other useful information in advance of incidents occurring and make them readily accessible. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs), and team member locations.



# Code
The follow scripts use data available only for mainland Great Britain, therefore areas outside mainland Great Britain are unsupported. Each Python script contains essential setup instructions that are required prior to use to ensure accuracy and correct function.

\
```AugmentLocations.py```

**Function:**
- ingests APs and RVs recorded in spreadsheets (spreadsheet and QGIS mapping templates are provided)
- adds accurate spatial conversions from longitude and latitude coordinates to:
  - British National Grid easting and northing
  - Ordnance Survey 1m grid reference
  - What3Words address
  - Google Maps URL (cross-platform app integration)
- adds metadata:
  - road access type
  - nearest postcode
  - mobile phone coverage for all providers
- exports this information in a variety of useful formats (.csv, .gpkg, .gpx)

**Example:**

From:
| ID   | Name           | Longitude | Latitude | VerifiedDate | Notes |
|------|----------------|-----------|----------|--------------|-------|
| AP_1 | Cwmorthin Adit | -3.96894  | 52.99787 | 11/11/21     | Gated |

| ID   | Name                 | Longitude   | Latitude    | VerifiedDate | ParkingType    | Notes                                                                                               |
|------|----------------------|-------------|-------------|--------------|----------------|-----------------------------------------------------------------------------------------------------|
| RV_1 | NWCRO Llanrwst Store | -3.80048028 | 53.13997834 | 07/08/21     | Police Station | Needs police presence |

To:
| Name                  | Notes | Verified | VerifiedDate | Longitude | Latitude | Easting | Northing | OSGridRef1m    | What3Words                   | GoogleMapsURL                                                       |
|-----------------------|-------|----------|--------------|-----------|----------|---------|----------|----------------|------------------------------|---------------------------------------------------------------------|
| Cwmorthin Adit (AP_1) | Gated | True     | 2021-11-11   | -3.96894  | 52.99787 | 267958  | 346317   | SH 67958 46317 | blanking.simulates.processor | https://www.google.com/maps/search/?api=1&query=52.99787%2C-3.96894 |

| Name                        | ParkingType    | Notes                                                                                               | Verified | VerifiedDate | RoadAccessType    | Postcode | MobileCoverage                                          | Longitude   | Latitude    | Easting | Northing | OSGridRef1m    | What3Words           | GoogleMapsURL                                                             |
|-----------------------------|----------------|-----------------------------------------------------------------------------------------------------|----------|--------------|-------------------|----------|---------------------------------------------------------|-------------|-------------|---------|----------|----------------|----------------------|---------------------------------------------------------------------------|
| NWCRO Llanrwst Store (RV_1) | Police Station | Needs police presence | True     | 2021-08-07   | Local Access Road | LL260DF  | EE (Green), Three (Green), Vodafone (Green), O2 (Green) | -3.80048028 | 53.13997834 | 279659  | 361827   | SH 79659 61827 | saying.lousy.elevate | https://www.google.com/maps/search/?api=1&query=53.13997834%2C-3.80048028 |

\
```GeolocateAddresses.py```

**Function:**
- ingests team member addresses recorded in a spreadsheet (a spreadsheet template is provided)
- extracts postcodes from the addresses
- adds longitude and latitude coordinates using the postcode, resulting in an approximate location
- exports this information in a variety of useful formats (.csv, .gpkg)

**Example:**

From:
| Name    | Contact      | Notes    | Address                                           |
|---------|--------------|----------|---------------------------------------------------|
| Member1 | PhoneNumber1 | Comment1 | 7 Carno Bettws NP20 7GU                     |

To:
| Info                                               | Longitude         | Latitude         |
|----------------------------------------------------|-------------------|------------------|
| Member1 (Contact: PhoneNumber1 \| Notes: Comment1) | -3.01810699882841 | 51.6077010367438 |



# Templates
```Mapping.qgz``` - [QGIS](https://qgis.org/en/site/) project containing various web map services for remote mapping

```APs_Master.ods``` - spreadsheet for recording APs

```RVs_Master.ods``` - spreadsheet for recording RVs

```TeamMembers_Master.ods``` - spreadsheet for recording team member addresses

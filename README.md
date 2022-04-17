# Spatial Data for Incident Response (Cave Rescue)



### Rationale

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations. This provides the opportunity to accurately record these locations and make them readily accessible in advance of incidents occurring, allowing incident controllers access to detailed location information ready for simple, rapid and error-free sharing with team members and other emergency services. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs).

The free and open source methodology (Great Britain only) below describes how to:
1. **Collate** AP and RV location data from various sources into a simple structured format
2. **Augment** these data with accurate spatial conversions and metadata (listed below)
3. **Serve** the augmented data on a map in a way that the underlying information can be interrogated

Why a cave rescue team would want to use this methodology:
- a structured catalogue of APs and RVs forms the foundation for intelligent incident response planning
- viewing the data on interactive maps with satellite imagery or topographic maps allows incident controllers to view the spatial relationship between APs and RVs to identify what RVs are best positioned for the task at hand
- having multiple pre-calculated spatial conversions that describe the same location facilitates error-free information sharing
- Google Maps URLs allow automated navigation to RVs and provide an accurate assessment of ETA accounting for current road conditions in addition to allowing incident controllers to assess RV suitability on Google Street View if available
- road access type provides an assessment of road accessibility, including identifying restricted access roads which may be gated, at RVs before team members arrive
- mobile phone coverage provides an assessment of available communications at RVs before team members arrive
- the data are exported in a variety of formats for use with mobile and GPS devices, online maps and GIS software
- Google cloud tools (Colaboratory, Drive and Maps) allow users to implement the methodology regardless of their technical experience or hardware and software constraints



### Methodology

![OperationalOverview](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/OperationalOverview.png)

*Data collation (red), augmentation (green) and serving (blue) are the responsibility of a team data controller*
  
1. **Data Collation** - Download and open [```Mapping.qgz```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/Mapping.qgz), a [QGIS](https://qgis.org/en/site/) project containing various web map services for remote location mapping. Generate WGS84 longitude, latitude coordinates for each location and paste them into a downloaded spreadsheet template ([```APs_Master.ods```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/APs_Master.ods) or [```RVs_Master.ods```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/RVs_Master.ods)) depending on the location type, adding additional information and columns as required (these will be unaltered and will carry through)

    ![Coordinates](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Coordinates.png)

    *Extracting longitude, latitude coordinates for a location using right-click with the hand tool selected in QGIS*


2. **Data Augmentation** - Visit [```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb) and follow the instructions to automatically add spatial conversions and metadata to the location records which are exported in a variety of formats (.csv, .gpkg, .gpx) to Google Drive for serving. [```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb) is created for use with [Google Colaboratory](https://colab.research.google.com/), where python code can be run temporarily in the cloud, so no setup is required on your local PC. It runs in a web browser and accesses files hosted on your Google Drive for persistent storage between sessions, and therefore requires a free Google account. The code can also be used on a local PC with a python installation, [Anaconda](https://www.anaconda.com/) is recommended.

    The code uses data available only for Great Britain from the Ordnance Survey (GB postcodes and roads), therefore areas outside Great Britain are unsupported.

    - Spatial conversions (APs and RVs)
        - Longitude - Decimal degrees (WGS84)
        - Latitude - Decimal degrees (WGS84)
        - Easting - Metres (British National Grid)
        - Northing - Metres (British National Grid)
        - OSGridRef1m - Ordnance Survey 1m grid reference
        - What3Words - What3Words address
        - GoogleMapsURL - Google Maps URL for directions and Street View
    - Metadata (RVs only)
        - RoadAccessType - Nearest road access type (within 50 m)
        - Postcode - Nearest postcode (within 300 m)
        - MobileCoverage - Minimum outdoor mobile phone coverage for all providers at buildings within a postcode



3. **Data Serving** - serve the exported files according to your requirements, examples are shown below

    - **Google Maps** (reads files from Google Drive; private online access)

      ![Google Maps](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Google.png)

    - **QGIS** (can ingest any spatial data format; local PC only)

      ![QGIS](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/QGIS.png)


    - **Mobile / GPS Device** (uses .gpx files for import; offline navigation and data access)

      ![Mobile](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Mobile.png)

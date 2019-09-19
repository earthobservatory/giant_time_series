# GIAnT Time Series
GIAnT time series processing of ISCEv2 interferograms

![pipeline](https://user-images.githubusercontent.com/387300/46752714-ca77ff80-cc72-11e8-99f6-502eaa954670.png)

## HySDS Cluster Installation
1. Log into your `mozart` instance.
1. Download HySDS package from the [latest release](https://github.com/hysds/giant_time_series/releases/latest) (replace \<version\>):
   ```
   wget https://github.com/hysds/giant_time_series/releases/download/<version>/container-hysds_giant_time_series.<version>.sdspkg.tar
   ```
1. Import HySDS package:
   ```
   sds pkg import container-hysds_giant_time_series.<version>.sdspkg.tar
   ```
1. Add datasets config for `filtered-ifg-stack`, `filtered-gunw-merged-stack`, and `displacement-time-series` to your *datasets.json* templates 
under *~/.sds/files* on `mozart`. Example config entries can be found [here](conf/datasets.json).
1. On `mozart`, recreate the code/config bundles and ship:
   ```
   sds ship
   ```

## Filtered Interferogram Stack
### Description
The filtered interferogram (`IFG`) stack datasets (`filtered-ifg-stack`) and (`filtered-gunw-merged-stack`) are primarily the HDF5 `RAW-STACK.h5` and 
`PROC-STACK.h5` outputs of GIAnT's `PrepIgramStack.py` and `ProcessStack.py`, respectively. Prior to
running these PGEs, a first-order filtering step is performed to filter out IFGs whose track and subswaths
don't match those specified. Additionally, IFGs are filtered whose reference bounding box contains no data
that pass the coherence threshold or which do not cover the region of interest.

### Outputs
- `RAW-STACK.h5.gz` - gzip-compressed HDF5 file of the filtered stack of IFGs
- `PROC-STACK.h5.gz` - gzip-compressed HDF5 file of the filtered stack of IFGs with atmospheric and orbit corrections applied
- `browse.png` - visual browse of temporal connectivity
- `gaps.txt` - record of any temporal gaps detected in the stack
- `create_filtered_ifg_stack.log` - verbose log which can be used to determine what IFGs were filtered and why
- `filt_info.pkl` - pickle file containing IFG and filter information
- `data.xml`, `sbas.xml` - other inputs needed by downstream displacement time series PGEs

### Usage
1. In `tosca` interface, draw bounding box on the region of interest.
1. Facet on the `S1-IFG` dataset.
1. Facet on the `track number`.
1. Facet on the `subswath`.
1. Facet on the `dataset version`.
1. Click on `On-Demand`.
1. For `Action`, select `GIAnT - Create filtered single scene IFG stack [\<version\>].
1. In the parameters section below, ensure `track` and `subswath` matches the track and subswath you initially faceted on. This ensures that `S1-IFG` products for other tracks and subswaths are filtered out in case the user failed to facet down to them.
1. Populate `ref_point`.
1. Adjust other parameters accordingly.
1. Click `Process Now`.

## Filtered GUNW Merged Stack
### Usage
1. In `tosca` interface, draw bounding box on the region of interest.
1. Facet on the `S1-GUNW-MERGED` dataset.
1. Facet on the `dataset version` (v2.0.2).
1. Facet on the `track number`.
1. Click on `On-Demand`.
1. For `Action`, select `GIAnT - Create filtered GUNW-MERGED stack [\<version\>].
1. In the parameters section below, ensure `track` matches the track you initially faceted on. This ensures that `S1-GUNW-MERGED` products for other tracksare filtered out in case the user failed to facet down to them.
1. Populate `ref_point`.
1. Adjust other parameters accordingly.
1. Click `Process Now`.

## Displacement Time Series
### Description
The displacement time series dataset (`displacement-time-series`) is primarily the 
HDF5 `LS-PARAMS.h5` (for SBAS-inversion) and `NSBAS-PARAMS.h5` (for NSBAS-inversion)
outputs of GIAnT's `SBASInvertWrapper.py` and `NSBASInvertWrapper.py`, respectively.

### Outputs
- `LS-PARAMS.h5.gz` or `NSBAS-PARAMS.h5.gz`- gzip-compressed HDF5 file of the displacement time series produced via the SBAS or NSBAS inversion method
- `browse.png` - visual browse of initial time series step

### Create displacement time series
1. In `tosca` interface, draw bounding box on the region of interest.
1. Facet on the `filtered-ifg-stack` dataset.
1. Click on `On-Demand`.
1. For `Action`, select `GIAnT - Create Displacement Time Series [\<version\>].
1. In the parameters section below, select the inversion `method`: `sbas` or `nsbas`.
1. Click `Process Now`.

### Visualization
#### Option 1: Panoply
1. Open HDF5 in `Panoply`: File->Open.
1. Double click on `rawts` (raw time series) or `recons` (reconstructed time series) variable.
1. Select `Create a georeferenced Longitude-Latitude plot`. Click on `Create`.
1. Zoom in to the region of interest. On MacOSX, hold down the `command` key while you click and drag a bounding box over the region of interest.
1. Click on the `Scale` tab and set `Scale Range Min.` to `-100` and `Max.` to `100`. You can play around with the values.
1. Click on the `Arrays` tab and cycle through the time slices by clicking the `up` arrow button.
![panoply](https://user-images.githubusercontent.com/387300/46819763-666c3e80-cd39-11e8-8b0b-74325014b4a3.gif)

#### Option 2: Leaflet server
If a leaflet time-series server is made available to you, you may visualize your time-series dataset by ingesting it into the server.
1. In the `tosca` interface, facet on the specific `time-series` dataset you would like to visualize on the map.
1. Click `On-Demand`.
1. For `Action`, select `Displacement Time Series Ingest`
1. For `Queue`, select `ts-ingest`
1. In the parameters section below, select:
    1. `thredds_data_dir` - the leaflet-servers thredds directory location to ingest time-series data
    1. `leaflet_url` - the url which the leaflet server is hosted
1. Click `Process Now`.
1. After job submission, a `Visualize` button will appear in `tosca` for your time-series dataset: <img src="https://user-images.githubusercontent.com/6346909/51800817-1d041880-2270-11e9-9a22-691927bad7df.png" width="350" class="centre">
1. Clicking on it will bering you to the ingested time-series in leaflet:
![leaflet-server](https://user-images.githubusercontent.com/6346909/51800988-ed0a4480-2272-11e9-8255-5afcaf3e2d86.gif)

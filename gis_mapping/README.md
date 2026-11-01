# Film Locations Explorer

An interactive GIS website for the CSE 310 `gis_mapping` assignment. It uses Leaflet, Leaflet.markercluster, and the supplied location datasets. The map loads every location with a direct film association (`productions > 0`) from `filming-locations.geojson`; this currently produces 4,481 mapped locations.

## Run it

Because browsers block `fetch()` from local `file://` pages, start a small local server from this folder:

```powershell
cd C:\Users\hlyco\CSE310\gis_mapping
py -m http.server 8000
```

Then open <http://localhost:8000>.

## Assignment requirements

1. Street and light basemaps are available through the layer control.
2. All 4,481 locations with a direct film association are displayed; marker clustering keeps the map responsive and expands into individual pins as you zoom in.
3. Marker data is loaded from `filming-locations.geojson` and includes the location name, country, category, coordinates, description, production titles, and film-association count. `filming-locations.csv` contains the same location records in tabular form; `productions.csv` is the film-level source used to derive the associations.
4. Clicking a marker or a location in the sidebar displays its stored information.
5. The page title is **Film Locations Explorer**.

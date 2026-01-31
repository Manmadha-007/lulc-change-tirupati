import { GeoJSON, Pane } from "react-leaflet";

const WORLD_BOUNDS = [
  [-180, -90],
  [180, -90],
  [180, 90],
  [-180, 90],
  [-180, -90],
];

export default function AOIMask({ aoi }) {
  // 1. Guard Clause: If aoi is null or undefined, don't render anything
  // This prevents the "Cannot read properties of undefined (reading 'type')" error
  if (!aoi || !aoi.geometry) {
    return null;
  }

  // 2. Safely extract coordinates based on Polygon vs MultiPolygon
  let aoiRing;
  try {
    aoiRing = aoi.geometry.type === "Polygon" 
      ? aoi.geometry.coordinates[0] 
      : aoi.geometry.coordinates[0][0];
  } catch (err) {
    console.error("Invalid GeoJSON structure", err);
    return null;
  }

  const maskFeature = {
    type: "Feature",
    geometry: {
      type: "Polygon",
      coordinates: [
        WORLD_BOUNDS, 
        [...aoiRing].reverse() // Winding order for the spotlight hole
      ],
    },
  };

  return (
    <Pane name="maskPane" style={{ zIndex: 450 }}>
      <GeoJSON
        key={JSON.stringify(aoi.geometry.coordinates[0][0])} // Helps React track changes
        data={maskFeature}
        style={{
          fillColor: "#000",
          fillOpacity: 0.7,
          stroke: false,
        }}
        interactive={false}
      />
    </Pane>
  );
}
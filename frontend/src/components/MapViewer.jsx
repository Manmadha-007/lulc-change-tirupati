import React, { useState, useRef } from 'react';
import { MapContainer, TileLayer, ZoomControl, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import LayerControl from './LayerControl';
import { fetchPixelValue } from '../services/api';

// Fix Leaflet's default icon path issues with Webpack/Vite
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const LULC_COLORS = {
    'Forest': 'rgb(0, 100, 0)',
    'Water': 'rgb(0, 0, 255)',
    'Agriculture': 'rgb(255, 255, 0)',
    'Barren': 'rgb(165, 42, 42)',
    'Built-up': 'rgb(255, 0, 0)',
};

const MapViewer = ({ activeLayer, onLayerChange }) => {
    const tirupatiCenter = [13.6288, 79.4192];

    // Layer State: Managed by Parent (Dashboard)
    // Opacity removed as per request

    // Tooltip State
    const [tooltipPos, setTooltipPos] = useState(null); // { x, y }
    const [tooltipData, setTooltipData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    // Data Fetching Ref
    const lastFetchRef = useRef(0);

    const fetchPixelData = async (lat, lng) => {
        setIsLoading(true);
        try {
            const data = await fetchPixelValue(lat, lng);
            setTooltipData(data);
        } catch (err) {
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleMouseMove = async (e) => {
        // Update position IMMEDIATELY for smoothness
        setTooltipPos(e.containerPoint);

        const now = Date.now();
        // Throttle API calls (e.g., every 100ms)
        if (now - lastFetchRef.current > 100) {
            lastFetchRef.current = now;
            fetchPixelData(e.latlng.lat, e.latlng.lng);
        }
    };

    const handleMouseOut = () => {
        setTooltipPos(null);
        setTooltipData(null);
    }

    // Helper to check if pixel is valid (not "No Data" / "Unknown")
    const isValidPixel = (data) => {
        return data &&
            data['2018']?.class_name !== 'No Data' &&
            data['2018']?.class_name !== 'Unknown';
    };

    return (
        <div className="relative w-full h-full bg-gray-100 overflow-hidden">
            <MapContainer
                center={tirupatiCenter}
                zoom={12}
                className="w-full h-full z-0 cursor-crosshair"
                zoomControl={false}
            // Default dragging enabled
            >
                <ZoomControl position="bottomright" />

                {/* CartoDB Positron (Light) Base Map */}
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                />

                {/* Overlays - Mutually Exclusive */}
                {activeLayer === 'lulc2018' && (
                    <TileLayer
                        url="/tiles/lulc_2018/{z}/{x}/{y}.png"
                        opacity={0.7} // Fixed opacity
                        tms={false}
                    />
                )}

                {activeLayer === 'lulc2023' && (
                    <TileLayer
                        url="/tiles/lulc_2023/{z}/{x}/{y}.png"
                        opacity={0.7} // Fixed opacity
                    />
                )}

                {activeLayer === 'change' && (
                    <TileLayer
                        url="/tiles/change_map/{z}/{x}/{y}.png"
                        opacity={0.7} // Fixed opacity
                    />
                )}

                <MapHoverEvents
                    onMouseMove={handleMouseMove}
                    onMouseOut={handleMouseOut}
                />

            </MapContainer>

            {/* Custom Tooltip Overlay - ONLY show if Valid Pixel (Prevents "Scanning" flash outside ROI) */}
            {tooltipPos && isValidPixel(tooltipData) && (
                <div
                    className="absolute pointer-events-none z-[2000] bg-white/95 backdrop-blur-sm p-3 rounded-xl shadow-xl border border-white/50 ring-1 ring-black/5 flex flex-col gap-2 transition-transform duration-75 ease-out -translate-x-1/2 -translate-y-[100%] mb-4"
                    style={{
                        top: tooltipPos.y - 20, // Offset to be fully above cursor
                        left: tooltipPos.x,
                        minWidth: '220px'
                    }}
                >
                    {/* Triangle Arrow */}
                    <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white/95 border-r border-b border-gray-200 rotate-45 shadow-[2px_2px_2px_-1px_rgba(0,0,0,0.05)]"></div>

                    <div className="flex items-center justify-between border-b border-gray-200 pb-2 mb-1">
                        <span className="text-xs font-bold uppercase text-gray-500 tracking-wider">Pixel Details</span>
                        {isLoading && <span className="animate-pulse w-2 h-2 bg-blue-500 rounded-full"></span>}
                    </div>

                    {tooltipData && isValidPixel(tooltipData) ? (
                        <div className="grid grid-cols-2 gap-3 text-sm">
                            <div>
                                <span className="text-[10px] font-bold text-gray-400 uppercase block mb-0.5">2018</span>
                                <div className="flex items-center gap-2">
                                    {tooltipData['2018']?.class_name && (
                                        <div
                                            className="w-3 h-3 rounded-full border border-black/10 shadow-sm"
                                            style={{ backgroundColor: LULC_COLORS[tooltipData['2018']?.class_name] || '#ccc' }}
                                        />
                                    )}
                                    <span className="font-semibold text-gray-800 block leading-tight">{tooltipData['2018']?.class_name || 'N/A'}</span>
                                </div>
                                <span className="text-[10px] text-gray-500 block">
                                    {(tooltipData['2018']?.confidence * 100)?.toFixed(1)}% Conf
                                </span>
                            </div>

                            <div className="border-l border-gray-200 pl-3">
                                <span className="text-[10px] font-bold text-gray-400 uppercase block mb-0.5">2023</span>
                                <div className="flex items-center gap-2">
                                    {tooltipData['2023']?.class_name && (
                                        <div
                                            className="w-3 h-3 rounded-full border border-black/10 shadow-sm"
                                            style={{ backgroundColor: LULC_COLORS[tooltipData['2023']?.class_name] || '#ccc' }}
                                        />
                                    )}
                                    <span className="font-semibold text-gray-800 block leading-tight">{tooltipData['2023']?.class_name || 'N/A'}</span>
                                </div>
                                <span className="text-[10px] text-gray-500 block">
                                    {(tooltipData['2023']?.confidence * 100)?.toFixed(1)}% Conf
                                </span>
                            </div>

                            {tooltipData['2018']?.class_id !== tooltipData['2023']?.class_id && (
                                <div className="col-span-2 mt-1 bg-gradient-to-r from-yellow-50 to-orange-50 text-orange-700 text-xs px-2 py-1.5 rounded-lg border border-orange-100 flex items-center justify-center font-bold shadow-sm">
                                    Change Detected ⚠️
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="py-2 text-center text-gray-400 text-xs italic">
                            Scanning...
                        </div>
                    )}
                </div>
            )}

            {/* Layer Control Panel */}
            <LayerControl
                activeLayer={activeLayer}
                onLayerChange={onLayerChange}
            />
        </div>
    );
};

// Helper component for map events
const MapHoverEvents = ({ onMouseMove, onMouseOut }) => {
    useMapEvents({
        mousemove: (e) => {
            onMouseMove(e);
        },
        mouseout: () => {
            onMouseOut();
        }
    });
    return null;
};

export default MapViewer;

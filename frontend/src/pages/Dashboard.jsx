import React, { useState } from 'react';
import MapViewer from '../components/MapViewer';
import Statistics from '../components/Statistics';

const Dashboard = () => {
    const [activeLayer, setActiveLayer] = useState('lulc2018');

    return (
        <div className="w-full h-full flex flex-col md:flex-row">
            <div className="flex-1 relative h-[60vh] md:h-full z-0">
                <MapViewer activeLayer={activeLayer} onLayerChange={setActiveLayer} />
            </div>

            <div className="w-full md:w-[400px] bg-white border-l border-gray-200 h-[40vh] md:h-full overflow-hidden flex flex-col z-10 shadow-xl">
                <Statistics />
            </div>
        </div>
    );
};

export default Dashboard;

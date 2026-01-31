import React from 'react';

const LULC_CLASSES = [
    { id: 1, name: 'Forest', color: 'rgb(0, 100, 0)' },
    { id: 2, name: 'Water', color: 'rgb(0, 0, 255)' },
    { id: 3, name: 'Agriculture', color: 'rgb(255, 255, 0)' },
    { id: 4, name: 'Barren', color: 'rgb(165, 42, 42)' },
    { id: 5, name: 'Built-up', color: 'rgb(255, 0, 0)' },
];

const LayerControl = ({
    activeLayer,
    onLayerChange
}) => {
    return (
        <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-md text-gray-800 p-4 rounded-xl shadow-lg z-[1000] min-w-[200px] border border-white/50 ring-1 ring-black/5 transition-all hover:bg-white/95">
            <h3 className="font-bold mb-3 text-sm border-b border-gray-100 pb-2 text-gray-900 tracking-tight flex items-center justify-between">
                <span>Map Layers</span>
            </h3>

            <div className="space-y-2 mb-4">
                {/* Radio Buttons Layer Toggles */}

                {/* LULC 2018 */}
                <div className="flex items-center justify-between group cursor-pointer" onClick={() => onLayerChange('lulc2018')}>
                    <div className="flex items-center space-x-2">
                        <div className={`w-4 h-4 rounded-full border flex items-center justify-center transition-all ${activeLayer === 'lulc2018' ? 'border-blue-600' : 'border-gray-300 group-hover:border-blue-400'}`}>
                            {activeLayer === 'lulc2018' && <div className="w-2 h-2 bg-blue-600 rounded-full" />}
                        </div>
                        <span className={`text-sm font-medium transition-colors ${activeLayer === 'lulc2018' ? 'text-blue-700' : 'text-gray-700 group-hover:text-gray-900'}`}>LULC 2018</span>
                    </div>
                </div>

                {/* LULC 2023 */}
                <div className="flex items-center justify-between group cursor-pointer" onClick={() => onLayerChange('lulc2023')}>
                    <div className="flex items-center space-x-2">
                        <div className={`w-4 h-4 rounded-full border flex items-center justify-center transition-all ${activeLayer === 'lulc2023' ? 'border-blue-600' : 'border-gray-300 group-hover:border-blue-400'}`}>
                            {activeLayer === 'lulc2023' && <div className="w-2 h-2 bg-blue-600 rounded-full" />}
                        </div>
                        <span className={`text-sm font-medium transition-colors ${activeLayer === 'lulc2023' ? 'text-blue-700' : 'text-gray-700 group-hover:text-gray-900'}`}>LULC 2023</span>
                    </div>
                </div>

                {/* Change Map */}
                <div className="flex items-center justify-between group cursor-pointer" onClick={() => onLayerChange('change')}>
                    <div className="flex items-center space-x-2">
                        <div className={`w-4 h-4 rounded-full border flex items-center justify-center transition-all ${activeLayer === 'change' ? 'border-blue-600' : 'border-gray-300 group-hover:border-blue-400'}`}>
                            {activeLayer === 'change' && <div className="w-2 h-2 bg-blue-600 rounded-full" />}
                        </div>
                        <span className={`text-sm font-medium transition-colors ${activeLayer === 'change' ? 'text-blue-700' : 'text-gray-700 group-hover:text-gray-900'}`}>Change Map</span>
                    </div>
                </div>

            </div>

            <h3 className="font-bold mb-2 text-[10px] uppercase text-gray-400 tracking-wider">Legend</h3>
            <div className="space-y-1.5">
                {LULC_CLASSES.map((cls) => (
                    <div key={cls.id} className="flex items-center space-x-2">
                        <span
                            className="w-2.5 h-2.5 rounded-full block shadow-sm ring-1 ring-black/5"
                            style={{ backgroundColor: cls.color }}
                        ></span>
                        <span className="text-xs text-gray-600 font-medium">{cls.name}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LayerControl;

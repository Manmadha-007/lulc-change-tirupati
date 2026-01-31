import React, { useEffect, useState } from 'react';
import { fetchSummary } from '../services/api';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    PieChart, Pie, Cell
} from 'recharts';

const COLORS = {
    "Forest": "#15803d",      // green-700
    "Water": "#3b82f6",       // blue-500
    "Agriculture": "#eab308", // yellow-500
    "Barren": "#a8a29e",      // stone-400 (Brownish grey)
    "Built-up": "#ef4444",    // red-500
    "Unknown": "#cbd5e1"
};

const Statistics = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadStats = async () => {
            try {
                // Fetch basic summary
                const stats = await fetchSummary();
                const chartData = Object.keys(stats).map(key => ({
                    name: key,
                    '2018': stats[key].area_2018_sq_km,
                    '2023': stats[key].area_2023_sq_km,
                    ...stats[key]
                }));
                setData(chartData);
            } catch (error) {
                console.error("Failed to load stats", error);
            } finally {
                setLoading(false);
            }
        };
        loadStats();
    }, []);

    if (loading) return <div className="p-4 text-gray-600 text-sm animate-pulse">Loading stats...</div>;

    return (
        <div className="bg-white/95 backdrop-blur rounded-xl p-5 text-gray-800 h-full overflow-auto shadow-xl border border-white/50 ring-1 ring-black/5 scrollbar-thin scrollbar-thumb-gray-300">
            <h2 className="text-lg font-bold mb-6 text-gray-900 border-b border-gray-100 pb-2">LULC Analytics (2018-2023)</h2>

            {/* Area Comparison Bar Chart */}
            <div className="mb-8 p-4 bg-gray-50 rounded-xl border border-gray-100">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Area Comparison (Sq. Km)</h3>
                <div className="h-[250px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                            data={data}
                            margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
                            <XAxis dataKey="name" stroke="#9ca3af" tick={{ fontSize: 12 }} />
                            <YAxis stroke="#9ca3af" tick={{ fontSize: 12 }} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#ffffff', border: 'none', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                                cursor={{ fill: '#f3f4f6' }}
                            />
                            <Legend wrapperStyle={{ paddingTop: '10px' }} />
                            <Bar dataKey="2018" fill="#818cf8" name="2018" radius={[4, 4, 0, 0]} />
                            <Bar dataKey="2023" fill="#34d399" name="2023" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Distribution Pie Charts - Stacked for better visibility in compact sidebar */}
            <div className="mb-8 grid grid-cols-1 gap-6">
                {/* 2018 Chart */}
                <div className="p-4 bg-gray-50 rounded-xl border border-gray-100 flex flex-col items-center">
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">2018 Distribution</h3>
                    <div className="h-[220px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={data}
                                    dataKey="2018"
                                    nameKey="name"
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={50}
                                    outerRadius={80} // Increased size
                                    paddingAngle={2}
                                >
                                    {data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#94a3b8'} stroke="none" />
                                    ))}
                                </Pie>
                                <Tooltip
                                    formatter={(value) => `${value.toFixed(2)} sq km`}
                                    contentStyle={{ backgroundColor: '#ffffff', border: 'none', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                                />
                                <Legend layout="horizontal" verticalAlign="bottom" align="center" wrapperStyle={{ fontSize: '11px' }} iconSize={10} />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* 2023 Chart */}
                <div className="p-4 bg-gray-50 rounded-xl border border-gray-100 flex flex-col items-center">
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">2023 Distribution</h3>
                    <div className="h-[220px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={data}
                                    dataKey="2023"
                                    nameKey="name"
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={50}
                                    outerRadius={80} // Increased size
                                    paddingAngle={2}
                                >
                                    {data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#94a3b8'} stroke="none" />
                                    ))}
                                </Pie>
                                <Tooltip
                                    formatter={(value) => `${value.toFixed(2)} sq km`}
                                    contentStyle={{ backgroundColor: '#ffffff', border: 'none', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                                />
                                <Legend layout="horizontal" verticalAlign="bottom" align="center" wrapperStyle={{ fontSize: '10px' }} iconSize={8} />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Change Summary Cards */}
            <div className="space-y-4">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">Net Change Summary</h3>
                <div className="grid grid-cols-1 gap-3">
                    {data.map((item) => (
                        <div key={item.name} className="bg-white p-3 rounded-xl border border-gray-100 shadow-sm flex items-center justify-between hover:shadow-md transition-all group">
                            <div className="flex items-center gap-3">
                                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[item.name] || '#94a3b8' }}></span>
                                <span className="font-medium text-gray-700 text-sm">{item.name}</span>
                            </div>
                            <div className="text-right">
                                <div className={`text-sm font-bold ${item.percent_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                    {item.percent_change > 0 ? '+' : ''}{item.percent_change}%
                                </div>
                                <div className="text-xs text-gray-400 font-medium">
                                    {item.net_change_sq_km > 0 ? '+' : ''}{item.net_change_sq_km.toFixed(2)} sq km
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Downloads */}
            <div className="mt-8 border-t border-gray-100 pt-6">
                <div className="flex gap-3">
                    <a
                        href="/api/summary"
                        download="summary_stats.json"
                        target="_blank"
                        className="flex-1 bg-gray-900 hover:bg-black text-white text-xs font-bold py-2.5 px-4 rounded-lg transition-all shadow-sm text-center tracking-wide"
                    >
                        Download Report
                    </a>
                    <a
                        href="/api/transition-matrix"
                        download="transition_matrix.json"
                        target="_blank"
                        className="flex-1 bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 text-xs font-bold py-2.5 px-4 rounded-lg transition-all shadow-sm text-center tracking-wide"
                    >
                        Transition Matrix
                    </a>
                </div>
            </div>
        </div>
    );
};

export default Statistics;

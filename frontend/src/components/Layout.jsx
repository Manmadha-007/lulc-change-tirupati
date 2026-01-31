import React from 'react';
import { Outlet } from 'react-router-dom';

const Layout = () => {
    return (
        <div className="flex h-screen w-screen bg-gray-50 text-gray-900">
            <div className="flex flex-col flex-1 h-full relative">
                {/* Header removed as per user request */}
                <main className="flex-1 relative overflow-auto">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;

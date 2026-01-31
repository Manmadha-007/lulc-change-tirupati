import axios from 'axios';

const api = axios.create({
    baseURL: '/api', // Proxy handles the target
    headers: {
        'Content-Type': 'application/json',
    },
});

export const fetchSummary = async () => {
    try {
        const response = await api.get('/summary');
        return response.data;
    } catch (error) {
        console.error('Error fetching summary stats:', error);
        throw error;
    }
};

export const fetchTransitionMatrix = async () => {
    try {
        const response = await api.get('/transition-matrix');
        return response.data;
    } catch (error) {
        console.error('Error fetching transition matrix:', error);
        throw error;
    }
};

export const fetchPixelValue = async (lat, lon) => {
    try {
        const response = await api.get(`/pixel?lat=${lat}&lon=${lon}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching pixel value:', error);
        throw error;
    }
};

export default api;

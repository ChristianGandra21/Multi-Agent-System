import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const researchService = {
    createResearch: async (query: string) => {
        const response = await api.post('/research', { query });
        return response.data;
    },

    getResearchStatus: async (id: number) => {
        const response = await api.get(`/research/${id}`);
        return response.data;
    }
}

export default api;
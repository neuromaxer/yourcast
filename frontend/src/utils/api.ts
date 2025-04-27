import axios from 'axios';

const API_BASE_URL = 'http://0.0.0.0:8081';

export const generatePodcast = async (data: {
  length: string;
  tone: string;
  style: string;
  data_sample: any[];
}) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate-podcast`, data, {
      responseType: 'blob',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error generating podcast:', error);
    throw error;
  }
};
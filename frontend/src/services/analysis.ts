import api from './api';
import { FullAnalysisResponse, ImageUploadResponse } from '../types';

export const analysisService = {
  async uploadImage(file: File): Promise<ImageUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post<ImageUploadResponse>('/analysis/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  async analyzeImage(sessionId: string): Promise<FullAnalysisResponse> {
    const response = await api.post<FullAnalysisResponse>(`/analysis/${sessionId}/analyze`);
    return response.data;
  },

  async getAnalysis(sessionId: string): Promise<FullAnalysisResponse> {
    const response = await api.get<FullAnalysisResponse>(`/analysis/${sessionId}`);
    return response.data;
  }
};

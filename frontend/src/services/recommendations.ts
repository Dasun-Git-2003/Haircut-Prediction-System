import api from './api';
import { RecommendationResponse, UserPreferences, RecommendationResult } from '../types';

export const recommendationsService = {
  async getRecommendations(analysisId: string, preferences?: UserPreferences): Promise<RecommendationResponse> {
    const response = await api.post<RecommendationResponse>(`/recommendations/${analysisId}`, preferences || {});
    return response.data;
  },

  async getRecommendationDetails(analysisId: string): Promise<RecommendationResult[]> {
    const response = await api.get<RecommendationResult[]>(`/recommendations/${analysisId}`);
    return response.data;
  }
};

import api from './api';
import { TryOnResponse } from '../types';

export const tryOnService = {
  async generateTryOn(recommendationId: string): Promise<TryOnResponse> {
    const response = await api.post<TryOnResponse>(`/try-on/${recommendationId}`);
    return response.data;
  },

  async getTryOnResult(id: string): Promise<TryOnResponse> {
    const response = await api.get<TryOnResponse>(`/try-on/${id}`);
    return response.data;
  }
};

import api from './api';
import { Hairstyle, HairstyleListResponse } from '../types';

export const hairstylesService = {
  async getHairstyles(params?: any): Promise<HairstyleListResponse> {
    const response = await api.get<HairstyleListResponse>('/hairstyles', { params });
    return response.data;
  },

  async getHairstyle(id: string): Promise<Hairstyle> {
    const response = await api.get<Hairstyle>(`/hairstyles/${id}`);
    return response.data;
  },

  async createHairstyle(data: Partial<Hairstyle>): Promise<Hairstyle> {
    const response = await api.post<Hairstyle>('/hairstyles', data);
    return response.data;
  },

  async updateHairstyle(id: string, data: Partial<Hairstyle>): Promise<Hairstyle> {
    const response = await api.put<Hairstyle>(`/hairstyles/${id}`, data);
    return response.data;
  },

  async deleteHairstyle(id: string): Promise<void> {
    await api.delete(`/hairstyles/${id}`);
  }
};

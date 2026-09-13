import api from './api';
import { Favorite } from '../types';

export const favoritesService = {
  async getFavorites(): Promise<Favorite[]> {
    const response = await api.get<Favorite[]>('/favorites');
    return response.data;
  },

  async addFavorite(data: { hairstyle_id: string }): Promise<Favorite> {
    const response = await api.post<Favorite>('/favorites', data);
    return response.data;
  },

  async removeFavorite(id: string): Promise<void> {
    await api.delete(`/favorites/${id}`);
  }
};

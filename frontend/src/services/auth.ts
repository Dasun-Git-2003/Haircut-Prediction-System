import api from './api';
import { User, UserLogin, UserRegister, Token } from '../types';

export const authService = {
  async register(data: UserRegister): Promise<User> {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },

  async login(data: UserLogin): Promise<Token> {
    const formData = new URLSearchParams();
    formData.append('username', data.email);
    if (data.password) formData.append('password', data.password);
    
    const response = await api.post<Token>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  logout(): void {
    localStorage.removeItem('token');
  }
};

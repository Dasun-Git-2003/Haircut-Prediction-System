import { useState } from 'react';
import { FullAnalysisResponse, RecommendationResult, UserPreferences } from '../types';
import { analysisService } from '../services/analysis';
import { recommendationsService } from '../services/recommendations';

export type AnalysisStep = 'upload' | 'analyzing' | 'preferences' | 'results' | 'tryon';

export const useAnalysis = () => {
  const [currentStep, setCurrentStep] = useState<AnalysisStep>('upload');
  const [analysisData, setAnalysisData] = useState<FullAnalysisResponse | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationResult[]>([]);
  const [selectedHairstyle, setSelectedHairstyle] = useState<RecommendationResult | null>(null);

  const startAnalysis = async (file: File) => {
    try {
      setCurrentStep('analyzing');
      const uploadRes = await analysisService.uploadImage(file);
      const data = await analysisService.analyzeImage(uploadRes.session_id);
      setAnalysisData(data);
      setCurrentStep('preferences');
    } catch (error) {
      console.error(error);
      setCurrentStep('upload');
      throw error;
    }
  };

  const setPreferences = async (preferences?: UserPreferences) => {
    if (!analysisData) return;
    try {
      setCurrentStep('results'); // optimistic
      const data = await recommendationsService.getRecommendations(analysisData.id, preferences);
      setRecommendations(data.recommendations);
    } catch (error) {
      console.error(error);
      throw error;
    }
  };

  const selectHairstyle = (hairstyle: RecommendationResult) => {
    setSelectedHairstyle(hairstyle);
    setCurrentStep('tryon');
  };

  return {
    currentStep,
    setCurrentStep,
    analysisData,
    recommendations,
    selectedHairstyle,
    startAnalysis,
    setPreferences,
    selectHairstyle
  };
};

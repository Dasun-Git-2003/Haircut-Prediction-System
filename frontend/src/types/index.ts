export interface User {
  id: string;
  username: string;
  email: string;
  is_admin: boolean;
  created_at: string;
}

export interface UserRegister {
  username: string;
  email: string;
  password?: string;
}

export interface UserLogin {
  email: string;
  password?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export enum FaceShape {
  OVAL = 'oval',
  ROUND = 'round',
  SQUARE = 'square',
  HEART = 'heart',
  DIAMOND = 'diamond',
  OBLONG = 'oblong',
}

export enum HairType {
  STRAIGHT = 'straight',
  WAVY = 'wavy',
  CURLY = 'curly',
  COILY = 'coily',
}

export enum HairLength {
  VERY_SHORT = 'very_short',
  SHORT = 'short',
  MEDIUM = 'medium',
  LONG = 'long',
}

export enum HairDensity {
  THIN = 'thin',
  MEDIUM = 'medium',
  THICK = 'thick',
}

export enum HairVolume {
  FLAT = 'flat',
  MEDIUM = 'medium',
  VOLUMINOUS = 'voluminous',
}

export enum MaintenanceLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
}

export enum StyleTag {
  CLASSIC = 'classic',
  MODERN = 'modern',
  PROFESSIONAL = 'professional',
  CASUAL = 'casual',
  TRENDY = 'trendy',
  EDGY = 'edgy',
}

export enum LifestyleTag {
  OFFICE = 'office',
  UNIVERSITY = 'university',
  EVERYDAY = 'everyday',
  FORMAL = 'formal',
  SPORTY = 'sporty',
}

export enum AnalysisStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export interface FaceAnalysisResult {
  face_shape: FaceShape;
  confidence: number;
}

export interface HairAnalysisResult {
  hair_type: HairType;
  hair_length: HairLength;
  hair_density: HairDensity;
  confidence: number;
}

export interface FullAnalysisResponse {
  id: string;
  status: AnalysisStatus;
  face_analysis?: FaceAnalysisResult;
  hair_analysis?: HairAnalysisResult;
  image_url: string;
  created_at: string;
}

export interface Hairstyle {
  id: string;
  name: string;
  description: string;
  image_url: string;
  suitable_face_shapes: FaceShape[];
  suitable_hair_types: HairType[];
  maintenance_level: MaintenanceLevel;
  style_tags: StyleTag[];
  category: string;
}

export interface HairstyleListResponse {
  items: Hairstyle[];
  total: number;
  page: number;
  size: number;
}

export interface UserPreferences {
  preferred_length?: HairLength[];
  maintenance?: MaintenanceLevel[];
  style?: StyleTag[];
  lifestyle?: LifestyleTag[];
  haircut_category?: string[];
}

export interface RecommendationResult {
  hairstyle: Hairstyle;
  match_score: number;
  reasons: string[];
}

export interface RecommendationResponse {
  analysis_id: string;
  recommendations: RecommendationResult[];
}

export interface TryOnRequest {
  recommendation_id: string;
}

export interface TryOnResponse {
  id: string;
  original_image_url: string;
  generated_image_url: string;
  status: string;
}

export interface Favorite {
  id: string;
  hairstyle_id: string;
  user_id: string;
  created_at: string;
  hairstyle?: Hairstyle;
}

export interface ImageUploadResponse {
  session_id: string;
  image_url: string;
}

export interface ErrorResponse {
  detail: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

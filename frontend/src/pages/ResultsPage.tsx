import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import StyleProfile from '../components/recommendations/StyleProfile';
import RecommendationCard from '../components/recommendations/RecommendationCard';

const FALLBACK_PROFILE = { face_shape: 'Oval', hair_type: 'Straight', hair_density: 'Medium' };
const FALLBACK_RECOMMENDATIONS = [
  { id: '1', name: 'Textured Crop', match: 95, maintenance: 'low', tags: ['modern', 'casual'], img: 'https://images.unsplash.com/photo-1622286342621-4bd786c2447c?auto=format&fit=crop&w=400&q=80' },
  { id: '2', name: 'Classic Pompadour', match: 88, maintenance: 'medium', tags: ['classic', 'professional'], img: 'https://images.unsplash.com/photo-1593702275687-f8b402bf1fb5?auto=format&fit=crop&w=400&q=80' },
  { id: '3', name: 'Messy Quiff', match: 82, maintenance: 'high', tags: ['trendy', 'casual'], img: 'https://images.unsplash.com/photo-1506806732259-39c2d0268443?auto=format&fit=crop&w=400&q=80' },
];

export default function ResultsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<any>(FALLBACK_PROFILE);
  const [recommendations, setRecommendations] = useState<any[]>(FALLBACK_RECOMMENDATIONS);

  useEffect(() => {
    let isMounted = true;
    const sessionId = location.state?.sessionId;
    const analysisResult = location.state?.analysisResult;

    if (analysisResult) {
      const faceShape = analysisResult.face_analysis?.face_shape || 'Oval';
      const hairType = analysisResult.hair_profile?.hair_type || 'Wavy';
      const hairDensity = analysisResult.hair_profile?.hair_density || 'Medium';
      setProfile({
        face_shape: faceShape,
        hair_type: hairType,
        hair_density: hairDensity,
      });
    }

    const fetchRecommendations = async () => {
      if (sessionId) {
        try {
          const res = await fetch(`/api/recommendations/${sessionId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(location.state?.preferences || {})
          });
          if (res.ok) {
            const data = await res.json();
            if (data.recommendations && data.recommendations.length > 0) {
              const mapped = data.recommendations.map((r: any) => ({
                id: r.id,
                name: r.hairstyle?.name || 'Recommended Hairstyle',
                description: r.hairstyle?.description || '',
                match: Math.round(r.score || 88),
                maintenance: r.hairstyle?.maintenance_level || 'medium',
                tags: r.hairstyle?.style_tags || ['modern'],
                img: r.hairstyle?.image_url || 'https://images.unsplash.com/photo-1622286342621-4bd786c2447c?auto=format&fit=crop&w=400&q=80',
                reasons: r.reasons || [],
                explanation: r.explanation || ''
              }));
              if (isMounted) setRecommendations(mapped);
            }
          }
        } catch (err) {
          console.warn('Could not fetch recommendations from API:', err);
        }
      }
      if (isMounted) setLoading(false);
    };

    fetchRecommendations();

    return () => {
      isMounted = false;
    };
  }, [location.state]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-24 flex flex-col items-center justify-center min-h-[60vh]">
        <Sparkles className="w-12 h-12 text-primary animate-pulse mb-6" />
        <h2 className="text-2xl font-bold mb-2">Generating Recommendations</h2>
        <p className="text-muted-foreground">Matching your face shape and hair profile with curated hairstyles...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <StyleProfile profile={profile} />
      </motion.div>

      <div className="mb-8">
        <h2 className="text-3xl font-bold">Recommended Hairstyles</h2>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {recommendations.map((style, idx) => (
          <motion.div
            key={style.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: idx * 0.1 }}
          >
            <RecommendationCard 
              style={style} 
              rank={idx + 1}
              onTryOn={() => navigate('/tryon', { 
                state: { 
                  style, 
                  allStyles: recommendations,
                  userPhotoUrl: location.state?.imageUrl,
                  sessionId: location.state?.sessionId
                } 
              })}
            />
          </motion.div>
        ))}
      </div>
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card } from '../components/ui/Card';
import AnalysisProgress from '../components/analysis/AnalysisProgress';

export default function AnalysisPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const file = location.state?.file as File;

  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!file) {
      navigate('/upload');
      return;
    }

    let isMounted = true;
    let uploadSessionId = '';
    let analysisData: any = null;

    // Trigger API call in parallel with progress animation
    const performAnalysis = async () => {
      try {
        const formData = new FormData();
        formData.append('file', file);
        const uploadRes = await fetch('/api/analysis/upload', {
          method: 'POST',
          body: formData,
        });
        if (uploadRes.ok) {
          const uploadJson = await uploadRes.json();
          uploadSessionId = uploadJson.session_id;
          const analyzeRes = await fetch(`/api/analysis/analyze/${uploadSessionId}`, {
            method: 'POST',
          });
          if (analyzeRes.ok) {
            analysisData = await analyzeRes.json();
          }
        }
      } catch (err) {
        console.warn('Live API analysis failed, using visual preview pipeline:', err);
      }
    };

    performAnalysis();

    const totalDuration = 4500;
    const interval = 100;
    const stepsCount = totalDuration / interval;
    let currentCount = 0;

    const timer = setInterval(() => {
      currentCount++;
      const percent = (currentCount / stepsCount) * 100;
      if (isMounted) {
        setProgress(percent);
        const stepIndex = Math.floor((percent / 100) * 5);
        setCurrentStep(Math.min(stepIndex, 4));
      }

      if (percent >= 100) {
        clearInterval(timer);
        setTimeout(() => {
          if (isMounted) {
            navigate('/preferences', { 
              state: { 
                file,
                sessionId: uploadSessionId || 'session_default', 
                imageUrl: URL.createObjectURL(file),
                analysisResult: analysisData
              } 
            });
          }
        }, 300);
      }
    }, interval);

    return () => {
      isMounted = false;
      clearInterval(timer);
    };
  }, [file, navigate]);

  return (
    <div className="container mx-auto px-4 py-16 max-w-4xl min-h-[calc(100vh-8rem)] flex items-center justify-center">
      <div className="w-full grid md:grid-cols-2 gap-12 items-center">
        <AnalysisProgress currentStep={currentStep} progress={progress} />

        <div className="hidden md:block">
          <Card className="p-2 glass overflow-hidden shadow-2xl rotate-2 hover:rotate-0 transition-transform duration-500">
            <div className="relative aspect-[3/4] rounded-lg overflow-hidden border border-white/20">
              {file && <img src={URL.createObjectURL(file)} alt="Analyzing" className="object-cover w-full h-full opacity-50 sepia-[.2]" />}
              <motion.div
                className="absolute left-0 right-0 h-1 bg-primary shadow-[0_0_15px_3px_rgba(124,58,237,0.5)] z-10"
                animate={{ top: ['0%', '100%', '0%'] }}
                transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
              />
              <div className="absolute inset-0 bg-primary/10 mix-blend-overlay" />
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

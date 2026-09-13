import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, Loader2, ScanFace, Scissors, Sparkles } from 'lucide-react';
import { Progress } from '../ui/Progress';

interface AnalysisProgressProps {
  currentStep: number;
  progress: number;
}

const steps = [
  { id: 1, label: 'Detecting face', icon: ScanFace },
  { id: 2, label: 'Mapping facial features', icon: ScanFace },
  { id: 3, label: 'Analyzing face shape', icon: ScanFace },
  { id: 4, label: 'Analyzing hair type & texture', icon: Scissors },
  { id: 5, label: 'Finding suitable hairstyles', icon: Sparkles },
];

export default function AnalysisProgress({ currentStep, progress }: AnalysisProgressProps) {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Analyzing your features</h1>
        <p className="text-muted-foreground">Our AI is processing your photo to give you the best recommendations.</p>
      </div>

      <Progress value={progress} className="h-2" />

      <div className="space-y-4 mt-8">
        {steps.map((step, index) => {
          const isActive = currentStep === index;
          const isCompleted = currentStep > index;
          const Icon = step.icon;

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0.5, x: -10 }}
              animate={{ 
                opacity: isActive || isCompleted ? 1 : 0.4,
                x: isActive ? 10 : 0
              }}
              className={`flex items-center gap-4 p-3 rounded-lg transition-colors ${isActive ? 'bg-primary/5 border border-primary/20' : ''}`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors duration-300 ${
                isCompleted ? 'bg-green-500 text-white shadow-[0_0_10px_rgba(34,197,94,0.4)]' :
                isActive ? 'bg-primary text-primary-foreground shadow-[0_0_10px_rgba(124,58,237,0.4)]' :
                'bg-muted text-muted-foreground'
              }`}>
                <AnimatePresence mode="wait">
                  {isCompleted ? (
                    <motion.div
                      key="completed"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: "spring", stiffness: 300, damping: 20 }}
                    >
                      <Check className="w-4 h-4" />
                    </motion.div>
                  ) : isActive ? (
                    <motion.div key="active" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                      <Loader2 className="w-4 h-4 animate-spin" />
                    </motion.div>
                  ) : (
                    <motion.div key="pending" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                      <Icon className="w-4 h-4" />
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              <span className={`font-medium transition-colors ${isCompleted ? 'text-foreground' : isActive ? 'text-primary' : 'text-muted-foreground'}`}>
                {step.label}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

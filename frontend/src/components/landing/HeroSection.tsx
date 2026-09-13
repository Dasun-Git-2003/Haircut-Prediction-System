import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from '../ui/Button';

export default function HeroSection() {
  const fadeInUp = {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" as const } }
  };

  return (
    <section className="relative pt-20 pb-32 overflow-hidden flex flex-col items-center text-center px-4">
      <motion.div initial="hidden" animate="visible" variants={fadeInUp} className="max-w-4xl z-10">
        <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors bg-primary/10 text-primary border-primary/20 mb-6">
          AI-Powered Makeovers
        </span>
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8">
          Find Your Perfect Hairstyle with <span className="text-gradient">AI</span>
        </h1>
        <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
          Analyze your face and hair, discover personalized hairstyles, and visualize them on yourself with AI.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link to="/upload">
            <Button size="lg" className="h-14 px-8 text-lg rounded-full shadow-lg shadow-primary/25 hover:scale-105 transition-transform">
              Try StyleAI Free
            </Button>
          </Link>
          <a href="#how-it-works">
            <Button size="lg" variant="outline" className="h-14 px-8 text-lg rounded-full bg-background/50 backdrop-blur hover:bg-muted">
              See How It Works
            </Button>
          </a>
        </div>
        
        {/* Social Proof Stats */}
        <div className="mt-16 pt-8 border-t border-border/50 grid grid-cols-3 gap-4 max-w-2xl mx-auto text-center">
          <div>
            <div className="text-2xl font-bold text-foreground">50k+</div>
            <div className="text-sm text-muted-foreground">Analyses</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-foreground">98%</div>
            <div className="text-sm text-muted-foreground">Match Accuracy</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-foreground">1M+</div>
            <div className="text-sm text-muted-foreground">Try-Ons</div>
          </div>
        </div>
      </motion.div>
      
      {/* Decorative elements */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-tr from-primary/20 via-secondary/20 to-transparent rounded-full blur-[100px] -z-10 opacity-70 animate-pulse" style={{ animationDuration: '8s' }} />
    </section>
  );
}

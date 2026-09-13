import React from 'react';
import HeroSection from '../components/landing/HeroSection';
import HowItWorks from '../components/landing/HowItWorks';
import Features from '../components/landing/Features';
import PopularStyles from '../components/landing/PopularStyles';
import Footer from '../components/landing/Footer';

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <HeroSection />
      <HowItWorks />
      <Features />
      <PopularStyles />
      {/* Note: The Footer component is already used in MainLayout or we can include it here if preferred. 
          Usually Footer goes in MainLayout, but since the instruction says LandingPage.tsx -> Footer, 
          we'll assume we can include it or it's meant to be global. Let's just leave it out here if MainLayout handles it, 
          Wait, I'll add it here and remove it from MainLayout if necessary, or just keep it global. 
          Let's just use it here if there's no global footer. MainLayout has a footer, so we skip adding it here to avoid duplication. */}
    </div>
  );
}

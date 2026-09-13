import React from 'react';
import { motion } from 'framer-motion';
import { Camera, Scan, Sparkles, Wand2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription } from '../ui/Card';

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.2 }
  }
};

const fadeInUp = {
  hidden: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
};

export default function HowItWorks() {
  const steps = [
    { icon: Camera, title: "1. Upload", desc: "Upload a clear front-facing photo" },
    { icon: Scan, title: "2. Analyze", desc: "AI analyzes your face shape and hair" },
    { icon: Sparkles, title: "3. Discover", desc: "Get personalized hairstyle recommendations" },
    { icon: Wand2, title: "4. Visualize", desc: "See yourself with new hairstyles using AI" }
  ];

  return (
    <section id="how-it-works" className="py-24 bg-muted/30">
      <div className="container mx-auto px-4">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={staggerContainer}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">Four simple steps to your new look</p>
        </motion.div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={staggerContainer}
          className="grid grid-cols-1 md:grid-cols-4 gap-8 relative"
        >
          {steps.map((step, i) => {
            const Icon = step.icon;
            return (
              <motion.div key={i} variants={fadeInUp} className="relative z-10">
                <Card className="h-full border-none shadow-lg bg-background/60 backdrop-blur-sm text-center pt-8 hover:-translate-y-2 transition-transform duration-300">
                  <CardHeader>
                    <div className="mx-auto w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary mb-4 shadow-inner">
                      <Icon className="w-8 h-8" />
                    </div>
                    <CardTitle>{step.title}</CardTitle>
                    <CardDescription className="text-sm mt-2">{step.desc}</CardDescription>
                  </CardHeader>
                </Card>
                {/* Connecting lines for desktop */}
                {i < steps.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-[2px] bg-border z-0" />
                )}
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}

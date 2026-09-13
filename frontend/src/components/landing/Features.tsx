import React from 'react';
import { motion } from 'framer-motion';
import { UserCheck, Scissors, Smartphone, Sparkles, ScanFace, Wand2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';

const features = [
  { icon: ScanFace, title: "Face Shape Analysis", desc: "Advanced computer vision determines your exact face shape with high precision." },
  { icon: Scissors, title: "Hair Type Detection", desc: "Identifies your natural hair texture and density for accurate matching." },
  { icon: Sparkles, title: "Smart Recommendations", desc: "Our AI curates hairstyles that perfectly balance your unique facial features." },
  { icon: Wand2, title: "Virtual Try-On", desc: "Generative AI places the new haircut on your actual photo realistically." }
];

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
};

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
};

export default function Features() {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background blobs */}
      <div className="absolute -left-40 top-20 w-80 h-80 bg-primary/10 rounded-full blur-[80px] -z-10" />
      <div className="absolute -right-40 bottom-20 w-80 h-80 bg-secondary/10 rounded-full blur-[80px] -z-10" />

      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Smart Features for Perfect Results</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Our proprietary AI pipeline analyzes multiple facial vectors to ensure the styles we recommend will actually look good on you.
          </p>
        </div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={staggerContainer}
          className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto"
        >
          {features.map((f, i) => {
            const Icon = f.icon;
            return (
              <motion.div key={i} variants={fadeInUp}>
                <Card className="h-full glass hover:-translate-y-2 transition-all duration-300 hover:shadow-xl border-white/20">
                  <CardHeader className="flex flex-row items-center gap-4 pb-2">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center text-primary">
                      <Icon className="w-6 h-6" />
                    </div>
                    <CardTitle className="text-xl">{f.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">{f.desc}</p>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}

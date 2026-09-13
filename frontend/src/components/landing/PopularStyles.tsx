import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Card, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';

const styles = [
  { id: 1, name: 'Textured Crop', category: 'Short', img: 'https://images.unsplash.com/photo-1622286342621-4bd786c2447c?w=400&q=80' },
  { id: 2, name: 'Modern Pompadour', category: 'Medium', img: 'https://images.unsplash.com/photo-1593702275687-f8b402bf1fb5?w=400&q=80' },
  { id: 3, name: 'Classic Fade', category: 'Short', img: 'https://images.unsplash.com/photo-1506806732259-39c2d0268443?w=400&q=80' },
  { id: 4, name: 'Long Layers', category: 'Long', img: 'https://images.unsplash.com/photo-1517524962299-bb33fb590a5a?w=400&q=80' },
  { id: 5, name: 'Messy Quiff', category: 'Medium', img: 'https://images.unsplash.com/photo-1620002094269-8bc3c6bfa6b4?w=400&q=80' },
  { id: 6, name: 'Buzz Cut', category: 'Very Short', img: 'https://images.unsplash.com/photo-1502324207935-77987b5a83a4?w=400&q=80' }
];

export default function PopularStyles() {
  return (
    <section className="py-24 bg-muted/20">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-end mb-12">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Trending Styles</h2>
            <p className="text-muted-foreground">Discover what's popular this season.</p>
          </div>
          <Link to="/hairstyles" className="text-primary font-medium hover:underline hidden md:block">
            View All Styles &rarr;
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 md:gap-6">
          {styles.map((style, idx) => (
            <motion.div
              key={style.id}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
            >
              <Card className="overflow-hidden group cursor-pointer border-none shadow-sm hover:shadow-xl transition-all duration-300 h-full">
                <div className="relative aspect-[3/4] overflow-hidden bg-gradient-to-br from-primary/10 to-secondary/10">
                  <img 
                    src={style.img} 
                    alt={style.name} 
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                  />
                  <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors duration-300" />
                  <div className="absolute bottom-3 left-3 right-3">
                    <Badge variant="secondary" className="mb-2 backdrop-blur-md bg-white/80 text-black border-none text-[10px]">
                      {style.category}
                    </Badge>
                    <h3 className="text-white font-bold text-sm leading-tight drop-shadow-md">
                      {style.name}
                    </h3>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
        
        <div className="mt-8 text-center md:hidden">
          <Link to="/hairstyles" className="text-primary font-medium hover:underline">
            View All Styles &rarr;
          </Link>
        </div>
      </div>
    </section>
  );
}

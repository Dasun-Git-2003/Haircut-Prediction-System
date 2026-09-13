import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Users, Activity, ImageIcon, Target } from 'lucide-react';

export default function Analytics() {
  const stats = [
    { title: 'Total Users', value: '1,248', icon: Users, change: '+12%', color: 'text-blue-500' },
    { title: 'Analyses Run', value: '5,820', icon: Activity, change: '+24%', color: 'text-purple-500' },
    { title: 'Try-Ons Generated', value: '12,400', icon: ImageIcon, change: '+18%', color: 'text-rose-500' },
    { title: 'Recommendation Success', value: '89%', icon: Target, change: '+2%', color: 'text-green-500' },
  ];

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <Card key={i}>
              <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
                <Icon className={`w-4 h-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-green-500 mt-1 flex items-center">
                  {stat.change} from last month
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Most Recommended Styles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-sm text-muted-foreground w-4">{i}.</span>
                    <span className="font-medium">Textured Crop {i}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">{1000 - i * 150} times</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>User Demographics (Face Shapes)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { shape: 'Oval', pct: 45 },
                { shape: 'Round', pct: 25 },
                { shape: 'Square', pct: 15 },
                { shape: 'Heart', pct: 10 },
                { shape: 'Diamond', pct: 5 }
              ].map((item, i) => (
                <div key={i} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>{item.shape}</span>
                    <span className="text-muted-foreground">{item.pct}%</span>
                  </div>
                  <div className="h-2 w-full bg-secondary/20 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-primary" 
                      style={{ width: `${item.pct}%` }} 
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

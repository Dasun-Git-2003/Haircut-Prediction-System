import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Activity, Image as ImageIcon, Heart } from 'lucide-react';
import SavedHairstyles from '../components/dashboard/SavedHairstyles';
import AnalysisHistory from '../components/dashboard/AnalysisHistory';

export default function DashboardPage() {
  const { user } = useAuth();

  const stats = [
    { title: 'Total Analyses', value: '12', icon: Activity, color: 'text-blue-500' },
    { title: 'Saved Styles', value: '5', icon: Heart, color: 'text-rose-500' },
    { title: 'Try-Ons Generated', value: '24', icon: ImageIcon, color: 'text-purple-500' },
  ];

  return (
    <div className="py-6 max-w-5xl">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Welcome back, {user?.username || 'User'}</h1>
          <p className="text-muted-foreground mt-1">Here is a summary of your style journey.</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3 mb-8">
        {stats.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <Card key={idx} className="glass">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <Icon className={`w-4 h-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stat.value}</div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <section>
          <h2 className="text-xl font-bold mb-4">Saved Hairstyles</h2>
          <SavedHairstyles hairstyles={[
            { name: 'Textured Crop' }, { name: 'Modern Fade' }, { name: 'Classic Pomp' }
          ]} />
        </section>

        <section>
          <h2 className="text-xl font-bold mb-4">Recent Analyses</h2>
          <AnalysisHistory history={[
            { face_shape: 'Oval', hair_type: 'Wavy' },
            { face_shape: 'Round', hair_type: 'Straight' }
          ]} />
        </section>
      </div>
    </div>
  );
}

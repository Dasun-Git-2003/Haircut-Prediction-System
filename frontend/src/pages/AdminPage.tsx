import React, { useState } from 'react';
import HairstyleManager from '../components/admin/HairstyleManager';
import Analytics from '../components/admin/Analytics';

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState('hairstyles');

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Admin Console</h1>
      </div>

      <div className="flex gap-4 mb-6 border-b">
        <button 
          onClick={() => setActiveTab('hairstyles')} 
          className={`px-4 py-2 text-sm font-medium border-b-2 ${activeTab === 'hairstyles' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'}`}
        >
          Hairstyle Management
        </button>
        <button 
          onClick={() => setActiveTab('analytics')} 
          className={`px-4 py-2 text-sm font-medium border-b-2 ${activeTab === 'analytics' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'}`}
        >
          System Analytics
        </button>
      </div>

      {activeTab === 'hairstyles' ? <HairstyleManager /> : <Analytics />}
    </div>
  );
}

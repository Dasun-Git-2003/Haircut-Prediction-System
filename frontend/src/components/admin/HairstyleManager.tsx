import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Button } from '../ui/Button';
import { Edit, Trash2, Plus } from 'lucide-react';

export default function HairstyleManager() {
  const styles = [1, 2, 3, 4, 5]; // Mock data

  return (
    <Card>
      <CardHeader className="flex flex-row justify-between items-center">
        <CardTitle>Hairstyles Database</CardTitle>
        <Button size="sm" className="gap-2"><Plus className="w-4 h-4"/> Add New</Button>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground uppercase bg-muted/50">
              <tr>
                <th className="px-6 py-3 rounded-tl-lg">ID</th>
                <th className="px-6 py-3">Image</th>
                <th className="px-6 py-3">Name</th>
                <th className="px-6 py-3">Category</th>
                <th className="px-6 py-3">Maintenance</th>
                <th className="px-6 py-3 text-right rounded-tr-lg">Actions</th>
              </tr>
            </thead>
            <tbody>
              {styles.map((item) => (
                <tr key={item} className="border-b last:border-0 hover:bg-muted/20 transition-colors">
                  <td className="px-6 py-4 font-medium">#00{item}</td>
                  <td className="px-6 py-4">
                    <div className="w-10 h-10 rounded bg-muted overflow-hidden">
                      <img src={`https://images.unsplash.com/photo-1622286342621-4bd786c2447c?w=100&q=80&random=${item}`} alt="Style" className="w-full h-full object-cover" />
                    </div>
                  </td>
                  <td className="px-6 py-4 font-medium">Textured Crop {item}</td>
                  <td className="px-6 py-4 text-muted-foreground">Short</td>
                  <td className="px-6 py-4 text-muted-foreground capitalize">Low</td>
                  <td className="px-6 py-4 text-right">
                    <Button variant="ghost" size="icon" className="h-8 w-8 mr-1">
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

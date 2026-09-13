import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, History, Heart, Settings, User as UserIcon } from 'lucide-react';
import { cn } from '../lib/utils';
import MainLayout from './MainLayout';

export default function DashboardLayout() {
  const location = useLocation();

  const links = [
    { href: '/dashboard', label: 'Overview', icon: LayoutDashboard },
    { href: '/dashboard/analyses', label: 'My Analyses', icon: History },
    { href: '/dashboard/favorites', label: 'Saved Styles', icon: Heart },
    { href: '/dashboard/profile', label: 'Profile', icon: UserIcon },
    { href: '/dashboard/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-8 flex flex-col md:flex-row gap-8 h-[calc(100vh-4rem-80px)]">
        {/* Sidebar */}
        <aside className="w-full md:w-64 flex-shrink-0">
          <nav className="flex md:flex-col gap-2 overflow-x-auto pb-4 md:pb-0 hide-scrollbar">
            {links.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.href;
              return (
                <Link
                  key={link.href}
                  to={link.href}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors whitespace-nowrap",
                    isActive 
                      ? "bg-primary/10 text-primary" 
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  )}
                >
                  <Icon className="w-5 h-5" />
                  {link.label}
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Content */}
        <main className="flex-1 overflow-y-auto pr-2">
          <Outlet />
        </main>
      </div>
    </MainLayout>
  );
}

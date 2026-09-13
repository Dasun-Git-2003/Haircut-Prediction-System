import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';
import { Menu, X, Wand2 } from 'lucide-react';
import { Button } from '../components/ui/Button';

interface MainLayoutProps {
  children?: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden bg-background">
      {/* Background decoration */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/5 blur-[120px] -z-10" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary/5 blur-[120px] -z-10" />

      <header className="sticky top-0 z-50 w-full border-b border-white/10 glass">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <Wand2 className="w-6 h-6 text-primary" />
            <span className="text-xl font-bold text-gradient">StyleAI</span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-6">
            <Link to="/" className="text-sm font-medium hover:text-primary transition-colors">Home</Link>
            <Link to="/hairstyles" className="text-sm font-medium hover:text-primary transition-colors">Hairstyles</Link>
            {user ? (
              <>
                <Link to="/dashboard" className="text-sm font-medium hover:text-primary transition-colors">Dashboard</Link>
                {user.is_admin && <Link to="/admin" className="text-sm font-medium hover:text-primary transition-colors">Admin</Link>}
                <Button variant="ghost" onClick={handleLogout}>Logout</Button>
              </>
            ) : (
              <>
                <Link to="/login"><Button variant="ghost">Login</Button></Link>
                <Link to="/register"><Button>Sign Up</Button></Link>
              </>
            )}
          </nav>

          {/* Mobile Toggle */}
          <button className="md:hidden p-2" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
            {isMobileMenuOpen ? <X /> : <Menu />}
          </button>
        </div>
      </header>

      {/* Mobile Nav */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="absolute top-16 left-0 right-0 glass z-40 p-4 border-b md:hidden flex flex-col gap-4 shadow-xl"
          >
            <Link to="/" onClick={() => setIsMobileMenuOpen(false)} className="px-4 py-2 hover:bg-muted rounded-md">Home</Link>
            <Link to="/hairstyles" onClick={() => setIsMobileMenuOpen(false)} className="px-4 py-2 hover:bg-muted rounded-md">Hairstyles</Link>
            {user ? (
              <>
                <Link to="/dashboard" onClick={() => setIsMobileMenuOpen(false)} className="px-4 py-2 hover:bg-muted rounded-md">Dashboard</Link>
                {user.is_admin && <Link to="/admin" onClick={() => setIsMobileMenuOpen(false)} className="px-4 py-2 hover:bg-muted rounded-md">Admin</Link>}
                <Button variant="ghost" onClick={() => { handleLogout(); setIsMobileMenuOpen(false); }}>Logout</Button>
              </>
            ) : (
              <div className="flex flex-col gap-2">
                <Link to="/login" onClick={() => setIsMobileMenuOpen(false)}><Button variant="outline" className="w-full">Login</Button></Link>
                <Link to="/register" onClick={() => setIsMobileMenuOpen(false)}><Button className="w-full">Sign Up</Button></Link>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      <main className="flex-1">
        {children || <Outlet />}
      </main>

      <footer className="border-t py-8 mt-auto">
        <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Wand2 className="w-5 h-5 text-primary" />
            <span className="font-bold">StyleAI</span>
          </div>
          <div className="flex gap-6 text-sm text-muted-foreground">
            <Link to="#" className="hover:text-foreground">About</Link>
            <Link to="#" className="hover:text-foreground">Privacy</Link>
            <Link to="#" className="hover:text-foreground">Terms</Link>
            <Link to="#" className="hover:text-foreground">Contact</Link>
          </div>
          <p className="text-sm text-muted-foreground">© 2024 StyleAI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

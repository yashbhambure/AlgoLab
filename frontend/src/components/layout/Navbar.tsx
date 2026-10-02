import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Cpu,
  BarChart3,
  Play,
  Sigma,
  Sparkles,
  FolderArchive,
  BookOpen,
  GraduationCap,
  Layers,
  Menu,
  X,
  Activity,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";
import { api } from "../../services/api";
import { ThemeToggle } from "../common/ThemeToggle";

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [backendStatus, setBackendStatus] = useState<"connected" | "checking" | "disconnected">("checking");
  const location = useLocation();

  useEffect(() => {
    let isMounted = true;
    api.getHealth()
      .then(() => {
        if (isMounted) setBackendStatus("connected");
      })
      .catch(() => {
        if (isMounted) setBackendStatus("disconnected");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const navItems = [
    { path: "/", label: "Dashboard", icon: Activity },
    { path: "/curriculum", label: "Curriculum", icon: GraduationCap },
    { path: "/problems", label: "Problems", icon: Layers },
    { path: "/catalog", label: "Catalog", icon: BookOpen },
    { path: "/benchmark", label: "Benchmark", icon: BarChart3 },
    { path: "/visualizer", label: "Visualizer", icon: Play },
    { path: "/complexity", label: "Complexity", icon: Sigma },
    { path: "/recommend", label: "Recommendation", icon: Sparkles },
    { path: "/experiments", label: "Experiments", icon: FolderArchive },
  ];

  const isActive = (path: string) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname.startsWith(path);
  };

  return (
    <header className="sticky top-0 z-50 bg-[#080b11]/95 backdrop-blur-md border-b border-slate-800/80 transition-colors duration-200">
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16 gap-4">
          {/* Brand Logo */}
          <Link
            to="/"
            className="flex items-center gap-2.5 group focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 rounded-lg p-1 -ml-1"
          >
            <div className="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700/80 flex items-center justify-center text-sky-400 group-hover:border-sky-500/60 group-hover:text-sky-300 transition-colors">
              <Cpu className="w-4 h-4" />
            </div>

            <div className="flex items-center gap-2">
              <span className="text-base font-semibold tracking-tight text-white group-hover:text-slate-200 transition-colors">
                Algo<span className="text-sky-400">Lab</span>
              </span>
              <span className="hidden sm:inline-block px-2 py-0.5 text-[11px] font-mono font-medium text-slate-400 bg-slate-900 border border-slate-800 rounded">
                DAA Suite
              </span>
            </div>
          </Link>

          {/* Desktop Nav Items */}
          <nav className="hidden xl:flex items-center space-x-1" aria-label="Main Navigation">
            {navItems.map((item) => {
              const active = isActive(item.path);
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-3 py-1.5 rounded-md text-[13px] font-medium transition-all flex items-center gap-1.5 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 ${
                    active
                      ? "text-sky-400 bg-sky-950/50 border border-sky-800/60 font-semibold"
                      : "text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent"
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${active ? "text-sky-400" : "text-slate-400"}`} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Right Controls: Status & Theme Toggle */}
          <div className="hidden sm:flex items-center gap-2.5">
            <ThemeToggle />
            <div
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-mono border ${
                backendStatus === "connected"
                  ? "bg-emerald-950/40 text-emerald-400 border-emerald-800/40"
                  : backendStatus === "checking"
                  ? "bg-slate-900 text-slate-400 border-slate-800"
                  : "bg-amber-950/40 text-amber-400 border-amber-800/40"
              }`}
            >
              {backendStatus === "connected" ? (
                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
              ) : backendStatus === "checking" ? (
                <div className="w-2 h-2 rounded-full bg-slate-400 animate-pulse" />
              ) : (
                <AlertCircle className="w-3 h-3 text-amber-400" />
              )}
              <span>
                {backendStatus === "connected"
                  ? "Core Ready"
                  : backendStatus === "checking"
                  ? "Connecting"
                  : "Offline Mode"}
              </span>
            </div>
          </div>

          {/* Mobile Right Controls */}
          <div className="flex items-center gap-2 xl:hidden">
            <ThemeToggle variant="compact" />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500"
              aria-label="Toggle navigation menu"
              aria-expanded={mobileMenuOpen}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Dropdown */}
      {mobileMenuOpen && (
        <div className="xl:hidden bg-[#0a0e17] border-b border-slate-800 px-4 py-3 space-y-1 animate-in fade-in slide-in-from-top-2 duration-150">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
            {navItems.map((item) => {
              const active = isActive(item.path);
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`p-2.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-2.5 ${
                    active
                      ? "bg-sky-950/60 border border-sky-800/60 text-sky-300 font-semibold"
                      : "bg-slate-900/50 border border-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800/60"
                  }`}
                >
                  <Icon className={`w-4 h-4 ${active ? "text-sky-400" : "text-slate-400"}`} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>

          <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400 px-1 font-mono">
            <span>Theme:</span>
            <ThemeToggle variant="pill" showLabel />
          </div>

          <div className="flex items-center justify-between text-[11px] text-slate-400 px-1 font-mono">
            <span>Backend Status:</span>
            <span className={backendStatus === "connected" ? "text-emerald-400 font-medium" : "text-amber-400"}>
              {backendStatus === "connected" ? "Connected" : "Disconnected"}
            </span>
          </div>
        </div>
      )}
    </header>
  );
}

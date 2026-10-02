import { Cpu, Terminal, ShieldCheck, BookOpen, Layers } from "lucide-react";
import { Link } from "react-router-dom";

export function Footer() {
  return (
    <footer className="bg-[#06080d] border-t border-slate-800/80 text-slate-400 text-xs mt-auto py-10 transition-colors duration-200">
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-8 border-b border-slate-800/60">
          {/* Col 1: System Info */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-white font-semibold text-sm">
              <div className="w-6 h-6 rounded bg-slate-900 border border-slate-700 flex items-center justify-center text-sky-400">
                <Cpu className="w-3.5 h-3.5" />
              </div>
              <span>AlgoLab Laboratory</span>
            </div>
            <p className="text-slate-400 text-[13px] leading-relaxed font-sans">
              High-precision algorithm analysis platform for the Design & Analysis of Algorithms curriculum.
              Empirical profiling, asymptotic derivations, and Multi-Criteria Decision Analysis (MCDA).
            </p>
          </div>

          {/* Col 2: Core Paradigms */}
          <div>
            <h4 className="text-slate-200 font-semibold text-xs uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-sky-400" />
              Core Paradigms
            </h4>
            <ul className="space-y-2 text-[12px] text-slate-400 font-sans">
              <li><Link to="/catalog?paradigm=Sorting" className="hover:text-slate-200 transition-colors">Sorting & Order Statistics</Link></li>
              <li><Link to="/catalog?paradigm=Searching" className="hover:text-slate-200 transition-colors">Search & Indexing Models</Link></li>
              <li><Link to="/catalog?paradigm=Divide%20%26%20Conquer" className="hover:text-slate-200 transition-colors">Divide & Conquer Recurrences</Link></li>
              <li><Link to="/catalog?paradigm=Greedy" className="hover:text-slate-200 transition-colors">Greedy Approximations & MST</Link></li>
              <li><Link to="/catalog?paradigm=Dynamic%20Programming" className="hover:text-slate-200 transition-colors">Dynamic Programming Tabulation</Link></li>
            </ul>
          </div>

          {/* Col 3: Analytical Capabilities */}
          <div>
            <h4 className="text-slate-200 font-semibold text-xs uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Terminal className="w-3.5 h-3.5 text-sky-400" />
              Analytical Engines
            </h4>
            <ul className="space-y-2 text-[12px] text-slate-400 font-sans">
              <li><Link to="/complexity" className="hover:text-slate-200 transition-colors">Master Theorem Solver (Cases 1–3)</Link></li>
              <li><Link to="/complexity" className="hover:text-slate-200 transition-colors">Empirical Non-linear Curve Fitting</Link></li>
              <li><Link to="/recommend" className="hover:text-slate-200 transition-colors">MCDA Multi-Criteria Scorer</Link></li>
              <li><Link to="/decision-tree" className="hover:text-slate-200 transition-colors">Guided Decision Tree Engine</Link></li>
              <li><Link to="/experiments" className="hover:text-slate-200 transition-colors">Scaling Sweep Experiments</Link></li>
            </ul>
          </div>

          {/* Col 4: Benchmark Methodology */}
          <div>
            <h4 className="text-slate-200 font-semibold text-xs uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-sky-400" />
              Benchmark Isolation
            </h4>
            <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 space-y-2 text-[12px] font-mono">
              <div className="flex justify-between">
                <span className="text-slate-400 font-sans">Timing:</span>
                <span className="text-sky-300">perf_counter_ns</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 font-sans">Memory:</span>
                <span className="text-emerald-400">tracemalloc</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 font-sans">GC State:</span>
                <span className="text-purple-400">Controlled</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-500 font-sans">
          <div className="flex items-center gap-2">
            <Layers className="w-3.5 h-3.5 text-slate-600" />
            <span>AlgoLab DAA Analysis Platform &bull; Academic & Engineering Laboratory</span>
          </div>
          <div className="flex items-center gap-4 font-mono text-[11px]">
            <span>FastAPI Backend</span>
            <span className="text-slate-700">&bull;</span>
            <span>React 19 + TypeScript</span>
            <span className="text-slate-700">&bull;</span>
            <span className="text-slate-400">35 Canonical Algorithms</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

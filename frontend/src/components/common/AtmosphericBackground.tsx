export function AtmosphericBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
      {/* Theme Adaptive Canvas Base */}
      <div className="absolute inset-0 bg-[var(--bg-canvas)] transition-colors duration-200" />

      {/* Ambient Laboratory Energy Orbs (Soft floating illumination) */}
      <div
        className="absolute -top-[15%] left-[20%] w-[650px] h-[650px] rounded-full bg-sky-500/[0.08] dark:bg-sky-500/[0.06] blur-[130px] animate-ambient-float-1"
        style={{ willChange: "transform" }}
      />
      <div
        className="absolute top-[35%] -right-[8%] w-[600px] h-[600px] rounded-full bg-purple-500/[0.08] dark:bg-purple-600/[0.05] blur-[150px] animate-ambient-float-2"
        style={{ willChange: "transform" }}
      />
      <div
        className="absolute -bottom-[12%] left-[30%] w-[550px] h-[550px] rounded-full bg-teal-500/[0.06] dark:bg-teal-500/[0.04] blur-[140px] animate-ambient-float-1"
        style={{ willChange: "transform" }}
      />

      {/* Layer 1: Primary Micro-Grid (Infinitely Moving) */}
      <div
        className="absolute inset-0 lab-grid-bg opacity-45 dark:opacity-60"
        style={{
          maskImage: "radial-gradient(ellipse 90% 70% at 50% 40%, black 45%, transparent 95%)",
          WebkitMaskImage: "radial-gradient(ellipse 90% 70% at 50% 40%, black 45%, transparent 95%)",
        }}
      />

      {/* Layer 2: Secondary Macro-Grid (Infinitely Counter-Drifting Parallax) */}
      <div
        className="absolute inset-0 lab-grid-bg-secondary opacity-35 dark:opacity-50"
        style={{
          maskImage: "radial-gradient(ellipse 85% 65% at 50% 45%, black 40%, transparent 90%)",
          WebkitMaskImage: "radial-gradient(ellipse 85% 65% at 50% 45%, black 40%, transparent 90%)",
        }}
      />

      {/* Layer 3: Coordinate Quantum Intersection Nodes */}
      <div
        className="absolute inset-0 lab-grid-dots opacity-45 dark:opacity-70"
        style={{
          maskImage: "radial-gradient(ellipse 80% 60% at 50% 40%, black 35%, transparent 85%)",
          WebkitMaskImage: "radial-gradient(ellipse 80% 60% at 50% 40%, black 35%, transparent 85%)",
        }}
      />

      {/* Layer 4: Vignette Edge Gradient for Pristine Readability */}
      <div
        className="absolute inset-0"
        style={{
          background: "radial-gradient(ellipse 95% 75% at 50% 40%, transparent 50%, var(--bg-canvas) 100%)",
        }}
      />
    </div>
  );
}

export default AtmosphericBackground;

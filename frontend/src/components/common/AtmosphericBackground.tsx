import { RealisticGridCanvas } from "./RealisticGridCanvas";

export function AtmosphericBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
      {/* Theme Adaptive Canvas Base */}
      <div className="absolute inset-0 bg-[var(--bg-canvas)] transition-colors duration-200" />

      {/* Ambient Laboratory Energy Orbs (Soft floating illumination) */}
      <div
        className="absolute -top-[15%] left-[20%] w-[650px] h-[650px] rounded-full bg-sky-500/[0.07] dark:bg-sky-500/[0.06] blur-[130px] animate-ambient-float-1"
        style={{ willChange: "transform" }}
      />
      <div
        className="absolute top-[35%] -right-[8%] w-[600px] h-[600px] rounded-full bg-purple-500/[0.07] dark:bg-purple-600/[0.05] blur-[150px] animate-ambient-float-2"
        style={{ willChange: "transform" }}
      />
      <div
        className="absolute -bottom-[12%] left-[30%] w-[550px] h-[550px] rounded-full bg-teal-500/[0.05] dark:bg-teal-500/[0.04] blur-[140px] animate-ambient-float-1"
        style={{ willChange: "transform" }}
      />

      {/* Realistic Dynamic Grid Engine (3D Perspective Horizon + Interactive Photometric Spotlight + Algorithmic Signals) */}
      <RealisticGridCanvas />

      {/* Vignette Edge Gradient for Crisp Card and Content Readability */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: "radial-gradient(ellipse 95% 75% at 50% 40%, transparent 45%, var(--bg-canvas) 100%)",
        }}
      />
    </div>
  );
}


export default AtmosphericBackground;

export function AtmosphericBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
      {/* Theme Adaptive Canvas */}
      <div className="absolute inset-0 bg-[var(--bg-canvas)] transition-colors duration-200" />
      {/* Subtle Technical Grid Texture */}
      <div className="absolute inset-0 lab-grid-bg opacity-30 dark:opacity-40" />
    </div>
  );
}

export default AtmosphericBackground;

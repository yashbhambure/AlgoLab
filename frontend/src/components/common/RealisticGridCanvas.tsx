import { useEffect, useRef, useCallback } from "react";
import { useThemeContext } from "../../context/ThemeContext";

interface DataPacket {
  axis: "horizontal" | "vertical";
  lineCoord: number; // Y coordinate for horizontal, X coordinate for vertical
  pos: number; // Current moving position along axis
  speed: number;
  length: number;
  colorType: "cyan" | "violet" | "teal" | "amber";
  sparkleTimer: number;
}

interface Shockwave {
  x: number;
  y: number;
  radius: number;
  maxRadius: number;
  alpha: number;
}

export function RealisticGridCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const { theme } = useThemeContext();

  // Animation and physics state
  const mouseRef = useRef({
    current: { x: -1000, y: -1000 },
    target: { x: -1000, y: -1000 },
    active: false,
  });

  const driftRef = useRef({ x: 0, y: 0 });
  const packetsRef = useRef<DataPacket[]>([]);
  const shockwavesRef = useRef<Shockwave[]>([]);
  const animFrameIdRef = useRef<number | null>(null);
  const lastTimeRef = useRef<number>(performance.now());

  // Initialize or re-seed data packets
  const initPackets = useCallback((width: number, height: number, cellSize: number) => {
    const packets: DataPacket[] = [];
    const count = Math.min(16, Math.max(8, Math.floor((width * height) / 110000)));
    const colorTypes: Array<"cyan" | "violet" | "teal" | "amber"> = ["cyan", "cyan", "violet", "teal"];

    for (let i = 0; i < count; i++) {
      const isHorizontal = Math.random() > 0.45;
      const numLines = isHorizontal ? Math.floor(height / cellSize) : Math.floor(width / cellSize);
      const lineIndex = Math.floor(Math.random() * numLines);
      const lineCoord = lineIndex * cellSize;

      const maxPos = isHorizontal ? width : height;
      const pos = Math.random() * maxPos;
      const speed = (Math.random() * 1.8 + 1.2) * (Math.random() > 0.5 ? 1 : -1);

      packets.push({
        axis: isHorizontal ? "horizontal" : "vertical",
        lineCoord,
        pos,
        speed,
        length: Math.random() * 60 + 50,
        colorType: colorTypes[Math.floor(Math.random() * colorTypes.length)],
        sparkleTimer: 0,
      });
    }

    packetsRef.current = packets;
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d", { alpha: true });
    if (!ctx) return;

    let width = 0;
    let height = 0;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const CELL_SIZE = 52;
    const MAJOR_STEP = 4; // Major grid line every 4 cells (208px)

    const handleResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);

      if (packetsRef.current.length === 0) {
        initPackets(width, height, CELL_SIZE);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize, { passive: true });

    // Pointer move listener on window so mouse tracking works smoothly anywhere
    const handlePointerMove = (e: PointerEvent) => {
      mouseRef.current.target.x = e.clientX;
      mouseRef.current.target.y = e.clientY;
      mouseRef.current.active = true;
    };

    const handlePointerLeave = () => {
      mouseRef.current.active = false;
      mouseRef.current.target.x = -1000;
      mouseRef.current.target.y = -1000;
    };

    // Click shockwave ripple
    const handlePointerDown = (e: PointerEvent) => {
      shockwavesRef.current.push({
        x: e.clientX,
        y: e.clientY,
        radius: 0,
        maxRadius: Math.max(width, height) * 0.45,
        alpha: 0.85,
      });
      // Cap maximum simultaneous shockwaves
      if (shockwavesRef.current.length > 5) {
        shockwavesRef.current.shift();
      }
    };

    window.addEventListener("pointermove", handlePointerMove, { passive: true });
    window.addEventListener("pointerleave", handlePointerLeave, { passive: true });
    window.addEventListener("pointerdown", handlePointerDown, { passive: true });

    // Check for reduced motion preference
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    let isReducedMotion = mediaQuery.matches;
    const handleReducedMotionChange = (e: MediaQueryListEvent) => {
      isReducedMotion = e.matches;
    };
    mediaQuery.addEventListener("change", handleReducedMotionChange);

    // Color definitions based on theme
    const isLight = theme === "light";

    // Palette tokens
    const PALETTE = isLight
      ? {
          minorLine: "rgba(15, 23, 42, 0.05)",
          majorLine: "rgba(15, 23, 42, 0.12)",
          dotNormal: "rgba(2, 132, 199, 0.25)",
          spotlightMinor: "rgba(2, 132, 199, 0.45)",
          spotlightMajor: "rgba(2, 132, 199, 0.85)",
          spotlightGlow: "rgba(2, 132, 199, 0.12)",
          spotlightDot: "rgba(2, 132, 199, 0.95)",
          perspectiveHorizon: "rgba(2, 132, 199, 0.08)",
          perspectiveLines: "rgba(15, 23, 42, 0.12)",
          packetCyan: "rgba(2, 132, 199, 0.95)",
          packetViolet: "rgba(124, 58, 237, 0.9)",
          packetTeal: "rgba(13, 148, 136, 0.9)",
          packetAmber: "rgba(217, 119, 6, 0.9)",
          shockwave: "rgba(2, 132, 199, 0.65)",
        }
      : {
          minorLine: "rgba(56, 189, 248, 0.06)",
          majorLine: "rgba(148, 163, 184, 0.15)",
          dotNormal: "rgba(56, 189, 248, 0.35)",
          spotlightMinor: "rgba(56, 189, 248, 0.55)",
          spotlightMajor: "rgba(56, 189, 248, 0.95)",
          spotlightGlow: "rgba(14, 165, 233, 0.16)",
          spotlightDot: "rgba(56, 189, 248, 1)",
          perspectiveHorizon: "rgba(14, 165, 233, 0.12)",
          perspectiveLines: "rgba(56, 189, 248, 0.14)",
          packetCyan: "rgba(56, 189, 248, 0.95)",
          packetViolet: "rgba(168, 85, 247, 0.92)",
          packetTeal: "rgba(45, 212, 191, 0.9)",
          packetAmber: "rgba(251, 191, 36, 0.9)",
          shockwave: "rgba(56, 189, 248, 0.75)",
        };

    // Main 60fps render loop
    const render = (timestamp: number) => {
      const dt = Math.min((timestamp - lastTimeRef.current) / 1000, 0.1);
      lastTimeRef.current = timestamp;

      // Clear frame
      ctx.clearRect(0, 0, width, height);

      // Smooth mouse interpolation (physical spring/damping)
      const mouse = mouseRef.current;
      if (mouse.active) {
        mouse.current.x += (mouse.target.x - mouse.current.x) * 0.12;
        mouse.current.y += (mouse.target.y - mouse.current.y) * 0.12;
      } else {
        mouse.current.x += (-1000 - mouse.current.x) * 0.05;
        mouse.current.y += (-1000 - mouse.current.y) * 0.05;
      }

      // Parallax 3D tilt offset calculation
      const centerX = width * 0.5;
      const centerY = height * 0.5;
      const normMouseX = mouse.active ? (mouse.current.x - centerX) / centerX : 0;
      const normMouseY = mouse.active ? (mouse.current.y - centerY) / centerY : 0;

      // Infinite drift velocity
      if (!isReducedMotion) {
        driftRef.current.x = (driftRef.current.x + dt * 10) % CELL_SIZE;
        driftRef.current.y = (driftRef.current.y + dt * 6) % CELL_SIZE;
      }

      const offsetX = driftRef.current.x + normMouseX * 12;
      const offsetY = driftRef.current.y + normMouseY * 12;

      // -------------------------------------------------------------
      // 1. RENDER 3D PERSPECTIVE HORIZON GROUND PLANE (Lower Viewport)
      // -------------------------------------------------------------
      const horizonY = height * 0.58;
      const groundHeight = height - horizonY;

      if (groundHeight > 50) {
        ctx.save();
        // Atmospheric Horizon Soft Glow
        const horizonGlow = ctx.createLinearGradient(0, horizonY - 40, 0, horizonY + 60);
        horizonGlow.addColorStop(0, "transparent");
        horizonGlow.addColorStop(0.4, PALETTE.perspectiveHorizon);
        horizonGlow.addColorStop(1, "transparent");
        ctx.fillStyle = horizonGlow;
        ctx.fillRect(0, horizonY - 40, width, 100);

        // Horizon vanishing point with smooth horizontal mouse parallax
        const vanishingPointX = centerX + normMouseX * 60;

        // Receding longitudinal lines (perspective fan)
        const fanSpacing = 64;
        const totalFanLines = Math.ceil(width / fanSpacing) + 12;
        const startX = -6 * fanSpacing;

        ctx.lineWidth = 0.8;
        ctx.strokeStyle = PALETTE.perspectiveLines;

        for (let i = 0; i <= totalFanLines; i++) {
          const bottomX = startX + i * fanSpacing + (driftRef.current.x % fanSpacing);
          ctx.beginPath();
          ctx.moveTo(vanishingPointX, horizonY);
          ctx.lineTo(bottomX, height);
          ctx.stroke();
        }

        // Transverse horizontal lines with exponential 3D perspective foreshortening
        const numDepthLines = 14;
        const speedOffset = !isReducedMotion ? ((timestamp * 0.0003) % 1) : 0;

        for (let i = 1; i <= numDepthLines; i++) {
          // Perspective mapping: t goes from 0 near horizon to 1 at bottom
          const t = Math.pow((i - 1 + speedOffset) / numDepthLines, 2.3);
          const lineY = horizonY + t * groundHeight;

          // Depth fog attenuation: closer lines are crisper, distant lines fade away
          const depthAlpha = Math.min(1, Math.max(0, t * 0.85));
          ctx.strokeStyle = isLight
            ? `rgba(15, 23, 42, ${0.03 + depthAlpha * 0.12})`
            : `rgba(56, 189, 248, ${0.03 + depthAlpha * 0.16})`;
          ctx.lineWidth = 0.5 + t * 0.9;

          ctx.beginPath();
          ctx.moveTo(0, lineY);
          ctx.lineTo(width, lineY);
          ctx.stroke();
        }
        ctx.restore();
      }

      // -------------------------------------------------------------
      // 2. RENDER FULL-SCREEN HOLOGRAPHIC 2D/3D TECHNICAL MATRIX
      // -------------------------------------------------------------
      const startGridX = (offsetX % CELL_SIZE) - CELL_SIZE;
      const startGridY = (offsetY % CELL_SIZE) - CELL_SIZE;

      // Draw Base Vertical Lines
      ctx.lineWidth = 0.6;
      for (let x = startGridX, index = 0; x <= width + CELL_SIZE; x += CELL_SIZE, index++) {
        const isMajor = Math.round((x - offsetX) / CELL_SIZE) % MAJOR_STEP === 0;
        ctx.strokeStyle = isMajor ? PALETTE.majorLine : PALETTE.minorLine;
        ctx.lineWidth = isMajor ? 0.9 : 0.5;

        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }

      // Draw Base Horizontal Lines
      for (let y = startGridY, index = 0; y <= height + CELL_SIZE; y += CELL_SIZE, index++) {
        const isMajor = Math.round((y - offsetY) / CELL_SIZE) % MAJOR_STEP === 0;
        ctx.strokeStyle = isMajor ? PALETTE.majorLine : PALETTE.minorLine;
        ctx.lineWidth = isMajor ? 0.9 : 0.5;

        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // -------------------------------------------------------------
      // 3. INTERACTIVE POINTER SPOTLIGHT (Photometric Inverse-Square Falloff)
      // -------------------------------------------------------------
      const spotX = mouse.current.x;
      const spotY = mouse.current.y;
      const spotRadius = 320;

      if (spotX > -spotRadius && spotX < width + spotRadius && spotY > -spotRadius && spotY < height + spotRadius) {
        ctx.save();
        // Radial aura glow around cursor
        const radialAura = ctx.createRadialGradient(spotX, spotY, 0, spotX, spotY, spotRadius);
        radialAura.addColorStop(0, PALETTE.spotlightGlow);
        radialAura.addColorStop(0.5, isLight ? "rgba(2, 132, 199, 0.04)" : "rgba(14, 165, 233, 0.05)");
        radialAura.addColorStop(1, "transparent");
        ctx.fillStyle = radialAura;
        ctx.beginPath();
        ctx.arc(spotX, spotY, spotRadius, 0, Math.PI * 2);
        ctx.fill();

        // Highlight grid segments under spotlight with high precision
        const minX = Math.max(0, spotX - spotRadius);
        const maxX = Math.min(width, spotX + spotRadius);
        const minY = Math.max(0, spotY - spotRadius);
        const maxY = Math.min(height, spotY + spotRadius);

        // Illuminated Vertical Grid Segments
        for (let x = startGridX; x <= width + CELL_SIZE; x += CELL_SIZE) {
          if (x >= minX && x <= maxX) {
            const distFromCenter = Math.abs(x - spotX);
            const intensity = Math.pow(1 - distFromCenter / spotRadius, 2);
            const isMajor = Math.round((x - offsetX) / CELL_SIZE) % MAJOR_STEP === 0;

            ctx.strokeStyle = isMajor ? PALETTE.spotlightMajor : PALETTE.spotlightMinor;
            ctx.lineWidth = isMajor ? 1.6 : 1.0;
            ctx.globalAlpha = intensity * (isMajor ? 0.95 : 0.65);

            ctx.beginPath();
            ctx.moveTo(x, minY);
            ctx.lineTo(x, maxY);
            ctx.stroke();
          }
        }

        // Illuminated Horizontal Grid Segments
        for (let y = startGridY; y <= height + CELL_SIZE; y += CELL_SIZE) {
          if (y >= minY && y <= maxY) {
            const distFromCenter = Math.abs(y - spotY);
            const intensity = Math.pow(1 - distFromCenter / spotRadius, 2);
            const isMajor = Math.round((y - offsetY) / CELL_SIZE) % MAJOR_STEP === 0;

            ctx.strokeStyle = isMajor ? PALETTE.spotlightMajor : PALETTE.spotlightMinor;
            ctx.lineWidth = isMajor ? 1.6 : 1.0;
            ctx.globalAlpha = intensity * (isMajor ? 0.95 : 0.65);

            ctx.beginPath();
            ctx.moveTo(minX, y);
            ctx.lineTo(maxX, y);
            ctx.stroke();
          }
        }

        // Illuminated Intersection Crosshairs & Quantum Nodes under spotlight
        ctx.globalAlpha = 1;
        for (let x = startGridX; x <= width + CELL_SIZE; x += CELL_SIZE) {
          if (x >= minX && x <= maxX) {
            for (let y = startGridY; y <= height + CELL_SIZE; y += CELL_SIZE) {
              if (y >= minY && y <= maxY) {
                const distSq = (x - spotX) * (x - spotX) + (y - spotY) * (y - spotY);
                if (distSq < spotRadius * spotRadius) {
                  const dist = Math.sqrt(distSq);
                  const nodeIntensity = Math.pow(1 - dist / spotRadius, 2);

                  // Glowing center diamond / micro-circle
                  ctx.fillStyle = PALETTE.spotlightDot;
                  ctx.globalAlpha = nodeIntensity * 0.9;
                  ctx.beginPath();
                  ctx.arc(x, y, 1.8 + nodeIntensity * 1.5, 0, Math.PI * 2);
                  ctx.fill();

                  // Subtle micro-crosshair on major intersections
                  const isMajorCross =
                    Math.round((x - offsetX) / CELL_SIZE) % MAJOR_STEP === 0 &&
                    Math.round((y - offsetY) / CELL_SIZE) % MAJOR_STEP === 0;

                  if (isMajorCross && nodeIntensity > 0.25) {
                    ctx.strokeStyle = PALETTE.spotlightMajor;
                    ctx.lineWidth = 1;
                    ctx.globalAlpha = nodeIntensity * 0.8;
                    const arm = 4 + nodeIntensity * 3;
                    ctx.beginPath();
                    ctx.moveTo(x - arm, y);
                    ctx.lineTo(x + arm, y);
                    ctx.moveTo(x, y - arm);
                    ctx.lineTo(x, y + arm);
                    ctx.stroke();
                  }
                }
              }
            }
          }
        }
        ctx.restore();
      }

      // -------------------------------------------------------------
      // 4. ALGORITHMIC DATA PACKETS (Laser Signals Travelling Along Grid)
      // -------------------------------------------------------------
      if (!isReducedMotion && packetsRef.current.length > 0) {
        ctx.save();
        for (const packet of packetsRef.current) {
          // Advance packet position
          packet.pos += packet.speed * dt * 60;

          const isHorizontal = packet.axis === "horizontal";
          const maxDimension = isHorizontal ? width : height;

          // Wrap around or re-seed when off-screen
          if (packet.speed > 0 && packet.pos > maxDimension + packet.length) {
            packet.pos = -packet.length;
            const numLines = isHorizontal ? Math.floor(height / CELL_SIZE) : Math.floor(width / CELL_SIZE);
            packet.lineCoord = Math.floor(Math.random() * numLines) * CELL_SIZE;
          } else if (packet.speed < 0 && packet.pos < -packet.length) {
            packet.pos = maxDimension + packet.length;
            const numLines = isHorizontal ? Math.floor(height / CELL_SIZE) : Math.floor(width / CELL_SIZE);
            packet.lineCoord = Math.floor(Math.random() * numLines) * CELL_SIZE;
          }

          // Compute screen coordinate aligned with drifting grid
          const linePos = isHorizontal
            ? packet.lineCoord + (offsetY % CELL_SIZE)
            : packet.lineCoord + (offsetX % CELL_SIZE);

          const headPos = packet.pos;
          const tailPos = packet.pos - Math.sign(packet.speed) * packet.length;

          const packetColor =
            packet.colorType === "cyan"
              ? PALETTE.packetCyan
              : packet.colorType === "violet"
              ? PALETTE.packetViolet
              : packet.colorType === "teal"
              ? PALETTE.packetTeal
              : PALETTE.packetAmber;

          // Create smooth phosphor fading trail gradient
          let grad: CanvasGradient;
          if (isHorizontal) {
            grad = ctx.createLinearGradient(tailPos, linePos, headPos, linePos);
          } else {
            grad = ctx.createLinearGradient(linePos, tailPos, linePos, headPos);
          }

          grad.addColorStop(0, "transparent");
          grad.addColorStop(0.7, packetColor.replace("0.95", "0.45").replace("0.9", "0.4"));
          grad.addColorStop(1, packetColor);

          ctx.strokeStyle = grad;
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          if (isHorizontal) {
            ctx.moveTo(tailPos, linePos);
            ctx.lineTo(headPos, linePos);
          } else {
            ctx.moveTo(linePos, tailPos);
            ctx.lineTo(linePos, headPos);
          }
          ctx.stroke();

          // Luminous packet head glow dot
          const headX = isHorizontal ? headPos : linePos;
          const headY = isHorizontal ? linePos : headPos;

          if (headX >= 0 && headX <= width && headY >= 0 && headY <= height) {
            ctx.fillStyle = packetColor;
            ctx.beginPath();
            ctx.arc(headX, headY, 2.2, 0, Math.PI * 2);
            ctx.fill();

            // Intersection flare when crossing perpendicular grid line
            const perpDist = isHorizontal
              ? Math.abs((headX - offsetX) % CELL_SIZE)
              : Math.abs((headY - offsetY) % CELL_SIZE);

            if (perpDist < 3 || perpDist > CELL_SIZE - 3) {
              ctx.fillStyle = isLight ? "#ffffff" : "#e0f2fe";
              ctx.beginPath();
              ctx.arc(headX, headY, 3.2, 0, Math.PI * 2);
              ctx.fill();
            }
          }
        }
        ctx.restore();
      }

      // -------------------------------------------------------------
      // 5. CLICK SHOCKWAVE ENERGY RIPPLES (Kinetic Quantum Waves)
      // -------------------------------------------------------------
      if (shockwavesRef.current.length > 0) {
        ctx.save();
        for (let i = shockwavesRef.current.length - 1; i >= 0; i--) {
          const wave = shockwavesRef.current[i];
          wave.radius += dt * 380;
          wave.alpha = Math.max(0, 1 - wave.radius / wave.maxRadius);

          if (wave.alpha <= 0 || wave.radius >= wave.maxRadius) {
            shockwavesRef.current.splice(i, 1);
            continue;
          }

          // Draw expanding wave ring that activates grid lines
          ctx.strokeStyle = PALETTE.shockwave;
          ctx.lineWidth = 2.2 * wave.alpha;
          ctx.globalAlpha = wave.alpha * 0.75;

          ctx.beginPath();
          ctx.arc(wave.x, wave.y, wave.radius, 0, Math.PI * 2);
          ctx.stroke();

          // Secondary subtle inner echo ring
          if (wave.radius > 30) {
            ctx.lineWidth = 1.0 * wave.alpha;
            ctx.globalAlpha = wave.alpha * 0.35;
            ctx.beginPath();
            ctx.arc(wave.x, wave.y, wave.radius - 24, 0, Math.PI * 2);
            ctx.stroke();
          }
        }
        ctx.restore();
      }

      // Request next frame
      animFrameIdRef.current = requestAnimationFrame(render);
    };

    // Pause animation when tab is hidden to save GPU & battery
    const handleVisibilityChange = () => {
      if (document.hidden) {
        if (animFrameIdRef.current) {
          cancelAnimationFrame(animFrameIdRef.current);
          animFrameIdRef.current = null;
        }
      } else {
        lastTimeRef.current = performance.now();
        animFrameIdRef.current = requestAnimationFrame(render);
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    animFrameIdRef.current = requestAnimationFrame(render);

    return () => {
      if (animFrameIdRef.current) {
        cancelAnimationFrame(animFrameIdRef.current);
      }
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("pointerleave", handlePointerLeave);
      window.removeEventListener("pointerdown", handlePointerDown);
      mediaQuery.removeEventListener("change", handleReducedMotionChange);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [theme, initPackets]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none block z-0"
      style={{ willChange: "transform, opacity" }}
      aria-hidden="true"
    />
  );
}

export default RealisticGridCanvas;

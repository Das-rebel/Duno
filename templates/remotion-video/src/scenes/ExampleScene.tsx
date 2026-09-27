import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { C, SANS, MONO, rand } from "../theme";

// Reference patterns: typewriter, number slam + shake, particle field, staged reveals.
export const ExampleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const head = "The invoice nobody budgets for.";
  const chars = Math.floor(interpolate(frame, [8, 80], [0, head.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const slam = spring({ frame: frame - 96, fps, config: { damping: 11, stiffness: 130, mass: 0.9 }, from: 2.6, to: 1 });
  const t = frame - 118;
  const shake = t > 0 ? Math.sin(t * 0.9) * 14 * Math.exp(-t / 7) : 0;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg, justifyContent: "center", alignItems: "center" }}>
      {Array.from({ length: 42 }).map((_, i) => (
        <div key={i} style={{ position: "absolute", left: `${rand(i, 1) * 100}%`, top: `${rand(i, 2) * 100}%`,
          width: 2 + rand(i, 3) * 5, height: 2 + rand(i, 3) * 5, borderRadius: "50%",
          background: i % 5 ? C.green : C.blue, opacity: 0.08 + 0.2 * (0.5 + 0.5 * Math.sin(frame / 18 + i * 1.7)) }} />
      ))}
      <div style={{ textAlign: "center", fontFamily: MONO }}>
        <div style={{ fontSize: 44, color: C.dim, fontFamily: SANS, fontWeight: 600 }}>{head.slice(0, chars)}</div>
        <div style={{ fontSize: 220, fontWeight: 900, color: C.red, letterSpacing: -5,
          transform: `scale(${slam}) translateX(${shake}px)`, opacity: frame >= 96 ? 1 : 0 }}>$9,999</div>
      </div>
    </AbsoluteFill>
  );
};

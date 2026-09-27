import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { C, SANS, MONO, rand } from "../theme";

const Particles: React.FC = () => (
  <AbsoluteFill>
    {Array.from({ length: 40 }).map((_, i) => (
      <div key={i} style={{ position: "absolute", left: `${rand(i, 1) * 100}%`, top: `${rand(i, 2) * 100}%`,
        width: 2 + rand(i, 3) * 5, height: 2 + rand(i, 3) * 5, borderRadius: "50%",
        background: i % 5 ? C.green : C.blue, opacity: 0.08 + 0.2 * (0.5 + 0.5 * Math.sin(i * 1.7)) }} />
    ))}
  </AbsoluteFill>
);

// Variant A — PAIN NUMBER: "invoice" typewriter → $ figure slams
export const HookSlam: React.FC<{ figure?: string; lead?: string }> = ({ figure = "$9,999", lead = "The invoice nobody budgets for." }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const chars = Math.floor(interpolate(frame, [8, 80], [0, lead.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const slam = spring({ frame: frame - 96, fps, config: { damping: 11, stiffness: 130, mass: 0.9 }, from: 2.6, to: 1 });
  const t = frame - 118;
  const shake = t > 0 ? Math.sin(t * 0.9) * 14 * Math.exp(-t / 7) : 0;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg, justifyContent: "center", alignItems: "center" }}>
      <Particles />
      <div style={{ textAlign: "center", fontFamily: MONO }}>
        <div style={{ fontSize: 44, color: C.dim, fontFamily: SANS, fontWeight: 600 }}>{lead.slice(0, chars)}</div>
        <div style={{ fontSize: 220, fontWeight: 900, color: C.red, letterSpacing: -5,
          transform: `scale(${slam}) translateX(${shake}px)`, opacity: frame >= 96 ? 1 : 0 }}>{figure}</div>
      </div>
    </AbsoluteFill>
  );
};

// Variant B — QUESTION: "What did your last AI month cost?" types → "?" pulses red
export const HookQuestion: React.FC = () => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const q = "What did your last AI month cost?";
  const chars = Math.floor(interpolate(frame, [10, 90], [0, q.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const blink = frame > 100 ? (0.5 + 0.5 * Math.sin(frame / 5)) : 0;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg, justifyContent: "center", alignItems: "center" }}>
      <Particles />
      <div style={{ fontSize: 84, fontFamily: SANS, fontWeight: 800, color: C.white, maxWidth: 1300, textAlign: "center" }}>
        {q.slice(0, chars)}<span style={{ color: C.red, opacity: blink }}>?</span>
      </div>
    </AbsoluteFill>
  );
};

// Variant C — BEFORE/AFTER: two bills stack, second one clips 99%
export const HookDelta: React.FC<{ before?: string; after?: string }> = ({ before = "$9,999", after = "$64" }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const s1 = spring({ frame: frame - 20, fps, config: { damping: 13 } });
  const s2 = spring({ frame: frame - 90, fps, config: { damping: 12, stiffness: 110 } });
  const strike = interpolate(frame, [100, 125], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg, justifyContent: "center", alignItems: "center" }}>
      <Particles />
      <div style={{ textAlign: "center", fontFamily: MONO }}>
        <div style={{ fontSize: 96, color: C.red, opacity: s1, textDecoration: "line-through",
          textDecorationThickness: 5, textDecorationColor: `rgba(239,68,68,${strike}%)` }}>{before}</div>
        <div style={{ fontSize: 34, color: C.dim, margin: "18px 0", opacity: s2 }}>→ routed</div>
        <div style={{ fontSize: 150, fontWeight: 900, color: C.green, transform: `scale(${s2})` }}>{after}</div>
      </div>
    </AbsoluteFill>
  );
};

export const HOOK_VARIANTS = { slam: HookSlam, question: HookQuestion, delta: HookDelta } as const;
export type HookVariant = keyof typeof HOOK_VARIANTS;

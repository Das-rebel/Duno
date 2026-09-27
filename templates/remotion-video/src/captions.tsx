import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

export interface WordCaption { word: string; startMs: number; endMs: number }

// paste your whisper segments here: [startSec, endSec, text]
const SEGMENTS: [number, number, string][] = [
  [0.0, 3.0, "Your first beat goes here."],
];

export const buildWords = (perPageMax = 6): WordCaption[] => {
  const words: WordCaption[] = [];
  for (const [start, end, text] of SEGMENTS) {
    const parts = text.split(/\s+/).filter(Boolean);
    const span = (end - start) / parts.length;
    parts.forEach((w, i) => words.push({
      word: w,
      startMs: Math.round((start + i * span) * 1000),
      endMs: Math.round((start + (i + 1) * span) * 1000),
    }));
  }
  return words;
};

export const CaptionOverlay: React.FC<{ words: WordCaption[]; color?: string; highlight?: string }> = ({
  words, color = "#E6F1E6", highlight = "#2EE59D",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const now = (frame / fps) * 1000;
  const active = words.findIndex((w) => now >= w.startMs && now < w.endMs);
  if (active === -1) return null;
  const pageStart = Math.floor(active / 6) * 6;
  const page = words.slice(pageStart, pageStart + 6);
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 72, pointerEvents: "none" }}>
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", justifyContent: "center",
        background: "rgba(8,10,8,0.72)", padding: "14px 28px", borderRadius: 16, maxWidth: "72%" }}>
        {page.map((w, i) => {
          const idx = pageStart + i;
          const isActive = idx === active;
          const isPast = idx < active;
          return (
            <span key={idx} style={{
              fontFamily: '"SF Mono", Menlo, monospace', fontSize: 40, fontWeight: 700,
              color: isActive ? highlight : isPast ? color : `${color}88`,
              transition: "none",
            }}>{w.word}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

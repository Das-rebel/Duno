export const C = {
  bg: "#0A0E0A", green: "#2EE59D", blue: "#60A5FA", amber: "#FFC857",
  red: "#EF4444", white: "#E6F1E6", dim: "#8CAA96", purple: "#B482FF",
};
export const SANS = '"SF Pro Display", -apple-system, "Inter", sans-serif';
export const MONO = '"SF Mono", Menlo, monospace';
// deterministic pseudo-random — Math.random() is banned in Remotion renders
export const rand = (i: number, salt = 1): number => {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
};
export const FPS = 30;
export const FADE = 15; // 0.5s crossfade
// EDIT ME: scene durations (frames). TOTAL must equal sum - (n-1)*FADE
export const DUR = { hook: 285, thesis: 147, mechanism: 375, architecture: 453, proof: 279, cta: 571 };
export const TOTAL = Object.values(DUR).reduce((a, b) => a + b, 0) - 5 * FADE;

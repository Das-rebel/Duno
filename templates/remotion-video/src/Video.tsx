import React from "react";
import { AbsoluteFill, Audio, staticFile, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { C, DUR, FADE, TOTAL } from "./theme";
import { HOOK_VARIANTS, HookSlam } from "./scenes/Hooks";
import { CaptionOverlay, buildWords } from "./captions";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const EndFade = React.forwardRef<HTMLDivElement>((_, ref) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const op = interpolate(frame, [durationInFrames - 28, durationInFrames - 3], [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ backgroundColor: "#000", opacity: op }} />;
});
EndFade.displayName = "EndFade";

export interface VideoProps { hookVariant?: keyof typeof HOOK_VARIANTS; figure?: string; after?: string }

// Replace the placeholder beats with your real scenes; keep boundaries inside VO gaps.
export const Video: React.FC<VideoProps> = ({ hookVariant = "slam", figure, after }) => {
  const Hook = HOOK_VARIANTS[hookVariant] ?? HookSlam;
  const hookNode = hookVariant === "delta"
    ? <HookDeltaSafe figure={figure} after={after} />
    : hookVariant === "slam"
      ? <HookSlam figure={figure} />
      : <Hook />;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={DUR.hook}>{hookNode}</TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: FADE })} />
        <TransitionSeries.Sequence durationInFrames={DUR.thesis}><ExampleScene /></TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: FADE })} />
        <TransitionSeries.Sequence durationInFrames={DUR.mechanism}><ExampleScene /></TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: FADE })} />
        <TransitionSeries.Sequence durationInFrames={DUR.architecture}><ExampleScene /></TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: FADE })} />
        <TransitionSeries.Sequence durationInFrames={DUR.proof}><ExampleScene /></TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: FADE })} />
        <TransitionSeries.Sequence durationInFrames={DUR.cta}><ExampleScene /></TransitionSeries.Sequence>
      </TransitionSeries>
      <CaptionOverlay words={buildWords()} />
      <EndFade />
      <Audio src={staticFile("voiceover.mp3")} />
      <Audio src={staticFile("music.mp3")} volume={(f) => interpolate(f, [0, 45], [0, 0.12], { extrapolateRight: "clamp" })} />
    </AbsoluteFill>
  );
};

// thin wrapper keeps the delta variant's optional props type-safe
import { HookDelta } from "./scenes/Hooks";
const HookDeltaSafe: React.FC<{ figure?: string; after?: string }> = ({ figure, after }) =>
  <HookDelta before={figure} after={after} />;

import { ExampleScene } from "./scenes/ExampleScene";

// single source of truth — throws at bundle time if DUR and TOTAL diverge
const sum = Object.values(DUR).reduce((a, b) => a + b, 0);
if (sum - 5 * FADE !== TOTAL) throw new Error(`DUR sum ${sum - 5 * FADE} != TOTAL ${TOTAL}`);

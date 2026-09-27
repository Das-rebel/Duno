import React from "react";
import { AbsoluteFill, Audio, staticFile, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { C, DUR, FADE, TOTAL } from "./theme";
import { ExampleScene } from "./scenes/ExampleScene";
import { CaptionOverlay, buildWords } from "./captions";

const EndFade: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const op = interpolate(frame, [durationInFrames - 28, durationInFrames - 3], [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ backgroundColor: "#000", opacity: op }} />;
};

// Replace ExampleScene with your 6 beat scenes; keep boundaries inside VO gaps.
export const Video: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.bg }}>
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={DUR.hook}><ExampleScene /></TransitionSeries.Sequence>
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

// keep TOTAL honest — if this throws, fix DUR, not this file.
const sum = Object.values(DUR).reduce((a, b) => a + b, 0);
if (sum - 5 * FADE !== TOTAL) throw new Error(`DUR sum ${sum - 5 * FADE} != TOTAL ${TOTAL}`);

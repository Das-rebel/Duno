import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import { ExampleScene } from "./scenes/ExampleScene";
import { TOTAL } from "./theme";

export const Root: React.FC = () => (
  <>
    <Composition
      id="Video"
      component={Video}
      durationInFrames={TOTAL}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{ hookVariant: "slam" }}
    />
    <Composition id="Thumb" component={ExampleScene} durationInFrames={300} fps={30} width={1920} height={1080} />
  </>
);

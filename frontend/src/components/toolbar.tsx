import { PauseButton } from "./pause_button";
import { StartButton } from "./start_button";
import { StopButton } from "./stop_button";

export const Toolbar = () => {
  return (
    <div
      style={{
        display: "flex",
        gap: "1rem",
        padding: "1rem",
      }}
    >
      <StartButton />
      <PauseButton />
      <StopButton />
    </div>
  );
};

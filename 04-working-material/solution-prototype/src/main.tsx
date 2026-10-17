import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Theme } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import "@fontsource/barlow/latin-400.css";
import "@fontsource/barlow/latin-500.css";
import "@fontsource/barlow/latin-600.css";
import "@fontsource/barlow/latin-700.css";
import "./theme.css";
import { StoreProvider } from "./data/store";
import { App } from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Theme accentColor="pink" grayColor="slate" radius="medium" scaling="100%">
      <StoreProvider>
        <App />
      </StoreProvider>
    </Theme>
  </StrictMode>,
);

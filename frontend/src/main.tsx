import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./app/App";
import { I18nProvider } from "./shared/i18n";
import { DisplayProvider } from "./shared/display";
import "./app/styles.css";

createRoot(document.getElementById("root")!).render(
  <React.StrictMode><BrowserRouter><I18nProvider><DisplayProvider><App /></DisplayProvider></I18nProvider></BrowserRouter></React.StrictMode>
);
if ("serviceWorker" in navigator && import.meta.env.PROD) navigator.serviceWorker.register("/sw.js");

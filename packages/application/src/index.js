import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import { Provider } from "react-redux";

import App from "./App";
import { store } from "./app/store";
import { APP_URL } from "./api/utils";
import Assignments from "./features/assignments/Assignments";

ReactDOM.createRoot(document.querySelector("#root")).render(
  <Provider store={store}>
    <BrowserRouter>
      <Routes>
        <Route path={APP_URL} element={<App />}>
          <Route path="assignments" element={<Assignments />} />
          <Route index element={<Navigate to="assignments" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </Provider>
);


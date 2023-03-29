import { Outlet } from "react-router-dom";
import NavbarLeft from "./nav/NavbarLeft";

import { ThemeProvider } from "@mui/material/styles";

import { theme } from "./theme/theme";

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <NavbarLeft>
        <Outlet />
      </NavbarLeft>
    </ThemeProvider>
  );
}

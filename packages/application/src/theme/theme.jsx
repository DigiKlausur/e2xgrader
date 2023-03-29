import { createTheme } from "@mui/material/styles";
import { blue, grey, green, orange } from "@mui/material/colors";

export const theme = createTheme({
  palette: {
    primary: {
      main: blue[500],
    },
    cell: {
      default: grey[200],
      solution: green[200],
      description: blue[300],
      test: orange[100],
    }
  },
  listIcon: {
    color: blue[500],
  },
  
});

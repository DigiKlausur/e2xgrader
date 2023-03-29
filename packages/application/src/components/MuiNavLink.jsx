import { Link as RouterLink } from "react-router-dom";
import { Link } from "@mui/material";

export default function MuiNavLink({ to, ...props }) {
  return (
    <Link component={RouterLink} to={to} underline="hover">
      {props.children}
    </Link>
  );
}

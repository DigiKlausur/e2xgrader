import React from "react";
import { Breadcrumbs, Typography } from "@mui/material";

import AssignmentsTable from "./AssignmentsTable";

export default function Assignments() {
  return (
    <>
      <Breadcrumbs separator=">">
        <Typography color="text.primary">Assignments</Typography>
      </Breadcrumbs>
      <AssignmentsTable />
    </>
  );
}

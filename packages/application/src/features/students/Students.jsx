import React from "react";
import { Breadcrumbs, Typography } from "@mui/material";

import StudentsTable from "./StudentsTable";

export default function Students() {
  return (
    <>
      <Breadcrumbs separator=">">
        <Typography color="text.primary">Students</Typography>
      </Breadcrumbs>
      <StudentsTable />
    </>
  );
}

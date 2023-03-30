import React from "react";
import { Breadcrumbs, Stack, Typography } from "@mui/material";

import StudentsTable from "./StudentsTable";
import AddStudentDialog from "./AddStudentDialog";

export default function Students() {
  return (
    <Stack spacing={2}>
      <Breadcrumbs separator=">">
        <Typography color="text.primary">Students</Typography>
      </Breadcrumbs>
      <StudentsTable />
      <Stack direction="row">
        <AddStudentDialog />
      </Stack>
    </Stack>
  );
}

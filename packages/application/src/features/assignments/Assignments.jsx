import React from "react";
import { Breadcrumbs, Stack, Typography } from "@mui/material";

import AssignmentsTable from "./AssignmentsTable";
import AddAssignmentDialog from "./AddAssignmentDialog";

export default function Assignments() {
  return (
    <Stack spacing={2}>
      <Breadcrumbs separator=">">
        <Typography color="text.primary">Assignments</Typography>
      </Breadcrumbs>
      <AssignmentsTable />
      <Stack direction="row">
        <AddAssignmentDialog />
      </Stack>
    </Stack>
  );
}

import React from "react";
import { Chip } from "@mui/material";
import format from "date-fns/format";

import DataTable from "../../components/DataTable";
import MuiNavLink from "../../components/MuiNavLink";
import { APP_URL, urlJoin } from "../../api/utils";
import { useGetAssignmentsQuery } from "../../api/assignmentApi";

function AssignmentStatus({ status, numberOfSubmissions }) {
  const colors = {
    draft: "primary",
    released: "warning",
  };
  if (status === "draft" && numberOfSubmissions > 0) {
    return (
      <Chip size="small" label="returned" color="success" variant="outlined" />
    );
  } else {
    return (
      <Chip
        size="small"
        label={status}
        color={colors[status]}
        variant="outlined"
      />
    );
  }
}

export default function AssignmentsTable() {
  const { data, isLoading, isError, error } = useGetAssignmentsQuery();

  const columns = React.useMemo(() => [
    {
      field: "name",
      headerName: "Name",
      flex: 2,
      renderCell: (params) => (
        <MuiNavLink to={urlJoin(APP_URL, "assignments", params.row.name)}>
          {params.row.name}
        </MuiNavLink>
      ),
    },
    {
      field: "duedate",
      headerName: "Due Date",
      flex: 1,
      valueGetter: (params) =>
        `${
          params.row.duedate !== null
            ? format(new Date(params.row.duedate), "yyyy-MM-dd HH:mm:ss OOOO")
            : "None"
        }`,
    },
    {
      field: "status",
      headerName: "Status",
      flex: 1,
      valueGetter: (params) =>
        `${
          params.row.status === "draft" && params.row.num_submissions > 0
            ? "returned"
            : params.row.status
        }`,
      renderCell: (params) => (
        <AssignmentStatus
          status={params.row.status}
          numberOfSubmissions={params.row.num_submissions}
        />
      ),
    },
    {
      field: "num_submissions",
      headerName: "Number of Submissions",
      flex: 1,
    },
  ]);

  if (isError) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <DataTable
      rows={data}
      columns={columns}
      loading={isLoading}
      getRowId={(row) => row.name}
    />
  );
}

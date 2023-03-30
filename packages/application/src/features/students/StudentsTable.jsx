import React from "react";
import EditIcon from "@mui/icons-material/Edit";

import DataTable from "../../components/DataTable";
import MuiNavLink from "../../components/MuiNavLink";
import { urlJoin, APP_URL } from "../../api/utils";
import { useGetStudentsQuery } from "../../api/studentApi";
import EditStudentDialog from "./EditStudentDialog";
import { IconButton } from "@mui/material";

export default function StudentsTable() {
  const {
    data: students,
    isLoading: studentsLoading,
    error: studentsError,
  } = useGetStudentsQuery();

  const columns = React.useMemo(() => [
    {
      field: "id",
      headerName: "Student ID",
      flex: 1,
    },
    {
      field: "name",
      headerName: "Name",
      flex: 2,
      renderCell: (params) => (
        <MuiNavLink to={urlJoin(APP_URL, "students", params.row.id)}>
          {`${
            params.row.first_name !== null ? params.row.first_name : "None"
          }, ${params.row.last_name !== null ? params.row.last_name : "None"}`}
        </MuiNavLink>
      ),
    },
    {
      field: "email",
      headerName: "Email",
      flex: 2,
      valueGetter: (params) =>
        `${params.row.email === null ? "None" : params.row.email}`,
    },
    {
      field: "score",
      type: "number",
      headerName: "Overall Score",
      flex: 1,
      renderCell: (params) =>
        `${Number(Math.round(params.row.score * 10) / 10).toLocaleString()} / ${
          params.row.max_score
        }`,
    },
    {
      field: "actions",
      type: "actions",
      headerName: "Edit",
      flex: 1,
      getActions: (params) => [
        <EditStudentDialog
          key={params.row.id}
          student={params.row}
          buttonElement={
            <IconButton color="primary">
              <EditIcon />
            </IconButton>
          }
        />,
      ],
    },
  ]);

  return (
    <DataTable
      rows={students}
      loading={studentsLoading}
      columns={columns}
      initialState={{
        sorting: {
          sortModel: [{ field: "id", sort: "asc" }],
        },
      }}
    />
  );
}

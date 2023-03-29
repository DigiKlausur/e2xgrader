import React from "react";

import DataTable from "../../components/DataTable";
import MuiNavLink from "../../components/MuiNavLink";
import { urlJoin, APP_URL } from "../../api/utils";
import { useGetStudentsQuery } from "../../api/studentApi";

export default function StudentsTable() {
  const {
    data: students,
    isLoading: studentsLoading,
    error: studentsError,
  } = useGetStudentsQuery();

  const columns = React.useMemo(() => [
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      renderCell: (params) => (
        <MuiNavLink to={urlJoin(APP_URL, "students", params.row.id)}>
          {`${
            params.row.first_name !== null ? params.row.first_name : "None"
          }, ${params.row.last_name !== null ? params.row.last_name : "None"}`}
        </MuiNavLink>
      ),
    },
    {
      field: "id",
      headerName: "Student ID",
      flex: 1,
    },
    {
      field: "email",
      headerName: "Email",
      flex: 1,
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
  ]);

  return (
    <DataTable rows={students} loading={studentsLoading} columns={columns} />
  );
}

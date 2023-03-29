import React from "react";
import { useParams } from "react-router-dom";
import { Breadcrumbs, Typography } from "@mui/material";

import StudentInfo from "./StudentInfo";
import { useGetStudentQuery } from "../../api/studentApi";
import MuiNavLink from "../../components/MuiNavLink";
import { APP_URL, urlJoin } from "../../api/utils";

export default function Student() {
  const params = useParams();
  const {
    data: student,
    isLoading: studentLoading,
    error: studentError,
  } = useGetStudentQuery(params.student);

  console.log(studentError);

  return (
    <>
      <Breadcrumbs separator=">">
        <MuiNavLink to={urlJoin(APP_URL, "students")}>Students</MuiNavLink>
        <Typography color="text.primary">{params.student}</Typography>
      </Breadcrumbs>
      <>
        {studentLoading ? "Loading" : <></>}
        {student === undefined ? (
          "No student found"
        ) : (
          <StudentInfo student={student} />
        )}
      </>
    </>
  );
}

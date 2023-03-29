import React from "react";
import { useParams } from "react-router-dom";

import StudentInfo from "./StudentInfo";
import { useGetStudentQuery } from "../../api/studentApi";

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
      {studentLoading ? "Loading" : <></>}
      {student === undefined ? (
        "No student found"
      ) : (
        <StudentInfo student={student} />
      )}
    </>
  );
}

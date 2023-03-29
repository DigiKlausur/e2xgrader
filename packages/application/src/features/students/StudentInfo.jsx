import React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Stack,
} from "@mui/material";

import EditStudentDialog from "./EditStudentDialog";

const toString = (value) => {
  if (value === undefined || value === null) {
    return "None";
  }
  return value;
};

export default function StudentInfo({ student }) {
  return (
    <Card sx={{ width: "30ch" }}>
      <CardHeader title={student.id} />
      <CardContent>
        <Stack spacing={2} alignContent="baseline">
          <Table>
            <TableBody>
              <TableRow>
                <TableCell>First Name</TableCell>
                <TableCell>{toString(student.first_name)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Last Name</TableCell>
                <TableCell>{toString(student.last_name)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>EMail</TableCell>
                <TableCell>{toString(student.email)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>LMS User ID</TableCell>
                <TableCell>{toString(student.lms_user_id)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Score</TableCell>
                <TableCell>{`${student.score} / ${student.max_score}`}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
          <EditStudentDialog student={student} />
        </Stack>
      </CardContent>
    </Card>
  );
}

import React from "react";
import * as yup from "yup";
import { useFormik } from "formik";
import { Button, Stack } from "@mui/material";

import FormDialogWithoutButton from "../../components/dialog/FormDialogWithoutButton";
import FormikTextField from "../../components/form/FormikTextField";
import { useCreateOrUpdateStudentMutation } from "../../api/studentApi";

export default function EditStudentDialog({ student }) {
  const [open, setOpen] = React.useState(false);
  const [updateStudent, { isLoading: isUpdating }] =
    useCreateOrUpdateStudentMutation();
  const formik = useFormik({
    initialValues: {
      first_name: student.first_name,
      last_name: student.last_name,
      email: student.email,
    },
    validationSchema: yup.object({
      first_name: yup
        .string()
        .min(2, "The name needs to have at least 2 characters")
        .nullable(),
      last_name: yup
        .string()
        .min(2, "The name needs to have at least 2 characters")
        .nullable(),
      email: yup.string().email().nullable(),
    }),
    onSubmit: (values) => {
      const student_info = {
        id: student.id,
        ...Object.fromEntries(
          Object.entries(values).filter(
            ([key, value]) => value !== null && value !== ""
          )
        ),
      };
      console.log(student.id, student_info);
      const student_id = student.id;
      updateStudent({ studentId: student_id, updatedStudent: student_info });
      if (!isUpdating) {
        setOpen(false);
      }
    },
  });
  const handleClose = () => {
    formik.resetForm();
    setOpen(false);
  };
  return (
    <>
      <Button variant="contained" onClick={() => setOpen(true)}>
        Edit Student
      </Button>
      <FormDialogWithoutButton
        title={`Edit Student Info for ${student.id}`}
        buttonText="Save"
        handleSubmit={formik.handleSubmit}
        open={open}
        handleClose={handleClose}
      >
        <form onSubmit={formik.handleSubmit}>
          <Stack spacing={2} sx={{ width: "30ch" }}>
            <FormikTextField
              formik={formik}
              name="first_name"
              label="First Name"
            />
            <FormikTextField
              formik={formik}
              name="last_name"
              label="Last Name"
            />
            <FormikTextField formik={formik} name="email" label="EMail" />
          </Stack>
        </form>
      </FormDialogWithoutButton>
    </>
  );
}

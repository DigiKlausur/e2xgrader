import React from "react";

import * as yup from "yup";
import { useFormik } from "formik";
import { Button, Stack, TextField } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";

import FormDialogWithoutButton from "../../components/dialog/FormDialogWithoutButton";
import FormikTextField from "../../components/form/FormikTextField";
import { useUpdateOrCreateAssignmentMutation } from "../../api/assignmentApi";

const transformDate = (date) => {
  const duedate_notimezone = date.toISOString().split(".")[0];
  return duedate_notimezone.slice(0, duedate_notimezone.length - 3);
};

export default function AddAssignmentDialog() {
  const [open, setOpen] = React.useState(false);
  const [updateAssignment, { isLoading: isUpdating }] =
    useUpdateOrCreateAssignmentMutation();
  const formik = useFormik({
    initialValues: {
      name: "",
      date: null,
    },
    validationSchema: yup.object({
      name: yup
        .string()
        .min(3, "The assignment name should have at least 2 characters")
        .matches(
          /^[A-Za-z\d]+[\w-]*$/,
          "Name can only consist of letters, digits, '-' and '_'!"
        )
        .required(),
      date: yup
        .date()
        .min(new Date(), "The due date can not be in the past!")
        .nullable(),
    }),
    onSubmit: (values) => {
      const assignment_info = {
        name: values["name"],
      };
      if (values["date"] !== null) {
        assignment_info["duedate_notimezone"] = transformDate(values["date"]);
      }
      updateAssignment({
        assignmentId: assignment_info.name,
        updatedAssignment: assignment_info,
      });
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
        Add Assignment
      </Button>
      <FormDialogWithoutButton
        title={`Add new assignment`}
        buttonText="Add Assignment"
        handleSubmit={formik.handleSubmit}
        open={open}
        handleClose={handleClose}
      >
        <form onSubmit={formik.handleSubmit}>
          <Stack spacing={2} sx={{ width: "30ch" }}>
            <FormikTextField
              formik={formik}
              name="name"
              label="Assignment Name"
            />
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DateTimePicker
                label="Due Date (optional)"
                value={formik.values.date}
                onChange={(newDate) => {
                  formik.setFieldValue("date", newDate);
                }}
                renderInput={(props) => (
                  <TextField
                    {...props}
                    error={formik.touched.date && Boolean(formik.errors.date)}
                    helperText={formik.touched.date && formik.errors.date}
                  />
                )}
              />
            </LocalizationProvider>
          </Stack>
        </form>
      </FormDialogWithoutButton>
    </>
  );
}

import React from "react";
import BaseDialog from "./BaseDialog";
import { Button } from "@mui/material";

export default function FormDialogWithoutButton({
  title,
  handleSubmit,
  buttonText,
  children,
  open,
  handleClose,
}) {
  return (
    <>
      <BaseDialog
        open={open}
        handleClose={handleClose}
        title={title}
        actions={
          <Button
            type="submit"
            variant="contained"
            color="success"
            onClick={handleSubmit}
          >
            {buttonText}
          </Button>
        }
      >
        {children}
      </BaseDialog>
    </>
  );
}

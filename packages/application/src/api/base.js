import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import { getCookie, urlJoin, ROOT } from "./utils";

const NBGRADER_API_ROOT = urlJoin(ROOT, "formgrader", "api");

const baseSettings = {
  credentials: "same-origin",
  headers: {
    "X-CSRFToken": getCookie("_xsrf"),
  },
};

export const baseApi = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: NBGRADER_API_ROOT, ...baseSettings }),
  endpoints: () => ({}),
});

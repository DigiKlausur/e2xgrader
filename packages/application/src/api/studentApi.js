import { baseApi } from "./base";

baseApi.enhanceEndpoints({ addTagTypes: ["Student"] });

export const studentApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getStudents: builder.query({
      query: () => `/students`,
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Student", id })),
              { type: "Student", id: "LIST" },
            ]
          : [{ type: "Student", id: "LIST" }],
    }),
    getStudent: builder.query({
      query: (studentId) => `/student/${studentId}`,
      providesTags: (result, error, id) => [{ type: "Student", id }],
    }),
    createOrUpdateStudent: builder.mutation({
      query: ({ studentId, updatedStudent }) => ({
        url: `/student/${studentId}`,
        method: "PUT",
        body: updatedStudent,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Student", id }],
    }),
  }),
});

export const {
  useGetStudentsQuery,
  useGetStudentQuery,
  useCreateOrUpdateStudentMutation,
} = studentApi;

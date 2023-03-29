import { baseApi } from "./base";

baseApi.enhanceEndpoints({ addTagTypes: ["Assignment"] });

export const assignmentApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getAssignments: builder.query({
      query: () => "/assignments",
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ name }) => ({ type: "Assignment", name })),
              { type: "Assignment", id: "LIST" },
            ]
          : [{ type: "Assignment", id: "LIST" }],
    }),
    getAssignment: builder.query({
      query: (assignmentId) => `/assignment/${assignmentId}`,
      providesTags: (result, error, name) => [{ type: "Assignment", name }],
    }),
    updateOrCreateAssignment: builder.mutation({
      query: ({ assignmentId, updatedAssignment }) => ({
        url: `/assignment/${assignmentId}`,
        method: "PUT",
        body: updatedAssignment,
      }),
      invalidatesTags: (result, error, { name }) => [
        { type: "Assignment", name },
      ],
    }),
    assignAssignment: builder.mutation({
      query: (assignmentId) => ({
        url: `/assignment/${assignmentId}/assign`,
        method: "POST",
      }),
      invalidatesTags: (result, error, { name }) => [
        { type: "Assignment", name },
      ],
    }),
    releaseAssignment: builder.mutation({
      query: (assignmentId) => ({
        url: `/assignment/${assignmentId}/release`,
        method: "POST",
      }),
      invalidatesTags: (result, error, { name }) => [
        { type: "Assignment", name },
      ],
    }),
    unreleaseAssignment: builder.mutation({
      query: (assignmentId) => ({
        url: `/assignment/${assignmentId}/unrelease`,
        method: "POST",
      }),
      invalidatesTags: (result, error, { name }) => [
        { type: "Assignment", name },
      ],
    }),
    collectAssignment: builder.mutation({
      query: (assignmentId) => ({
        url: `/assignment/${assignmentId}/collect`,
        method: "POST",
      }),
      invalidatesTags: (result, error, { name }) => [
        { type: "Assignment", name },
      ],
    }),
    generateFeedback: builder.mutation({
      query: (assignmentId) => ({
        url: `/assignment/${assignmentId}/generate_feedback`,
        method: "POST",
      }),
    }),
    releaseFeedback: builder.mutation({
      query: (assignmentId) => ({
        url: `/assignment/${assignmentId}/release_feedback`,
        method: "POST",
      }),
    }),
    generateFeedbackForStudent: builder.mutation({
      query: ({ assignmentId, studentId }) => ({
        url: `/assignment/${assignmentId}/${studentId}/generate_feedback`,
        method: "POST",
      }),
    }),
    releaseFeedbackForStudent: builder.mutation({
      query: ({ assignmentId, studentId }) => ({
        url: `/assignment/${assignmentId}/${studentId}/release_feedback`,
        method: "POST",
      }),
    }),
  }),
});

export const {
  useGetAssignmentsQuery,
  useGetAssignmentQuery,
  useUpdateOrCreateAssignmentMutation,
  useAssignAssignmentMutation,
  useReleaseAssignmentMutation,
  useUnreleaseAssignmentMutation,
  useCollectAssignmentMutation,
  useGenerateFeedbackMutation,
  useReleaseFeedbackMutation,
  useGenerateFeedbackForStudentMutation,
  useReleaseFeedbackForStudentMutation,
} = assignmentApi;

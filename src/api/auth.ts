import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_BASE_URL } from "../consts/api-base-url";
import { getHeaders } from "../utils/get-headers";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
    prepareHeaders: getHeaders,
  }),
  endpoints: (build) => ({
    signUp: build.mutation({
      query: ({ ...body }) => ({
        url: "/auth/register/",
        method: "POST",
        body,
      }),
    }),
    signIn: build.mutation({
      query: ({ ...body }) => ({
        url: "/auth/login/",
        method: "POST",
        body,
      }),
    }),
    refreshToken: build.mutation({
      query: ({ ...body }) => ({
        url: "/auth/refresh/",
        method: "POST",
        body,
      }),
    }),
  }),
});

export const { useSignInMutation, useSignUpMutation, useRefreshTokenMutation } =
  authApi;

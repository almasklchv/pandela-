import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_BASE_URL } from "../consts/api-base-url";
import { getHeaders } from "../utils/get-headers";
import { UserType } from "../types/user.type";

export const profilesApi = createApi({
  reducerPath: "profilesApi",
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
    prepareHeaders: getHeaders,
  }),
  endpoints: (build) => ({
    info: build.query<UserType, string>({
      query: (id) => ({
        url: `/profiles/info/${id}/`,
        method: "GET",
      }),
    }),
    user: build.query<UserType, string>({
      query: (id) => ({
        url: `/profiles/user/${id}/`,
        method: "GET",
      }),
    }),
    userPlaylists: build.query<UserType, string>({
      query: (id) => ({
        url: `/profiles/user-playlists/${id}/`,
        method: "GET"
      })
    }),
    followById: build.mutation({
      query: (id) => ({
        url: `/profiles/follow/${id}/`,
        method: "POST",
      })
    })
  }),
});

export const { useInfoQuery, useUserQuery, useUserPlaylistsQuery, useFollowByIdMutation } = profilesApi;

import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_BASE_URL } from "../consts/api-base-url";
import { getHeaders } from "../utils/get-headers";
import { VideoType } from "../types/video.type";
import { SearchType } from "../types/search.type";

export const blogsApi = createApi({
  reducerPath: "blogsApi",
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
    prepareHeaders: getHeaders,
  }),
  endpoints: (build) => ({
    blogs: build.query<{ results: { blogs: VideoType[] } }, any>({
      query: () => ({
        url: "/blogs/",
        method: "GET",
      }),
    }),
    search: build.query<{ matches: SearchType[] }, string>({
      query: (searchTerm) => ({
        url: `/blogs/search/${searchTerm}/`,
        method: "GET",
      }),
    }),
    video: build.query<VideoType, string>({
      query: (id) => ({
        url: `/blogs/video/${id}/`,
        method: "GET",
      }),
    }),
  }),
});

export const { useBlogsQuery, useSearchQuery, useVideoQuery } = blogsApi;

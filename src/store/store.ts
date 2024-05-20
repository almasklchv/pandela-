import { configureStore } from "@reduxjs/toolkit";
import playerModeReducer from "./playerModeSlice";
import availableCountReducer from "./availableCountSlice";
import { authApi } from "../api/auth";
import { blogsApi } from "../api/blogs";
import { profilesApi } from "../api/profiles";

export const store = configureStore({
  reducer: {
    [authApi.reducerPath]: authApi.reducer,
    [blogsApi.reducerPath]: blogsApi.reducer,
    [profilesApi.reducerPath]: profilesApi.reducer,
    videoPlayerMode: playerModeReducer,
    availableCount: availableCountReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      authApi.middleware,
      blogsApi.middleware,
      profilesApi.middleware
    ),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

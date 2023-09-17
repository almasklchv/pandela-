import { configureStore } from "@reduxjs/toolkit";
import playerModeReducer from "./playerModeSlice";
import availableCountReducer from "./availableCountSlice";

export default configureStore({
  reducer: {
    videoPlayerMode: playerModeReducer,
    availableCount: availableCountReducer,
  },
});

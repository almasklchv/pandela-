import { configureStore } from "@reduxjs/toolkit";
import playerModeReducer from './playerModeSlice'

export default configureStore({
  reducer: {
    videoPlayerMode: playerModeReducer
  },
});

import { createSlice } from "@reduxjs/toolkit";

export const playerModeSlice = createSlice({
  name: "mode",
  initialState: {
    value: ''
  },
  reducers: {
    isTheaterMode: (mode, action) => {
      mode.value = action.payload;
    },
  },
});

export const { isTheaterMode } = playerModeSlice.actions;

export default playerModeSlice.reducer;

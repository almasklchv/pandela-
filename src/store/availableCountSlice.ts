import { createSlice } from "@reduxjs/toolkit";

export const availableCountSlice = createSlice({
  name: "mode",
  initialState: {
    value: 0
  },
  reducers: {
    setCount: (count, action) => {
      count.value = action.payload;
    },
  },
});

export const { setCount } = availableCountSlice.actions;

export default availableCountSlice.reducer;

import { UserType } from "../types/user.type";

export const USER: UserType = JSON.parse(localStorage.getItem("user") ?? "");

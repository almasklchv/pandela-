export const getHeaders = (headers: Headers) => {
  const token = localStorage.getItem("token");
  if (token) {
    headers.set("Authorization", token);
  }
  return headers;
};

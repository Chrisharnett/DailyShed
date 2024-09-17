import { useState } from "react";

export const useToken = () => {
  const [token, setTokenInternal] = useState(() => {
    return sessionStorage.getItem("id_token");
  });

  const setToken = (newToken) => {
    sessionStorage.setItem("id_token", newToken);
    setTokenInternal(newToken);
  };

  return [token, setToken];
};

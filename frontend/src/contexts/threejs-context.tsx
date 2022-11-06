import axios, { AxiosInstance } from "axios";

import React, { useContext } from "react";

class ThreeJSValue {
  axios: AxiosInstance;

  constructor(public buyer: string = "Stephen", public seller: string = "Leo") {
    this.axios = axios.create({
      withCredentials: true,
    });
  }
}

const defaultValue = new ThreeJSValue();
const ThreeJSContext = React.createContext<ThreeJSValue>(defaultValue);
const useThreeJS = () => useContext(ThreeJSContext);
const ThreeJSProvider = (props: { children: React.ReactNode }) => {
  return (
    <ThreeJSContext.Provider value={defaultValue}>
      {props.children}
    </ThreeJSContext.Provider>
  );
};

export { useThreeJS, ThreeJSProvider };

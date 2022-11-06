import axios, { AxiosInstance } from "axios";
import React, { useContext } from "react";

class APIContextValue {
  axios: AxiosInstance;

  constructor(public readonly IP: string = import.meta.env.REACT_APP_IP) {
    this.axios = axios.create({
      withCredentials: true,
    });
  }
  getSimulations = async () => {
    return await this.axios.get(`/simulations`);
  };
}

const defaultValue = new APIContextValue();
const APIContext = React.createContext<APIContextValue>(defaultValue);
const useAPIs = () => useContext(APIContext);
const APIProvider = (props: { children: React.ReactNode }) => {
  return (
    <APIContext.Provider value={defaultValue}>
      {props.children}
    </APIContext.Provider>
  );
};

export { APIContext, APIProvider, useAPIs };

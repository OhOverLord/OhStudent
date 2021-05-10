import axios from "axios";

const jwtInterceptor = axios.create({});
 
 
jwtInterceptor.interceptors.request.use((config) => {
    const authData = localStorage.getItem('token');
    if (authData == null) {
      return config;
    }
  
    config.headers.common["Authorization"] = `Token ${authData}`;
    return config;
  });
  
  jwtInterceptor.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      if (error.response.status === 403) {
        const payload = {
          access_token: localStorage.getItem('token'),
          refresh_token: localStorage.getItem('refresh_token'),
        };
  
        var response = await axios.post(
          "http://localhost:8000/account/refresh_token/",
          payload
        );
        error.config.headers[
          "Authorization"
        ] = `Token ${response.data.access_token}`;
        return axios(error.config);
      } else {
        return Promise.reject(error);
      }
    }
  );
  
  export default jwtInterceptor;
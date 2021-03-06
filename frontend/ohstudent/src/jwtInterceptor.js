import axios from "axios";
import { HOST_URL } from "@/settings";

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
          token: localStorage.getItem('token'),
          refresh_token: localStorage.getItem('refresh_token'),
        };
  
        var response = await axios.post(
          `${HOST_URL}/account/refresh_token/`,
          payload
        );
        console.log(response.data)
        error.config.headers[
          "Authorization"
        ] = `Token ${response.data.user.token}`;
        localStorage.setItem('token', response.data.user.token)
        localStorage.setItem('token', response.data.user.refresh_token)
        return axios(error.config);
      } else if (error.response.status === 500) { 
        this.$router.push('/login');
      } else {
        return Promise.reject(error);
      }
    }
  );
  
  export default jwtInterceptor;
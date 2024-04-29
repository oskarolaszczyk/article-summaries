import axios from 'axios'

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refreshToken')
  
  try {
    const response = await axios.post('http://localhost:8000/api/auth/refresh', {
      refresh_token: refreshToken,
    }, {
      headers: {
        'Authorization': `Bearer ${refreshToken}`,
      },
    
    })
    const { access_token } = response.data
    localStorage.setItem('accessToken', access_token)

    return access_token
  } catch (error) {
    console.error(error)
  }
}

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api',
})

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.log('Refresh token')
      return refreshAccessToken().then((access_token) => {
        error.response.config.headers['Authorization'] = `Bearer ${access_token}`
        return axiosInstance(error.response.config)
      })
    }
    return Promise.reject(error)
  },
)

export default axiosInstance
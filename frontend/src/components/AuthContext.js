import React, { createContext, useEffect, useState } from 'react';
import axiosInstance from '../api/axiosInstance';

const AuthContext = createContext({
  isLoggedIn: false,
  isAdmin: null,
  accessToken: null,
  refreshToken: null,
  login: () => {},
  logout: () => {}
});

const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [accessToken, setAccessToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);

  useEffect(() => {
    // When the application starts, we check whether authentication data exists in localStorage
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    const storedIsAdmin = localStorage.getItem('isAdmin');


    if (storedAccessToken && storedRefreshToken && storedIsAdmin) {
      setIsLoggedIn(true);
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
      storedIsAdmin === 'true' ? setIsAdmin(true) : setIsAdmin(false);

      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${storedAccessToken}`;
    }
  }, []);

  const handleLogin = (access_token, refresh_token, is_admin) => {

    setIsLoggedIn(true);
    setIsAdmin(is_admin);
    setAccessToken(access_token);
    setRefreshToken(refresh_token);

    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
    localStorage.setItem('isAdmin', is_admin);

    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setIsAdmin(null);
    setAccessToken(null);
    setRefreshToken(null);
    
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('isAdmin');

    delete axiosInstance.defaults.headers.common["Authorization"];
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, isAdmin, accessToken, refreshToken, login: handleLogin, logout: handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };

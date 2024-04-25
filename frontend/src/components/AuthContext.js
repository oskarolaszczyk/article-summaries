import React, { createContext, useEffect, useState } from 'react';

const AuthContext = createContext({
  isLoggedIn: false,
  user: null,
  accessToken: null,
  refreshToken: null,
  login: () => {},
  logout: () => {}
});

const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);

  useEffect(() => {
    // When the application starts, we check whether authentication data exists in localStorage
    const storedUser = localStorage.getItem('user');
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    
    if (storedUser && storedAccessToken && storedRefreshToken) {
      setIsLoggedIn(true);
      setUser(JSON.parse(storedUser));
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
    }
  }, []);

  const handleLogin = (userData, access_token, refresh_token) => {
    setIsLoggedIn(true);
    setUser(userData);
    setAccessToken(access_token);
    setRefreshToken(refresh_token);
    
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);
    
    localStorage.removeItem('user');
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, accessToken, refreshToken, login: handleLogin, logout: handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };

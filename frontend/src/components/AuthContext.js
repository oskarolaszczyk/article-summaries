import React, { createContext, useState } from 'react';

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

  const handleLogin = (userData, access_token, refresh_token) => {
    setIsLoggedIn(true);
    setUser(userData);
    setAccessToken(access_token);
    setRefreshToken(refresh_token);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, accessToken, refreshToken, login: handleLogin, logout: handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };

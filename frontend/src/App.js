import {Route, Routes} from 'react-router';

import AppNavbar from "./components/AppNavbar";
import AppFooter from "./components/AppFooter";
import MainPage from "./components/MainPage";
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import ProfilePanel from "./components/ProfilePanel";
import ArticlePanel from "./components/ArticlePanel";
import AdminPanel from './components/AdminPanel';



function App() {
  return (
    <div className="App">
      <AppNavbar/>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/profile" element={<ProfilePanel />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/article_panel" element={<ArticlePanel />} />
      </Routes>
      <AppFooter/>
    </div>
  );
}

export default App;

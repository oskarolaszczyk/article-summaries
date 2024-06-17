import { Route, Routes } from 'react-router';
import AdminPanel from './components/AdminPanel';
import AppFooter from "./components/AppFooter";
import AppNavbar from "./components/AppNavbar";
import ArticlePanel from "./components/ArticlePanel";
import LoginPage from "./components/LoginPage";
import MainPage from "./components/MainPage";
import ProfilePanel from "./components/ProfilePanel";
import RegisterPage from "./components/RegisterPage";

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

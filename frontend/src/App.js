import { Route, Routes } from 'react-router';
import AdminPanel from './components/AdminPanel';
import AppFooter from "./components/AppFooter";
import AppNavbar from "./components/AppNavbar";
import ArticlePanel from "./components/ArticlePanel";
import LoginPage from "./components/LoginPage";
import MainPage from "./components/MainPage";
import ProfilePanel from "./components/ProfilePanel";
import RegisterPage from "./components/RegisterPage";
import { ToastProvider } from './components/ToastProvider';

function App() {
  return (
    <div className="App">
      <ToastProvider>
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
      </ToastProvider>
    </div>
  );
}

export default App;

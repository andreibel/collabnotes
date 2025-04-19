import {Route, Routes} from 'react-router-dom'
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import NotesListPage from './pages/NotesListPage';
function app() {
  return(
    <Routes>
      <Route  path="/login" element={<LoginPage/>}/>
      <Route  path="/register" element={<RegisterPage/>}/>
      <Route  path="/note" element={<NotesListPage/>}/>
      <Route  path="*" element={<h1> 404 not found</h1>}/>
    </Routes>
  );
}

export default app;

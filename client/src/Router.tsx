import { BrowserRouter, Route , Routes} from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import NotFound from "./pages/NotFound";


const Router = () => {
  return (
   
       <BrowserRouter>
      <Routes>
      <Route path="/"  element={<LandingPage />}/>
      <Route path="/login"  element={<LoginPage />}/>
      <Route element={<NotFound />}/>
      
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
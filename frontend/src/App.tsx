import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { GetMessage } from "./components/getMessage/getMessage";
import { NotFoundComponent } from "./components/notFound/notFound";
import { SendMessage } from "./components/sendMessage/sendMessage";
import { RegistrationForm } from "./components/registrationForm/registrationForm";

export function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route
            path="/registrationForm"
            element={<RegistrationForm />}
          ></Route>
          <Route path="/message" element={<GetMessage />}></Route>
          <Route path="/send" element={<SendMessage />}></Route>
          <Route path="*" element={<NotFoundComponent />}></Route>
        </Routes>
      </Router>
    </div>
  );
}

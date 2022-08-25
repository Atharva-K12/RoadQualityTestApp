import './App.css';
import {Routes, Route, BrowserRouter as Router} from 'react-router-dom';
import {Input, Navbar, Output} from './Components';

function App() {
  const Backend_URL = "http://127.0.0.1:8000";

  return (
    <div className="App">
      <Navbar />
      {/* <Input Backend_URL = {Backend_URL}/> */}
      <Output />
    </div>
  );
}

export default App;

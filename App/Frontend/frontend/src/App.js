import './App.css';
import {Routes, Route, BrowserRouter as Router} from 'react-router-dom';
import {Input, Navbar} from './Components';

function App() {
  const location = "http://127.0.0.1:8000";

  return (
    <div className="App">
      <Navbar />
      <Input />
    </div>
  );
}

export default App;

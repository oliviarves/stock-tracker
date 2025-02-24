import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import StockDetails from './pages/StockDetails';
import './App.css';

function App() {
    return (
        <Router>
            <div>
                <nav className="nav-header">
                    <div className="container nav-links">
                        <Link to="/" className="nav-brand">Stock Tracker</Link>
                        <div className="nav-items">
                            <Link to="/" className="nav-link">Dashboard</Link>
                        </div>
                    </div>
                </nav>

                <main className="main-content">
                    <div className="container">
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/stock/:symbol" element={<StockDetails />} />
                        </Routes>
                    </div>
                </main>
            </div>
        </Router>
    );
}

export default App;
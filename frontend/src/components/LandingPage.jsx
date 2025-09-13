import React, { useState } from 'react';
import NebulaSketch from './NebulaSketch';
import '../styles/LandingPage.css';

const LandingPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isInputFocused, setIsInputFocused] = useState(false);
  
  const handleInputChange = (e) => {
    setSearchQuery(e.target.value);
  };
  
  const handleSearch = (e) => {
    e.preventDefault();
    console.log('Searching for:', searchQuery);
    // Add search functionality here
  };
  
  return (
    <div className="landing-page">
      <div className="nebula-container">
        <NebulaSketch />
      </div>
      <div className="content">
        <div className="search-container">
          <div className={`search-field-wrapper ${isInputFocused ? 'focused' : ''}`}>
            <form onSubmit={handleSearch}>
              <input 
                type="text" 
                className="search-input" 
                placeholder="find me a cracked frontend engineer"
                value={searchQuery}
                onChange={handleInputChange}
                onFocus={() => setIsInputFocused(true)}
                onBlur={() => setIsInputFocused(false)}
              />
              <button type="submit" className="search-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </button>
            </form>
            {/* Laser tracing effect */}
            <div className="laser-trace top"></div>
            <div className="laser-trace bottom"></div>
            
            <div className="glow-effect"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
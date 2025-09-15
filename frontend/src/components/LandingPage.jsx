import React, { useState } from 'react';
import { motion } from 'framer-motion';
import NebulaSketch from './NebulaSketch';
import Results from './Results';
import useTypingAnimation from '../hooks/useTypingAnimation';
import '../styles/LandingPage.css';

const LandingPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isInputFocused, setIsInputFocused] = useState(false);
  const [apiResponse, setApiResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const { displayedText: typedTitle } = useTypingAnimation('crakd.co', 150, 600);
  
  const handleInputChange = (e) => {
    setSearchQuery(e.target.value);
  };
  
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setApiResponse(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/search/${searchQuery}`);
      const data = await response.json();
      setApiResponse(data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setApiResponse({ error: "Failed to fetch data" });
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="landing-page">
      <div className="nebula-container">
        <NebulaSketch />
      </div>
      <motion.div 
        className="content"
        initial="hidden"
        animate="visible"
        variants={{
          visible: {
            opacity: 1,
            transition: {
              staggerChildren: 0.3,
            },
          },
          hidden: {
            opacity: 0,
          },
        }}
      >
        <motion.div 
          className="header"
          variants={{
            visible: { y: 0, opacity: 1, transition: { duration: 0.6 } },
            hidden: { y: -30, opacity: 0 },
          }}
        >
          <h1 className="brand-title">{typedTitle}<span className="cursor">|</span></h1>
        </motion.div>
        
        <motion.div 
          className="search-container"
          variants={{
            visible: { y: 0, opacity: 1, '--backdrop-blur': '15px', transition: { duration: 0.8, ease: "easeOut" } },
            hidden: { y: -50, opacity: 0, '--backdrop-blur': '0px' },
          }}
          style={{ backdropFilter: 'blur(var(--backdrop-blur))' }}
        >
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
              <button type="submit" className="search-button" disabled={isLoading}>
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
            
            <div className="glow-effect"></div>
          </div>
        </motion.div>
        <Results results={apiResponse} loading={isLoading} />
      </motion.div>
    </div>
  );
};

export default LandingPage;
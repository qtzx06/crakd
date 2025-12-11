import React, { useState, useRef } from 'react';
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
  const [statusMessage, setStatusMessage] = useState('');
  const abortControllerRef = useRef(null);

  const { displayedText: typedTitle } = useTypingAnimation('crakd.co', 150, 600);

  const handleInputChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    // Cancel any existing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    setIsLoading(true);
    setApiResponse(null);
    setStatusMessage('connecting to server...');

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/search-stream/${encodeURIComponent(searchQuery)}`,
        { signal: abortControllerRef.current.signal }
      );

      // If streaming endpoint doesn't exist, fall back
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');

        // Keep the last incomplete chunk in buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.type === 'status') {
                setStatusMessage(data.message);
              } else if (data.type === 'done') {
                setApiResponse(data.results);
                setIsLoading(false);
              }
            } catch (parseError) {
              console.error('Parse error:', parseError, line);
            }
          }
        }
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        return; // Request was cancelled, ignore
      }
      console.error("Error fetching data:", error);
      setStatusMessage('connection failed, retrying with fallback...');

      // Fallback to non-streaming endpoint
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_BASE_URL}/search/${encodeURIComponent(searchQuery)}`
        );
        const data = await response.json();
        setApiResponse(data);
      } catch (fallbackError) {
        console.error("Fallback also failed:", fallbackError);
        setApiResponse({ error: "failed to fetch data" });
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
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
          <motion.p
            className="brand-subtitle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 3, duration: 1 }}
          >
            <span>made by </span><a href="https://github.com/qtzx06" target="_blank" rel="noopener noreferrer">joshua</a><span> and </span><a href="https://github.com/stephenhungg" target="_blank" rel="noopener noreferrer">stephen</a>
          </motion.p>
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
                placeholder="&quot;find me cracked rust developers&quot;"
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
          </div>
        </motion.div>
        <Results results={apiResponse} loading={isLoading} statusMessage={statusMessage} />
      </motion.div>
    </div>
  );
};

export default LandingPage;

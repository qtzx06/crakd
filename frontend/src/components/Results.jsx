import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import '../styles/Results.css';

const Results = ({ results, loading }) => {
  if (loading) {
    return <div className="loading-message">Searching for cracked devs...</div>;
  }

  // The API returns a direct array, so we access it directly.
  const developerList = (results || []).slice(0, 3);

  return (
    <div className="results-container">
      <AnimatePresence>
        {developerList.map((dev, index) => (
          <motion.a 
            key={dev.username}
            href={`https://github.com/${dev.username}`} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="developer-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            layout
          >
            <div className="developer-info">
              <span className="developer-login">{dev.username}</span>
              {dev.reasoning && (
                <motion.p 
                  className="developer-summary"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5, delay: index * 0.1 + 0.3 }}
                >
                  {dev.reasoning}
                </motion.p>
              )}
            </div>
          </motion.a>
        ))}
      </AnimatePresence>

      {/* Message for when the search is complete but no results are found */}
      {results && results.length === 0 && !loading && (
        <motion.div
          className="loading-message"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          No developers found for this query.
        </motion.div>
      )}
    </div>
  );
};

export default Results;

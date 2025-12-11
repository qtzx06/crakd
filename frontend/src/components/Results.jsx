import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import '../styles/Results.css';

const Results = ({ results, loading, statusMessage }) => {
  if (loading) {
    return (
      <div className="loading-message">
        <AnimatePresence mode="wait">
          <motion.div
            key={statusMessage}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {statusMessage || 'initializing...'}
          </motion.div>
        </AnimatePresence>
      </div>
    );
  }

  const developerList = results || [];

  return (
    <AnimatePresence>
      {developerList.length > 0 && (
        <motion.div
          className="results-container"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          {developerList.map((dev, index) => (
            <motion.a
              key={dev.username}
              href={`https://github.com/${dev.username}`}
              target="_blank"
              rel="noopener noreferrer"
              className="developer-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <div className="developer-info">
                <div className="developer-header">
                  <span className="developer-rank">#{index + 1}</span>
                  <span className="developer-login">{dev.username}</span>
                  {dev.ensemble_score && (
                    <span className="developer-score">{Math.round(dev.ensemble_score)}</span>
                  )}
                </div>
                {dev.reasoning && (
                  <p className="developer-summary">
                    {dev.reasoning}
                  </p>
                )}
              </div>
            </motion.a>
          ))}
        </motion.div>
      )}

      {results && results.length === 0 && !loading && (
        <motion.div
          className="loading-message"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          no developers found for this query.
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Results;

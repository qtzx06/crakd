/**
 * Utility functions for the NebulaSketch particle simulator
 */

// Constants
export const TAU = Math.PI * 2;

/**
 * Generate a random number between 0 and 1
 * @returns {number} Random number between 0 and 1
 */
export const rand = (min = 0, max = 1) => {
  return Math.random() * (max - min) + min;
};

/**
 * Generate a random number in a range
 * @param {number} range - Range of random number
 * @returns {number} Random number in range
 */
export const randRange = (range) => {
  return rand(0, range);
};

/**
 * Generate a random number between min and max
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Random number between min and max
 */
export const randIn = (min, max) => {
  return rand(min, max);
};

/**
 * Linear interpolation between two values
 * @param {number} a - Start value
 * @param {number} b - End value
 * @param {number} t - Interpolation factor (0-1)
 * @returns {number} Interpolated value
 */
export const lerp = (a, b, t) => {
  return a + (b - a) * t;
};

/**
 * Cosine function shorthand
 * @param {number} angle - Angle in radians
 * @returns {number} Cosine of angle
 */
export const cos = Math.cos;

/**
 * Sine function shorthand
 * @param {number} angle - Angle in radians
 * @returns {number} Sine of angle
 */
export const sin = Math.sin;

/**
 * Fade in and out based on time to live
 * @param {number} t - Current time
 * @param {number} ttl - Total time to live
 * @returns {number} Alpha value between 0 and 1
 */
export const fadeInOut = (t, ttl) => {
  const halfTtl = ttl / 2;
  if (t < halfTtl) {
    return t / halfTtl; // Fade in
  } else {
    return 1 - (t - halfTtl) / halfTtl; // Fade out
  }
};

/**
 * Create a rendering context for the particle system
 * @param {number} width - Canvas width
 * @param {number} height - Canvas height
 * @returns {Object} Object containing canvas and context
 */
export const createRenderingContext = (width = window.innerWidth, height = window.innerHeight) => {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  return { canvas, ctx };
};

/**
 * PropsArray utility for efficient particle data storage
 * @param {number} size - Number of particles
 * @param {Array|Object} props - Properties for each particle
 * @returns {Object} PropsArray instance
 */
export class PropsArray {
  constructor(size, props) {
    this.size = size;
    
    // Handle both array and object props
    if (Array.isArray(props)) {
      this.props = props;
    } else {
      this.props = Object.keys(props);
    }
    
    this.propCount = this.props.length;
    this.data = new Float32Array(size * this.propCount);
  }
  
  /**
   * Set properties for a specific particle
   * @param {Array|Object} values - Values to set
   * @param {number} i - Particle index
   */
  set(values, i) {
    if (Array.isArray(values)) {
      for (let j = 0; j < this.propCount; j++) {
        this.data[i * this.propCount + j] = values[j];
      }
    } else {
      for (let j = 0; j < this.propCount; j++) {
        const prop = this.props[j];
        if (values[prop] !== undefined) {
          this.data[i * this.propCount + j] = values[prop];
        }
      }
    }
  }
  
  /**
   * Get all properties for a specific particle
   * @param {number} i - Particle index
   * @returns {Array} Array with all properties for the particle
   */
  get(i) {
    const result = [];
    for (let j = 0; j < this.propCount; j++) {
      result.push(this.data[i * this.propCount + j]);
    }
    return result;
  }
  
  /**
   * Apply a function to each particle
   * @param {Function} fn - Function to apply
   */
  map(fn) {
    for (let i = 0; i < this.size; i++) {
      this.set(fn(this.get(i), i), i);
    }
  }
  
  /**
   * Execute a function for each particle
   * @param {Function} fn - Function to execute
   */
  forEach(fn) {
    for (let i = 0; i < this.size; i++) {
      fn(this.get(i), i);
    }
  }
}
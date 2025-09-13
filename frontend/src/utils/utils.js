/**
 * Utility functions for the NebulaSketch particle simulator
 */

/**
 * Generate a random number between min and max
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Random number between min and max
 */
export const rand = (min, max) => {
  return Math.random() * (max - min) + min;
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
 * Clamp a value between min and max
 * @param {number} val - Value to clamp
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Clamped value
 */
export const clamp = (val, min, max) => {
  return Math.max(min, Math.min(max, val));
};

/**
 * Map a value from one range to another
 * @param {number} value - Value to map
 * @param {number} inMin - Input range minimum
 * @param {number} inMax - Input range maximum
 * @param {number} outMin - Output range minimum
 * @param {number} outMax - Output range maximum
 * @returns {number} Mapped value
 */
export const mapRange = (value, inMin, inMax, outMin, outMax) => {
  return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
};

/**
 * Create a rendering context for the particle system
 * @param {number} width - Canvas width
 * @param {number} height - Canvas height
 * @returns {Object} Object containing canvas and context
 */
export const createRenderingContext = (width, height) => {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  return { canvas, ctx };
};

/**
 * PropsArray utility for efficient particle data storage
 * @param {number} size - Number of particles
 * @param {Object} props - Properties for each particle
 * @returns {Object} PropsArray instance
 */
export class PropsArray {
  constructor(size, props) {
    this.size = size;
    this.props = props;
    this.propNames = Object.keys(props);
    this.propCount = this.propNames.length;
    
    // Calculate total array size
    this.arraySize = size * this.propCount;
    
    // Create the array
    this.array = new Float32Array(this.arraySize);
    
    // Create getter/setter methods for each property
    this.propNames.forEach((prop, i) => {
      Object.defineProperty(this, prop, {
        get() {
          return this.array.subarray(i * size, (i + 1) * size);
        },
        set(arr) {
          this.array.set(arr, i * size);
        }
      });
    });
  }
  
  /**
   * Get all properties for a specific particle
   * @param {number} index - Particle index
   * @returns {Object} Object with all properties for the particle
   */
  getProps(index) {
    const result = {};
    this.propNames.forEach((prop, i) => {
      result[prop] = this.array[i * this.size + index];
    });
    return result;
  }
  
  /**
   * Set all properties for a specific particle
   * @param {number} index - Particle index
   * @param {Object} props - Properties to set
   */
  setProps(index, props) {
    this.propNames.forEach((prop, i) => {
      if (props[prop] !== undefined) {
        this.array[i * this.size + index] = props[prop];
      }
    });
  }
}
import React, { useRef, useEffect } from 'react';
import { createNoise3D } from 'simplex-noise';
import { PropsArray, rand, fadeInOut, createRenderingContext, TAU, cos, sin, lerp } from '../utils/nebula-utils';

const NebulaSketch = () => {
  const containerRef = useRef(null);
  const animationRef = useRef(null);
  
  useEffect(() => {
    
    // Create main canvas
    const mainCanvas = document.createElement('canvas');
    mainCanvas.style.position = 'absolute';
    mainCanvas.style.top = '0';
    mainCanvas.style.left = '0';
    containerRef.current.appendChild(mainCanvas);
    const ctx = mainCanvas.getContext('2d');
    
    // Create buffer for rendering
    const { ctx: buffer } = createRenderingContext();
    
    // Create noise generator
    const simplex = createNoise3D();
    
    // Variables
    let tick = 0;
    let imageBuffer;
    let particles;
    let width;
    let height;
    let centerx;
    let centery;
    
    // Particle system configuration
    const particleCount = 20000;
    const particleProps = [
      'x',
      'y',
      'vx',
      'vy',
      'a',
      'l',
      'ttl',
      'vc',
      'r',
      'g',
      'b'
    ];
    const noiseSteps = 6;
    
    // Setup function
    function setup() {
      resize();
      createParticles();
    }
    
    // Resize function
    function resize() {
      buffer.canvas.width = ctx.canvas.width = width = containerRef.current.clientWidth;
      buffer.canvas.height = ctx.canvas.height = height = containerRef.current.clientHeight;
      
      centerx = 0.5 * width;
      centery = 0.5 * height;
      
      imageBuffer = buffer.createImageData(width, height);
    }
    
    // Create particles
    function createParticles() {
      particles = new PropsArray(particleCount, particleProps);
      particles.map(createParticle);
    }
    
    // Create a single particle
    function createParticle() {
      let theta, rdist, x, y, vx, vy, a, l, ttl, vc, r, g, b;
      
      theta = rand(0, TAU);
      rdist = rand(0, 250);
      x = centerx + rdist * cos(theta);
      y = centery + rdist * sin(theta);
      vx = vy = 0;
      l = 0;
      ttl = 100 + rand(0, 200);
      vc = rand(1, 10);
      a = 0;

      // Color based on distance from the center
      const distanceFactor = rdist / 142.069; // 0 at center, 1 at edge
      
      // Center color (pure white)
      const r_center = 255;
      const g_center = 255;
      const b_center = 255;

      // Edge color (your chosen orange)
      const r_edge = 210;
      const g_edge = 134;
      const b_edge = 95;

      // Interpolate between the two colors
      r = lerp(r_center, r_edge, distanceFactor);
      g = lerp(g_center, g_edge, distanceFactor);
      b = lerp(b_center, b_edge, distanceFactor);
      
      r = (r + rand(-20, 20)) | 0;
      g = (g + rand(-20, 20)) | 0;
      b = (b + rand(-20, 20)) | 0;
      
      return [x, y, vx, vy, a, l, ttl, vc, r, g, b];
    }
    
    // Reset a particle
    function resetParticle(i) {
      particles.set(createParticle(), i);
    }
    
    // Check if particle is out of bounds
    function outOfBounds(x, y, width, height) {
      return y < 1 || y > height - 1 || x < 1 || x > width - 1;
    }
    
    // Fill a pixel in the image buffer
    function fillPixel(imageData, i, [r, g, b, a]) {
      imageData.data.set([r, g, b, a], i);
    }
    
    // Update particle coordinates based on noise field
    function updatePixelCoords(x, y, vx, vy, vc) {
      let n = simplex(x * 0.0025, y * 0.00125, tick * 0.00025) * TAU * noiseSteps;
      
      vx = lerp(vx, cos(n) * vc, 0.015);
      vy = lerp(vy, sin(n) * vc, 0.015);
      
      x += vx;
      y += vy;
      
      return [x, y, vx, vy, vc];
    }
    
    // Update particle alpha based on life
    function updatePixelAlpha(l, ttl) {
      l++;
      return [l, fadeInOut(l, ttl) * 255];
    }
    
    // Draw background
    function drawBackground() {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, width, height);
    }
    
    // Update particles
    function updateParticles() {
      imageBuffer.data.fill(0);
      
      particles.forEach(([x, y, vx, vy, a, l, ttl, vc, r, g, b], index) => {
        let i = 4 * ((x | 0) + (y | 0) * width);
        
        [l, a] = updatePixelAlpha(l, ttl);
        
        if (l < ttl && !outOfBounds(x, y, width, height)) {
          [x, y, vx, vy, vc] = updatePixelCoords(x, y, vx, vy, vc);
          
          particles.set([x, y, vx, vy, a, l, ttl, vc, r, g, b], index);
          
          fillPixel(imageBuffer, i, [r, g, b, a]);
        } else {
          resetParticle(index);
        }
      });
      
      buffer.putImageData(imageBuffer, 0, 0);
    }
    
    // Render frame with post-processing
    function renderFrame() {
      ctx.save();
      
      const isMobile = width < 768;
      const blur = isMobile ? '5px' : '10px';
      const brightness = isMobile ? '1%' : '100%';
      const saturation = isMobile ? '-100%' : '1%';

      ctx.filter = `blur(${blur}) brightness(${brightness})`;
      ctx.drawImage(buffer.canvas, 0, 0);
      
      ctx.globalCompositeOperation = 'lighter';
      
      ctx.filter = `saturate(${saturation})`;
      ctx.drawImage(buffer.canvas, 0, 0);
      
      ctx.restore();
    }
    
    // Main animation loop
    function render() {
      animationRef.current = requestAnimationFrame(render);
      
      try {
        tick++;
      updateParticles();
      drawBackground();
      renderFrame();
      } catch (error) {
        console.error(error);
        cancelAnimationFrame(animationRef.current);
      }
    }
    
    // Initialize and start animation
    setup();
    render();
    
    // Handle window resize
    const handleResize = () => {
      resize();
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup on unmount
    return () => {
      cancelAnimationFrame(animationRef.current);
      window.removeEventListener('resize', handleResize);
    };
  }, []);
  
  return (
    <div 
      ref={containerRef} 
      style={{ 
        position: 'relative',
        width: '100%', 
        height: '100%',
        overflow: 'hidden',
        background: '#000'
      }}
    />
  );
};

export default NebulaSketch;
import React from "react";

const PymetraSymbol = ({ size = 80 }) => {
  return (
    <svg 
      width={size} 
      height={size} 
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      style={{ display: 'block', margin: '0 auto' }}
    >
      {/* Laptop */}
      <g transform="translate(8, 15)">
        {/* Pantalla */}
        <rect x="0" y="0" width="18" height="12" fill="none" stroke="#0C3C32" strokeWidth="1.5"/>
        <rect x="1" y="1" width="16" height="8" fill="none" stroke="#0C3C32" strokeWidth="0.8"/>
        {/* Base del laptop */}
        <rect x="-2" y="12" width="22" height="3" fill="#0C3C32"/>
        <line x1="-3" y1="15" x2="23" y2="15" stroke="#0C3C32" strokeWidth="1"/>
      </g>

      {/* Avión */}
      <g transform="translate(45, 8)">
        <path 
          d="M8 4 L20 8 L18 12 L12 8 L8 16 L4 12 L8 4Z" 
          fill="#0C3C32"
        />
        <path 
          d="M6 10 L2 12 L2 8 L6 10Z" 
          fill="#0C3C32"
        />
      </g>

      {/* Globo Terráqueo */}
      <g transform="translate(15, 45)">
        <circle cx="15" cy="15" r="14" fill="none" stroke="#0C3C32" strokeWidth="1.8"/>
        {/* Líneas de latitud */}
        <ellipse cx="15" cy="15" rx="14" ry="7" fill="none" stroke="#0C3C32" strokeWidth="0.8"/>
        <ellipse cx="15" cy="15" rx="14" ry="4" fill="none" stroke="#0C3C32" strokeWidth="0.8"/>
        {/* Líneas de longitud */}
        <ellipse cx="15" cy="15" rx="7" ry="14" fill="none" stroke="#0C3C32" strokeWidth="0.8"/>
        <ellipse cx="15" cy="15" rx="4" ry="14" fill="none" stroke="#0C3C32" strokeWidth="0.8"/>
        <line x1="15" y1="1" x2="15" y2="29" stroke="#0C3C32" strokeWidth="0.8"/>
      </g>

      {/* Flecha hacia arriba */}
      <g transform="translate(68, 35)">
        <line x1="8" y1="25" x2="8" y2="5" stroke="#0C3C32" strokeWidth="2.2"/>
        <path d="M3 10 L8 5 L13 10" fill="none" stroke="#0C3C32" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
      </g>

      {/* Número 19 */}
      <g transform="translate(8, 68)">
        <text 
          x="0" 
          y="15" 
          fontFamily="Arial, sans-serif" 
          fontSize="14" 
          fontWeight="bold" 
          fill="#0C3C32"
        >
          19
        </text>
      </g>
    </svg>
  );
};

export default PymetraSymbol;
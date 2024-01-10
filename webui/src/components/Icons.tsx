import React from "react";

export const LogoIcon = () => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 47 40" fill="none">
        <path fill="#4f46e5" d="M23.5 6.5C17.5 6.5 13.75 9.5 12.25 15.5C14.5 12.5 17.125 11.375 20.125 12.125C21.8367 12.5529 23.0601 13.7947 24.4142 15.1692C26.6202 17.4084 29.1734 20 34.75 20C40.75 20 44.5 17 46 11C43.75 14 41.125 15.125 38.125 14.375C36.4133 13.9471 35.1899 12.7053 33.8357 11.3308C31.6297 9.09158 29.0766 6.5 23.5 6.5ZM12.25 20C6.25 20 2.5 23 1 29C3.25 26 5.875 24.875 8.875 25.625C10.5867 26.0529 11.8101 27.2947 13.1642 28.6693C15.3702 30.9084 17.9234 33.5 23.5 33.5C29.5 33.5 33.25 30.5 34.75 24.5C32.5 27.5 29.875 28.625 26.875 27.875C25.1633 27.4471 23.9399 26.2053 22.5858 24.8307C20.3798 22.5916 17.8266 20 12.25 20Z"/>
        <defs>
            <linearGradient id="%%GRADIENT_ID%%" x1="33.999" x2="1" y1="16.181" y2="16.181" gradientUnits="userSpaceOnUse">
                <stop stopColor="%%GRADIENT_TO%%"/>
                <stop offset="1" stopColor="%%GRADIENT_FROM%%"/>
            </linearGradient>
        </defs>
    </svg>
  )
}

export const LoadingCircle = ({width, height, color = "fill-white"}: { color?: string, width?: string, height?: string }) => {
  return (
    <svg className={`animate-spin ${color}`} xmlns="http://www.w3.org/2000/svg" width={width || 16} height={height || 16} viewBox="0 0 16 16">
      <path
        d="M15.4375 8.5625C15.1266 8.5625 14.875 8.31094 14.875 8C14.875 7.07188 14.6938 6.17188 14.3344 5.32344C13.9887 4.50665 13.4884 3.76439 12.8609 3.1375C12.2347 2.50925 11.4923 2.0088 10.675 1.66406C9.82813 1.30625 8.92813 1.125 8 1.125C7.68906 1.125 7.4375 0.873438 7.4375 0.5625C7.4375 0.251563 7.68906 0 8 0C9.07969 0 10.1281 0.210938 11.1141 0.629687C12.0672 1.03125 12.9219 1.60938 13.6563 2.34375C14.3906 3.07812 14.9672 3.93438 15.3703 4.88594C15.7875 5.87188 15.9984 6.92031 15.9984 8C16 8.31094 15.7484 8.5625 15.4375 8.5625Z"/>
    </svg>
  );
}
import { Button } from '@/components/livekit/button';

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref} className="fixed inset-0" style={{ backgroundColor: '#FFFFFF' }}>
      <section className="flex h-screen w-full flex-col items-center justify-center text-center px-4">
        {/* Logo/Icon */}
        <div className="mb-8 flex items-center justify-center">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full blur-xl opacity-20"></div>
            <svg 
              width="80" 
              height="80" 
              viewBox="0 0 80 80" 
              fill="none" 
              xmlns="http://www.w3.org/2000/svg"
              className="relative"
            >
              <circle cx="40" cy="40" r="38" stroke="url(#gradient)" strokeWidth="4" fill="white"/>
              <path 
                d="M25 35C25 33.8954 25.8954 33 27 33C28.1046 33 29 33.8954 29 35V45C29 46.1046 28.1046 47 27 47C25.8954 47 25 46.1046 25 45V35Z" 
                fill="url(#gradient)"
              />
              <path 
                d="M35 28C35 26.8954 35.8954 26 37 26C38.1046 26 39 26.8954 39 28V52C39 53.1046 38.1046 54 37 54C35.8954 54 35 53.1046 35 52V28Z" 
                fill="url(#gradient)"
              />
              <path 
                d="M45 32C45 30.8954 45.8954 30 47 30C48.1046 30 49 30.8954 49 32V48C49 49.1046 48.1046 50 47 50C45.8954 50 45 49.1046 45 48V32Z" 
                fill="url(#gradient)"
              />
              <path 
                d="M55 36C55 34.8954 55.8954 34 57 34C58.1046 34 59 34.8954 59 36V44C59 45.1046 58.1046 46 57 46C55.8954 46 55 45.1046 55 44V36Z" 
                fill="url(#gradient)"
              />
              <defs>
                <linearGradient id="gradient" x1="0" y1="0" x2="80" y2="80" gradientUnits="userSpaceOnUse">
                  <stop offset="0%" stopColor="#3B82F6"/>
                  <stop offset="100%" stopColor="#8B5CF6"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
          VaaniPay
        </h1>
        
        <div className="h-1 w-24 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-6"></div>

        {/* Subtitle */}
        <p className="max-w-prose text-xl mb-12 text-gray-600 font-medium">
          Your Voice Banking Assistant
        </p>

        {/* CTA Button */}
        <button
          onClick={onStartCall}
          className="font-semibold text-lg px-16 py-5 rounded-full shadow-xl transition-all duration-300 transform hover:scale-105 hover:shadow-2xl"
          style={{ 
            backgroundColor: '#000000',
            color: '#FFFFFF'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = '#1F2937';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = '#000000';
          }}
        >
          {startButtonText}
        </button>

        {/* Subtle tagline */}
        <p className="mt-8 text-sm text-gray-400">
          by Sneha and Pooja
        </p>
      </section>
    </div>
  );
};

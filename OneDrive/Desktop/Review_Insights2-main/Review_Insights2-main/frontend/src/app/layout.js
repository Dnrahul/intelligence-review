import './globals.css';

export const metadata = {
  title: 'Intelligent Review | AI-Powered Product Analysis',
  description:
    'Paste any product URL and get instant AI-powered sentiment analysis, key themes, and actionable insights from customer reviews. Powered by Intelligent Review.',
  keywords: ['review analysis', 'sentiment analysis', 'AI', 'product reviews', 'NLP', 'Intelligent Review'],
  openGraph: {
    title: 'Intelligent Review',
    description: 'AI-Powered Product Review Analysis — Understand your products through customer reviews.',
    type: 'website',
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}

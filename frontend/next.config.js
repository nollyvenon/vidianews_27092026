const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: process.env.NODE_ENV === "development",
  },
  env: {
    NEXT_PUBLIC_API_URL: apiUrl,
  },
  // Same-origin API proxy: the browser calls /api/v1/* on the frontend origin and
  // Next.js forwards it to the backend. Pages that use relative API paths then work
  // in every environment (including Docker, where the backend host is not browser-reachable).
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${apiUrl}/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;

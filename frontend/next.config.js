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
  // The sign-in page lives at /auth/login; /login is kept as a permanent redirect for old links.
  async redirects() {
    return [
      {
        source: "/login",
        destination: "/auth/login",
        permanent: true,
      },
      // Sign-up lives at /auth/signup; /register is kept as a permanent redirect for old links.
      {
        source: "/register",
        destination: "/auth/signup",
        permanent: true,
      },
      {
        source: "/",
        destination: "/home",
        permanent: false,
      },
    ];
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

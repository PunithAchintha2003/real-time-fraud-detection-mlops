import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    root: process.cwd(),
  },

  async rewrites() {
    return [
      {
        source: "/fastapi/:path*",
        destination: "http://localhost:8000/:path*",
      },
    ];
  },
};

export default nextConfig;

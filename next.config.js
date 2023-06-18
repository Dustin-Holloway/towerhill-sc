/** @type {import('next').NextConfig} */
module.exports = {
  webpack: (config) => {
    config.experiments = { ...config.experiments, topLevelAwait: true };
    return config;
  },

  images: {
    domains: ["lh3.googlusercontent.com"],
  },

  async rewrites() {
    return [
      {
        source: "/api2/:path*",
        destination: "http://127.0.0.1:5555/api2/:path*",
      },
    ];
  },
};

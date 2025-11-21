/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,  // 临时关闭严格模式以避免WebSocket重复连接
  assetPrefix: process.env.BASE_PATH || "",
  basePath: process.env.BASE_PATH || "",
  trailingSlash: true,
  publicRuntimeConfig: {
    root: process.env.BASE_PATH || "",
  },
};

module.exports = nextConfig;

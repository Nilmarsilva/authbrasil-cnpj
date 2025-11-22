/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://api.authbrasil.app.br',
  },
  images: {
    domains: ['authbrasil.app.br'],
  },
}

export default nextConfig

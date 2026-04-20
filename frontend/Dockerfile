# --- Stage 1: Build ---
FROM node:20-alpine AS builder

ARG VITE_API_URL=http://localhost:9001

WORKDIR /build
COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- Stage 2: Serve ---
FROM nginx:alpine

# Copy built React app
COPY --from=builder /build/dist /usr/share/nginx/html

# Custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# Build frontend first
FROM node:18-alpine as frontend-builder
WORKDIR /app
ENV CI=false
ENV GENERATE_SOURCEMAP=false
COPY frontend/package*.json ./
RUN npm install --only=production
COPY frontend/ .
RUN node sanitize.js
RUN npm run build

# Nginx production
FROM nginx:alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend-builder /app/build /usr/share/nginx/html
EXPOSE 80

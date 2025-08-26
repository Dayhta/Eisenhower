# For development
FROM node:18-alpine As development
WORKDIR /app
ENV CI=false
ENV GENERATE_SOURCEMAP=false
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["sh","-c","[ -d node_modules ] || npm install; node sanitize.js; npm start"]

# For staging
FROM node:18-alpine As staging
WORKDIR /app
ENV CI=false
ENV GENERATE_SOURCEMAP=false
COPY package*.json ./
RUN npm install
COPY . .
RUN node sanitize.js
RUN npm run build
FROM nginx:alpine
COPY --from=staging /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# For production
FROM node:18-alpine As production
WORKDIR /app
ENV CI=false
ENV GENERATE_SOURCEMAP=false
COPY package*.json ./
RUN npm install --only=production
COPY . .
RUN node sanitize.js
RUN npm run build
FROM nginx:alpine
COPY --from=production /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

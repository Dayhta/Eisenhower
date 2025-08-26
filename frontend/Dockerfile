# For development
FROM node:18-alpine As development
WORKDIR /app
ENV CI=false
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["sh","-c","[ -d node_modules ] || npm install; node sanitize.js; npm start"]

# For staging
FROM node:18-alpine As staging
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]


# For production
FROM node:18-alpine As production
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]

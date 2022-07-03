FROM node:16 as dev
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN chown -R node /app/node_modules
USER node
EXPOSE 3000
CMD ["npm", "run", "dev"]

FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.22-alpine as prod
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
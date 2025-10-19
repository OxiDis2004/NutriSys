FROM node:20 AS builder
LABEL authors="Denys Ponomarenko"

WORKDIR /web

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx

COPY --from=builder /web/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
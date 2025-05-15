FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install -g serve

COPY * .

CMD ["serve", "-s", "."]

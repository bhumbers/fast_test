FROM node:16-alpine

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install
RUN npm install -g serve

COPY frontend .

CMD ["serve", "-s", "."]

FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY public/ ./public
COPY src/ ./src

RUN npm run build

FROM node:16-alpine as production

WORKDIR /app

RUN npm install -g serve

COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]

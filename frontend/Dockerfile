FROM node:19.9

WORKDIR /frontend

COPY package.json .

RUN npm -g install npm@latest

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
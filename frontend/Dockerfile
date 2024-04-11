FROM node:16 as build-stage

WORKDIR /app

COPY ./frontend/package*.json /app/

RUN npm install serve -g

RUN npm install

COPY ./frontend/ /app/

RUN npm run build

EXPOSE 3003

CMD ["npm", "run","serve"]
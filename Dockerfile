#-------------------------- build stage ---------------------
FROM node:lts-alpine as build-stage
WORKDIR /app

#install dependencies
COPY ./fe/package.json ./
RUN npm install

#main fe logic (docker optimization)
COPY ./fe ./
RUN npm run build

#-------------------------- prod stage ----------------------
FROM tiangolo/uwsgi-nginx-flask:python3.8 as production-stage

#serve static/index.html
ENV STATIC_INDEX 1
ENV LISTEN_PORT 80

#install dependencies
COPY ./be/requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY ./be/requirements_aligner.txt /app
RUN pip install -r /app/requirements_aligner.txt

#copy assets
RUN mkdir /app/static /app/static/flags
COPY ./fe/src/assets/flags /app/static/flags

#main fe logic (docker optimization)
COPY ./be /app

COPY --from=build-stage /app/dist /app/static

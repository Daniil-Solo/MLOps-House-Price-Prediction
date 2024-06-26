FROM node:20.11-alpine as react_build
WORKDIR /app
COPY . .
ENV VITE_MODE=production
RUN npm install
RUN npm run build

FROM nginx:alpine3.18
COPY --from=react_build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
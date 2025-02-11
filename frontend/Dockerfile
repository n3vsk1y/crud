# FROM node:18 AS build-stage

# WORKDIR /app

# COPY package.json package-lock.json ./
# RUN npm install
# COPY . .
# RUN npm run build

# FROM nginx:alpine
# COPY --from=build-stage /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# Используем официальный образ Node.js
FROM node:18 AS build-stage

WORKDIR /app

# Копируем package.json и package-lock.json для установки зависимостей
COPY package.json package-lock.json ./
RUN npm install

# Копируем все файлы приложения в контейнер
COPY . .

# Устанавливаем зависимости
RUN npm install

# Открываем порт 3000 для разработки
EXPOSE 5173

# Запускаем Vite в режиме разработки
CMD ["npm", "run", "dev"]


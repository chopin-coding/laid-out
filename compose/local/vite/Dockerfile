# Base image
FROM node:21-alpine

# Working directory
WORKDIR /app

# Copy Vite dependencies
COPY package.json ./

# Install Vite dependencies
RUN npm install

# Copy project code
COPY . ./

# Run Vite dev server
CMD ["npm", "run", "dev"]

# Expose Vite dev server port
EXPOSE 5173

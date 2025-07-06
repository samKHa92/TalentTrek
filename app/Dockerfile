# Dockerfile
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the React app
RUN npm run build

# Expose port
EXPOSE 80

# Serve the build with a static server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "80"] 
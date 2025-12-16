# 1. Use Node.js (matches your local environment)
FROM node:18-alpine

# 2. Set working directory
WORKDIR /app

# 3. Copy package.json first (for caching)
COPY package*.json ./

# 4. Install dependencies inside the container
RUN npm install

# 5. Copy the rest of the code
COPY . .

# 6. Start the app
# We add --host to allow access from outside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
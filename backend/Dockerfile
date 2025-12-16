# 1. Use an official lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependencies file first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your backend code
COPY . .

# 6. Command to run the application
# We use 0.0.0.0 so the container accepts connections from outside
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
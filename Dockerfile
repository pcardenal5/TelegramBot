FROM python:3.12
WORKDIR /app

# Install dependencies
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install

# Copy the code
COPY src ./src
COPY .env ./
COPY main.py ./
EXPOSE 5000


CMD ["pipenv", "run", "main"]

FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add the deployment user
RUN groupadd -g 1070 stg && useradd -u 1070 -g stg stg

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements_dev.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

RUN chmod +x /code/cmd.sh && chmod +x wait-for.sh

# Grant the deployment user access to the files
RUN chown -R stg:stg /code/

# Run the container as deployment user
USER stg
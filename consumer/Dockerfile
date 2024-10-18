FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/code/src:${PYTHONPATH}"
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-11-jdk \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# Pre-compile the python packages
# Cleanup unnecessary build tools (optional)
# Make the entrypoint script executable
RUN python -m compileall -q -f /usr/local/lib/python3.9/site-packages/* && \
    python -m compileall -q -f ./src && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    chmod +x entrypoint.sh

# Download and cache the Hugging Face model weights
RUN python -c "from transformers import AutoModelForSequenceClassification, AutoTokenizer; \
               AutoTokenizer.from_pretrained('cardiffnlp/xlm-twitter-politics-sentiment'); \
               AutoModelForSequenceClassification.from_pretrained('cardiffnlp/xlm-twitter-politics-sentiment')"

ENTRYPOINT ["./entrypoint.sh"]
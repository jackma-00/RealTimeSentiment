FROM golang:1.23.2-bookworm


COPY . /app
WORKDIR /app

RUN go build -o main .

CMD ["/app/main"]


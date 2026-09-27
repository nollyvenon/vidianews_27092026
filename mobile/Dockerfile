FROM cirrusci/flutter:latest

WORKDIR /app

COPY pubspec.yaml pubspec.lock* ./
RUN flutter pub get

COPY . .
RUN flutter build web

EXPOSE 8080

CMD ["flutter", "run", "-d", "web", "--web-hostname", "0.0.0.0"]

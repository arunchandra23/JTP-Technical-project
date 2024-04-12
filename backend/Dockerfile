FROM python:3.10.8

WORKDIR /app

COPY ./backend /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8008

ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PORT="8008"

CMD ["sh", "-c", "uvicorn ${MODULE_NAME}:${VARIABLE_NAME} --host 0.0.0.0 --port ${PORT}"]

# syntax=docker/dockerfile:1
FROM python:3.13-alpine3.24

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python3.13 src/main.py" > /dev/null || exit 1

RUN addgroup -S darkbotgroup && adduser -S darkbotuser -G darkbotgroup

RUN apk update && apk add git
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev

RUN git clone https://github.com/xNiloGamerx/DarkBot.git
WORKDIR /DarkBot/src

RUN mkdir ../log
RUN touch ../log/discord.log

RUN chown -R darkbotuser:darkbotgroup /DarkBot
USER darkbotuser

RUN pip install -r ../requirements.txt

CMD ["python3.13", "./main.py"]

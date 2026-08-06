# Assistente Estratégico — bot em tempo real (Socket Mode).
# Build a partir da RAIZ do repo:  docker build -f assistente-estrategico/bot/Dockerfile -t acta-assistente .
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl jq ca-certificates gnupg git \
 && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && npm install -g @anthropic-ai/claude-code \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/acta-agentes
COPY . .
RUN pip install --no-cache-dir -r assistente-estrategico/bot/requirements.txt \
 && chmod +x pauta-staff/scripts/*.sh assistente-estrategico/scripts/*.sh

# variáveis esperadas em tempo de execução: SLACK_BOT_TOKEN, SLACK_APP_TOKEN,
# SLACK_CHANNEL_ID, SLACK_STAFF_CHANNEL_ID, ANTHROPIC_API_KEY e, opcionalmente,
# GOOGLE_SERVICE_ACCOUNT_FILE (monte o JSON como volume/secret) e
# DRIVE_DOC_PLANEJAMENTO
CMD ["python3", "assistente-estrategico/bot/bot.py"]

FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml requirements.txt ./
COPY security_patch_agent ./security_patch_agent
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -e . \
    && useradd -m agentuser
USER agentuser
ENTRYPOINT ["security-patch-agent"]

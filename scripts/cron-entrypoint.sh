#!/usr/bin/env bash
set -e

# Export current environment so cron jobs inherit Docker-injected env vars
export -p > /app/.cronenv

# Install crontab: run at 00:00, 06:00, 12:00, 18:00 (minute 0, every 6 hours)
# SHELL and sourcing .cronenv ensure jobs run with the same env as the container
{
  echo "SHELL=/bin/bash"
  echo "0 */6 * * * . /app/.cronenv 2>/dev/null; cd /app && uv run python -m commands.tweet en >> /var/log/cron.log 2>&1"
  echo "0 */6 * * * . /app/.cronenv 2>/dev/null; cd /app && uv run python -m commands.tweet fr >> /var/log/cron.log 2>&1"
} | crontab -

exec crond -f

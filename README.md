# Flow Discord Release Alerts Bot

This project is a Dockerized Python application that monitors the **Flow Discord `#developer-updates` channel** and sends automated alerts whenever a **new release** is announced.

## What it does
- Listens to a specific Discord channel using a read-only bot
- Detects release messages (version numbers, release keywords, GitHub release links)
- Sends real-time alerts via a webhook (Discord/Slack/etc.)
- Runs continuously inside Docker

## Why this is needed
Flow release announcements are posted in Discord and currently require manual monitoring.  
This bot removes manual effort and ensures no important release updates are missed.

## Current status
- ✅ Bot created and fully tested in a test Discord server
- ✅ Alerts work in real time
- ⏳ Waiting for Flow Discord admin approval to add the bot to the real Flow server

Once the bot is added to the Flow Discord server and the real channel ID is configured, it will work live with no code changes.

## Requirements
- Docker & Docker Compose
- Discord Bot Token
- Discord Channel ID
- Webhook URL (Discord/Slack)

## How it works (high level)
1. Discord bot connects using a bot token
2. Listens for new messages in `#developer-updates`
3. Filters messages to detect real releases
4. Sends alerts instantly via webhook

## Running the app

```bash
docker compose up -d
```
README:

Check logs:
```bash
docker logs -f flow-alerts
```

Stop the app:
```bash
docker compose down
```
## Configuration

All sensitive values are stored in a .env file (not committed to GitHub):
```env
DISCORD_TOKEN=your_bot_token
CHANNEL_ID=discord_channel_id
ALERT_WEBHOOK_URL=your_webhook_url
```

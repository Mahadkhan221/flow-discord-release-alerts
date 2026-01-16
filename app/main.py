import os
import re
import json
import aiohttp
import discord

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL", "").strip()

# --- Release detection (based on your pasted Flow messages) ---
VERSION_RE = re.compile(r"\bv\d+\.\d+(\.\d+)?\b", re.IGNORECASE)
GITHUB_RELEASE_RE = re.compile(r"github\.com\/.+\/releases", re.IGNORECASE)

RELEASE_KEYWORDS = [
    "released",
    "now live",
    "release notes",
    "network upgrade",
    "upgrade to",
    "please upgrade",
    "is now complete",
    "is live",
]

# Optional noise suppression (doesn't block real releases with version/GitHub release proof)
IGNORE_KEYWORDS = [
    "office hours",
    "meeting",
]

def is_release_message(content: str) -> bool:
    text = (content or "").lower()

    # Ignore obvious noise unless strong release proof exists
    if any(k in text for k in IGNORE_KEYWORDS):
        strong = bool(VERSION_RE.search(text) or GITHUB_RELEASE_RE.search(text))
        if not strong:
            return False

    has_proof = bool(VERSION_RE.search(text) or GITHUB_RELEASE_RE.search(text))
    has_release_language = any(k in text for k in RELEASE_KEYWORDS)

    return has_proof and has_release_language


async def send_alert(text: str):
    if not ALERT_WEBHOOK_URL:
        print("ALERT_WEBHOOK_URL not set; skipping alert.")
        return

    payload = {"content": text}  # Discord webhook format
    async with aiohttp.ClientSession() as session:
        async with session.post(
            ALERT_WEBHOOK_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            if resp.status >= 300:
                body = await resp.text()
                print(f"Webhook error {resp.status}: {body}")


intents = discord.Intents.default()
intents.message_content = True  # requires Message Content Intent enabled in portal
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} | watching channel_id={CHANNEL_ID}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID:
        return

    if is_release_message(message.content):
        alert = (
            f"🚀 **Flow Release Alert**\n"
            f"**Author:** {message.author.display_name}\n"
            f"**Message:** {message.content}\n"
            f"**Link:** {message.jump_url}"
        )
        print("RELEASE DETECTED:", alert)
        await send_alert(alert)
    else:
        print("Ignored:", (message.content or "")[:120])


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise SystemExit("DISCORD_TOKEN missing")
    if CHANNEL_ID == 0:
        raise SystemExit("CHANNEL_ID missing/invalid")
    client.run(DISCORD_TOKEN)

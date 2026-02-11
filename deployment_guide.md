# Deploying CyberRescue Bot: Permanent Hosting Guide 🚀

Since this bot uses **SQLite** (a local database file), you need a hosting provider that supports **Persistent Disk Storage**. If you use a free tier that wipes the disk on restart (like Heroku/Render free), you will **lose all user data**.

## Recommended Option: Virtual Private Server (VPS)
This is the most robust, professional, and "permanent" way. You get a full computer in the cloud.

**Providers**: DigitalOcean ($4/mo), Hetzner ($5/mo), AWS Lightsail ($3.50/mo).

### Steps to Deploy on a VPS:
1.  **Buy a VPS** (Ubuntu 22.04 LTS recommended).
2.  **SSH into the server**: `ssh root@your-server-ip`
3.  **Install Docker**:
    ```bash
    apt update && apt install -y docker.io docker-compose
    ```
4.  **Clone your Repo**:
    ```bash
    git clone https://github.com/Ch4lkP0wd3r/CyberRescueBot.git
    cd CyberRescueBot
    ```
5.  **Set your Token**:
    Create a `.env` file:
    ```bash
    echo "TELEGRAM_TOKEN=your_actual_token_here" > .env
    ```
6.  **Run with Docker Compose**:
    ```bash
    docker-compose up -d
    ```

**Result**: The bot runs forever. Even if the server restarts, Docker will restart the bot, and your database will be safe in the `data/` volume.

---

## Alternative: Railway / Render (PaaS)
easier to set up, but requires configuration for storage.

### Railway (Recommended for Ease)
1.  Connect GitHub repo to **Railway**.
2.  Add a **Volume** in Railway settings and mount it to `/app/data`.
3.  Set `TELEGRAM_TOKEN` in Variables.
4.  Deploy.

### Render
1.  Connect GitHub repo to **Render Web Service** (Select Docker runtime).
2.  Add a **Disk** (requires paid plan) mounted to `/app/data`.
3.  Deploy.

---

> [!WARNING]
> Do **NOT** use Heroku Free or Render Free tier without external storage. Your database will be deleted every 24 hours.

---

## 💸 Free Hosting Options (Permanent)

### 1. Oracle Cloud "Always Free" (Best Choice) 🥇
Oracle provides a surprisingly generous free tier.
- **What you get**: A real VPS (ARM Ampere instance) with 24GB RAM and 4 OCPUs.
- **Persistence**: Yes, full local storage.
- **Validity**: "Always Free" (supposedly forever).
- **Setup**: Same as VPS instructions above.

### 2. Fly.io (Good for Docker) 🥈
- **What you get**: Free allowance for small apps.
- **Persistence**: You can attach a free 1GB volume.
- **Setup**:
    1. Install `flyctl`.
    2. `fly launch` (it detects the Dockerfile).
    3. `fly vol create data_volume --size 1` (Create 1GB persistent disk).
    4. Update `fly.toml` to mount `data_volume` to `/app/data`.
    5. `fly deploy`.

### 3. PythonAnywhere (Free Tier) 🥉
- **What you get**: A specific Python hosting environment.
- **Persistence**: Yes, SQLite files are kept safe!
- **Limitations**: 
    - No Docker (you must use their interface/git).
    - Can only use `Polling` (Webhooks restricted).
    - CPU usage limits.

---

## 🕵️‍♂️ Privacy Mode (Ephemeral Hosting)
**"I don't care if data is wiped. Privacy is key."**

If you want the bot to **forget everything** (users, reports, logs) every time it restarts (approx every 24h), use these platforms without configuring storage volumes.

### 1. Render.com (Free Tier)
- **Setup**:
    1. New **Web Service** -> Connect Repo.
    2. Runtime: **Docker**.
    3. Environment Variable: `TELEGRAM_TOKEN`.
    4. **Deploy**.
- **Result**: Bot runs 24/7 (sleeps after inactivity). Resets daily. 100% Free.

### 2. Railway (No Volume)
- **Setup**: Just deploy the repo. Don't add a volume.
- **Result**: Faster than Render, but limited execution hours per month on free tier.

# Deploying AR-MED Telegram Bot on Render

This guide explains how to deploy the AR-MED Posture Analysis Telegram Bot on Render.

## Prerequisites

1. A Render account (https://render.com)
2. Your Telegram Bot Token (from BotFather)

## Deployment Steps

### 1. Fork or Clone this Repository

Make sure you have a copy of the code in your own GitHub repository.

### 2. Create a New Web Service on Render

1. Go to the Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: `ar-med-telegram-bot` (or your preferred name)
   - Environment: `Python`
   - Build Command: `./build.sh` 
   - Start Command: `python telegram_bot.py`
   - Plan: Choose an appropriate plan (at least the "Individual" plan with 512 MB RAM)

### 3. Set Environment Variables

In the Render dashboard, under your service, go to "Environment" and add the following variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather
- `RENDER`: `true`
- `PORT`: `8080` (or let Render assign automatically)

Optional for webhook mode:
- `WEBHOOK_URL`: `https://your-service-name.onrender.com/`

### 4. Deploy

Click "Create Web Service" to deploy the bot.

## Troubleshooting Deployment Issues

If you encounter build errors:

1. Check that you're using the build.sh script as your build command
2. Verify that the runtime.txt specifies Python 3.9
3. If NumPy or other compilation errors occur, try using pre-compiled wheels by modifying requirements.txt

## Webhook vs Long Polling

The bot supports two modes of operation:

1. **Long Polling** (default): The bot will continuously poll the Telegram API for updates. This is simpler but may have higher latency.

2. **Webhook**: If you provide a `WEBHOOK_URL`, the bot will use webhook mode, which is more efficient. Telegram will push updates directly to your service.

To use webhook mode, add the `WEBHOOK_URL` environment variable pointing to your Render service URL.

## File Storage

The bot uses Render's ephemeral storage (`/tmp` directory) for storing uploaded images, generated reports, and other temporary files. Note that these files will be lost when the service restarts, which is normal for most cloud deployments.

## Resource Considerations

The bot processes images and videos, which requires significant CPU and memory resources. On Render:

- The Free plan may not be sufficient for video processing
- The Individual plan ($7/month) should work for moderate usage
- For higher volume, consider the Pro plan ($15/month) or higher

## Support

If you encounter issues with deployment, check the Render logs for specific error messages and refer to Render's documentation at https://render.com/docs. 
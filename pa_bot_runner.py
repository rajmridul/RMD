"""
Simple runner script for the bot that includes error handling
and automatic restart if the bot crashes.
"""
import time
import logging
import subprocess
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_bot():
    while True:
        try:
            logger.info("Starting the bot...")
            process = subprocess.Popen(
                [sys.executable, "python_anywhere_bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            
            # Monitor the process
            for line in process.stdout:
                logger.info(line.decode().strip())
            
            # If we get here, the process has ended
            exit_code = process.wait()
            logger.warning(f"Bot exited with code {exit_code}")
            
            # Wait before restarting
            logger.info("Waiting 10 seconds before restart...")
            time.sleep(10)
            
        except Exception as e:
            logger.exception(f"Error in runner: {e}")
            logger.info("Waiting 30 seconds before retry...")
            time.sleep(30)

if __name__ == "__main__":
    run_bot()
import os
import logging
import telebot
import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
from datetime import datetime
import uuid
import tempfile
import sys
from posture_analysis import analyze_posture, create_pdf_report, create_aggregated_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize the Telegram bot with your token
# Get from environment variable or settings file
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    # Check for a token file for PythonAnywhere
    token_path = os.path.join(os.path.dirname(__file__), 'token.txt')
    if os.path.exists(token_path):
        with open(token_path, 'r') as f:
            BOT_TOKEN = f.read().strip()

if not BOT_TOKEN:
    raise ValueError("No Telegram bot token found. Please set TELEGRAM_BOT_TOKEN environment variable or create a token.txt file.")

bot = telebot.TeleBot(BOT_TOKEN)

# Create directories for file storage
# PythonAnywhere's file system is persistent unlike Heroku
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
FRAMES_DIR = os.path.join(BASE_DIR, 'frames')
VISUALIZATIONS_DIR = os.path.join(BASE_DIR, 'visualizations')

# Create directories if they don't exist
for directory in [UPLOADS_DIR, REPORTS_DIR, FRAMES_DIR, VISUALIZATIONS_DIR]:
    os.makedirs(directory, exist_ok=True)

def extract_frames(video_path, output_dir, max_frames=10):
    """Extract frames from a video file"""
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        
        # Check if video opened successfully
        if not cap.isOpened():
            logger.error(f"Error opening video file {video_path}")
            return {"error": "Failed to open video file"}
        
        # Get video properties
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        logger.info(f"Video info: {length} frames, {fps} fps, resolution: {width}x{height}")
        
        # Determine frames to capture
        if length <= max_frames:
            # If video is short, take all frames
            frame_indices = range(length)
        else:
            # Sample frames evenly throughout the video
            frame_indices = [int(i * length / max_frames) for i in range(max_frames)]
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract frames
        frame_paths = []
        for idx, frame_idx in enumerate(frame_indices):
            # Set the position of the video file to the frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            
            # Read the frame
            ret, frame = cap.read()
            if not ret:
                logger.warning(f"Failed to read frame {frame_idx}")
                continue
                
            # Save the frame
            frame_path = os.path.join(output_dir, f"frame_{idx:03d}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            
        # Release the video capture object
        cap.release()
        
        logger.info(f"Extracted {len(frame_paths)} frames from video")
        
        # Return information about the extracted frames
        return {
            "total_frames": len(frame_paths),
            "frame_paths": frame_paths,
            "original_length": length,
            "fps": fps
        }
        
    except Exception as e:
        logger.exception(f"Error extracting frames: {str(e)}")
        return {"error": f"Failed to extract frames: {str(e)}"}

# Telegram bot handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
                 "Welcome to AR-MED Posture Analysis Bot! 👋\n\n"
                 "Send me a photo or video of yourself standing, and I'll analyze your posture.\n\n"
                 "Commands:\n"
                 "/start - Show this welcome message\n"
                 "/help - Show help information")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Send a processing message
        processing_msg = bot.reply_to(message, "Processing your photo... Please wait.")
        
        # Get the file ID of the largest photo
        file_id = message.photo[-1].file_id
        
        # Get file path from Telegram
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        
        # Download the file
        downloaded_file = bot.download_file(file_path)
        
        # Generate unique filename
        user_id = message.from_user.id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{user_id}_{timestamp}_{unique_id}.jpg"
        local_path = os.path.join(UPLOADS_DIR, filename)
        
        # Save the file locally
        with open(local_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        logger.info(f"Image saved to {local_path}")
        
        # Analyze posture
        analysis_result = analyze_posture(local_path, visualization=True, generate_pdf=False, return_data=True)
        
        # Check for errors
        if "error" in analysis_result:
            bot.edit_message_text(
                f"❌ Analysis error: {analysis_result['error']}",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
            return
        
        # Get visualization path
        vis_path = analysis_result.get("visualization_path")
        
        # Create PDF report
        pdf_path = create_pdf_report(local_path, analysis_result, vis_path)
        
        # Send results to user
        bot.edit_message_text(
            "✅ Analysis complete! Here are your results:",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id
        )
        
        # Send visualization if available
        if vis_path and os.path.exists(vis_path):
            with open(vis_path, 'rb') as vis_file:
                bot.send_photo(message.chat.id, vis_file, caption="Posture Analysis Visualization")
        
        # Send PDF report
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf_file:
                bot.send_document(
                    message.chat.id, 
                    pdf_file, 
                    caption="Detailed Posture Analysis Report",
                    visible_file_name="posture_analysis.pdf"
                )
        
        # Send summary text
        if "summary" in analysis_result:
            summary = "Summary of findings:\n\n"
            for issue, details in analysis_result["summary"].items():
                summary += f"• {issue}: {details}\n"
            
            bot.send_message(message.chat.id, summary)
        
    except Exception as e:
        logger.exception(f"Error processing photo: {e}")
        bot.send_message(message.chat.id, f"Sorry, an error occurred while processing your photo: {str(e)}")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        # Send a processing message
        processing_msg = bot.reply_to(message, "Processing your video... This might take a minute.")
        
        # Get the file ID
        file_id = message.video.file_id
        
        # Get file path from Telegram
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        
        # Download the file
        downloaded_file = bot.download_file(file_path)
        
        # Generate unique filename
        user_id = message.from_user.id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{user_id}_{timestamp}_{unique_id}.mp4"
        local_path = os.path.join(UPLOADS_DIR, filename)
        
        # Save the file locally
        with open(local_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        logger.info(f"Video saved to {local_path}")
        
        # Create output directory for frames
        frames_output_dir = os.path.join(FRAMES_DIR, f"{user_id}_{timestamp}_{unique_id}")
        os.makedirs(frames_output_dir, exist_ok=True)
        
        # Extract frames from video
        bot.edit_message_text(
            "Extracting frames from video...",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id
        )
        
        frame_result = extract_frames(local_path, frames_output_dir, max_frames=10)
        
        # Check for errors
        if "error" in frame_result:
            bot.edit_message_text(
                f"❌ Error extracting frames: {frame_result['error']}",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
            return
        
        # Check if we have enough frames
        if frame_result["total_frames"] < 5:
            bot.edit_message_text(
                "❌ Not enough frames could be extracted from the video. Please upload a longer video or a photo instead.",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
            return
        
        # Analyze each frame
        bot.edit_message_text(
            f"Analyzing {frame_result['total_frames']} frames...",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id
        )
        
        analysis_results = []
        for i, frame_path in enumerate(frame_result["frame_paths"]):
            try:
                analysis_data = analyze_posture(frame_path, visualization=True, generate_pdf=False, return_data=True)
                if "error" not in analysis_data:
                    analysis_data["frame_number"] = i + 1
                    analysis_results.append(analysis_data)
            except Exception as e:
                logger.warning(f"Error analyzing frame {frame_path}: {str(e)}")
        
        # Check if we have enough successful analyses
        if len(analysis_results) < 3:  # At least 3 successful analyses
            bot.edit_message_text(
                "❌ Could not analyze enough frames successfully. Please try with a clearer video or a photo.",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
            return
        
        # Create aggregated report
        bot.edit_message_text(
            "Creating aggregated report...",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id
        )
        
        # Generate report filename
        report_filename = f"video_analysis_{user_id}_{timestamp}_{unique_id}.pdf"
        report_path = os.path.join(REPORTS_DIR, report_filename)
        
        # Create visualization path
        vis_filename = f"video_vis_{user_id}_{timestamp}_{unique_id}.jpg"
        vis_path = os.path.join(VISUALIZATIONS_DIR, vis_filename)
        
        # Generate the report
        report_result = create_aggregated_report(
            analysis_results, 
            report_path, 
            visualization_path=vis_path,
            frame_paths=frame_result["frame_paths"][:4]  # Use first 4 frames for visualization
        )
        
        # Check for errors
        if "error" in report_result:
            bot.edit_message_text(
                f"❌ Error creating report: {report_result['error']}",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
            return
        
        # Send results to user
        bot.edit_message_text(
            "✅ Video analysis complete! Here are your results:",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id
        )
        
        # Send visualization if available
        if os.path.exists(vis_path):
            with open(vis_path, 'rb') as vis_file:
                bot.send_photo(message.chat.id, vis_file, caption="Video Analysis Overview")
        
        # Send PDF report
        if os.path.exists(report_path):
            with open(report_path, 'rb') as pdf_file:
                bot.send_document(
                    message.chat.id, 
                    pdf_file, 
                    caption="Detailed Video Analysis Report",
                    visible_file_name="video_posture_analysis.pdf"
                )
        
        # Summary message
        bot.send_message(
            message.chat.id,
            f"📊 Analyzed {len(analysis_results)} frames from your video.\n"
            f"💡 The report contains aggregated measurements and posture insights."
        )
        
    except Exception as e:
        logger.exception(f"Error processing video: {e}")
        bot.send_message(message.chat.id, f"Sorry, an error occurred while processing your video: {str(e)}")

# Health check handler
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "Pong! Bot is up and running.")

# Periodic task to keep bot alive
def keep_alive():
    logger.info("Keep-alive check: bot is running")

# Start the bot with polling
def main():
    logger.info("Starting AR-MED Telegram bot...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.exception(f"Bot polling error: {e}")

if __name__ == "__main__":
    main()
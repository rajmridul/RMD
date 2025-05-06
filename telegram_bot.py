import os
import tempfile
import logging
import uuid
from telebot import TeleBot, types
import cv2
import sys

print(f"Using OpenCV version: {cv2.__version__}")
# Add your project's directory to the path so we can import from it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing posture analysis code
from posture_analysis import analyze_posture, create_aggregated_report

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize directories
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
PDF_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
FRAMES_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frames')
VISUALIZATIONS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'visualizations')

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)
os.makedirs(VISUALIZATIONS_FOLDER, exist_ok=True)

# Initialize the bot with your token
TOKEN = '7390276698:AAE08VB7ML-4xee3OOD8VrDOFVPCWm-1g6U'  # Replace with your actual token
bot = TeleBot(TOKEN)

def extract_frames(video_path, output_dir, num_frames=10, max_duration=6.0):
    """
    Extract frames from a video at regular intervals
    
    Args:
        video_path: Path to the video file
        output_dir: Directory to save extracted frames
        num_frames: Number of frames to extract
        max_duration: Maximum duration of video to process in seconds
    
    Returns:
        List of paths to the extracted frames
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"Failed to open video file: {video_path}")
            return []
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        logger.info(f"Video properties: FPS={fps}, Total frames={total_frames}, Duration={duration:.2f}s")
        
        # Limit to max_duration
        processed_duration = min(duration, max_duration)
        processed_frames = int(processed_duration * fps)
        
        # Calculate frame interval
        if num_frames <= 0 or processed_frames < num_frames:
            actual_frames = min(10, processed_frames)
        else:
            actual_frames = num_frames
            
        if processed_frames <= 0 or actual_frames <= 0:
            logger.error(f"Invalid processed frames: {processed_frames} or actual frames: {actual_frames}")
            return []
            
        interval = processed_frames / actual_frames
        
        logger.info(f"Extracting {actual_frames} frames with interval {interval:.2f} frames")
        
        # Extract frames
        frame_paths = []
        for i in range(actual_frames):
            # Calculate the frame number to extract
            frame_num = int(i * interval)
            
            # Set the frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            
            # Read the frame
            ret, frame = cap.read()
            if not ret:
                logger.warning(f"Failed to read frame {i} (position {frame_num})")
                break
            
            # Save the frame
            frame_path = os.path.join(output_dir, f"frame_{i:03d}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            logger.debug(f"Extracted frame {i} to {frame_path}")
        
        # Release the video capture
        cap.release()
        
        logger.info(f"Successfully extracted {len(frame_paths)} frames from {video_path}")
        return frame_paths
    
    except Exception as e:
        logger.exception(f"Error extracting frames from video: {str(e)}")
        return []

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
        "👋 Welcome to AR-MED Posture Analysis Bot!\n\n"
        "I can analyze posture from images or videos and provide detailed reports.\n\n"
        "Send me a photo or video (up to 6 seconds) of a person standing, "
        "and I'll analyze their posture and provide a comprehensive report.\n\n"
        "Type /help for more information on how to get the best results.")

# Handle /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Tips for Good Photos", callback_data="tips_photo"),
        types.InlineKeyboardButton("Tips for Videos", callback_data="tips_video")
    )
    markup.row(
        types.InlineKeyboardButton("About Posture Analysis", callback_data="about")
    )
    
    bot.send_message(message.chat.id,
        "📋 *How to use AR-MED Bot:*\n\n"
        "1. Send a full-body photo or short video (max 6 seconds)\n"
        "2. Wait for processing (typically 30-60 seconds)\n"
        "3. Receive your analysis visualization and detailed PDF report\n\n"
        "Click a button below for more information:",
        parse_mode="Markdown",
        reply_markup=markup)

# Handle callback queries from inline buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "tips_photo":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
            "📸 *Tips for Good Photos:*\n\n"
            "• Take a full body photo (head to toe)\n"
            "• Stand naturally against a plain background\n"
            "• Wear fitted clothing (not baggy)\n"
            "• Face the camera directly or from the side\n"
            "• Ensure good, even lighting\n"
            "• Have someone else take the photo if possible",
            parse_mode="Markdown")
            
    elif call.data == "tips_video":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
            "🎥 *Tips for Good Videos:*\n\n"
            "• Record a 3-6 second video\n"
            "• Start facing the camera, then slowly rotate 360°\n"
            "• Keep a steady pace while rotating\n"
            "• Maintain good posture throughout\n"
            "• Ensure good lighting from all angles\n"
            "• Wear fitted clothing for better landmark detection",
            parse_mode="Markdown")
            
    elif call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
            "ℹ️ *About AR-MED Posture Analysis:*\n\n"
            "AR-MED uses advanced AI and computer vision to analyze your posture.\n\n"
            "The analysis identifies potential issues with:\n"
            "• Knee alignment (knock knees or bow legs)\n"
            "• Shoulder balance\n"
            "• Hip alignment\n"
            "• Overall vertical posture\n\n"
            "Video analysis is more comprehensive as it examines your posture from multiple angles.\n\n"
            "*Remember:* This analysis is for informational purposes only. For professional advice, please consult with a healthcare provider.",
            parse_mode="Markdown")

# Handle photo messages
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Inform user processing has begun
        status_msg = bot.send_message(message.chat.id, "📸 Received your photo. Beginning posture analysis...")
        
        # Get the largest photo (best resolution)
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Create a unique file name
        unique_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_FOLDER, f"telegram_photo_{unique_id}.jpg")
        
        # Save the file
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Update status
        bot.edit_message_text("🔍 Analyzing posture in your photo...", 
                             message.chat.id, status_msg.message_id)
        
        # Process the image
        result = analyze_posture(file_path, visualization=True, generate_pdf=True, return_data=True)
        
        if isinstance(result, dict) and result.get("error"):
            bot.edit_message_text(f"❌ Analysis error: {result.get('error')}", 
                                 message.chat.id, status_msg.message_id)
            return
        
        # Update status
        bot.edit_message_text("📊 Analysis complete! Preparing your report...", 
                             message.chat.id, status_msg.message_id)
        
        # Send visualization image
        with open(result["visualization_path"], 'rb') as vis:
            bot.send_photo(message.chat.id, vis, 
                           caption="🔍 Posture analysis visualization")
        
        # Send PDF report
        with open(result["pdf_path"], 'rb') as pdf:
            bot.send_document(message.chat.id, pdf, 
                             caption="📋 Your detailed posture analysis report")
        
        # Complete status message
        bot.edit_message_text("✅ Posture analysis completed successfully!", 
                             message.chat.id, status_msg.message_id)
        
        # Send follow-up message with disclaimer
        bot.send_message(message.chat.id,
            "⚠️ *Important Note:* This analysis is for informational purposes only. "
            "For professional advice, please consult with a healthcare provider.",
            parse_mode="Markdown")
            
    except Exception as e:
        logger.exception(f"Error processing photo: {str(e)}")
        bot.send_message(message.chat.id, 
            f"❌ An error occurred during processing: {str(e)}\n\nPlease try again with a different photo.")

# Handle video messages
@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        # Check video duration (Telegram provides this info)
        if message.video.duration > 10:
            bot.reply_to(message, 
                "⚠️ Video is too long. Please send a video of maximum 6 seconds for optimal analysis.")
            return
            
        # Inform user processing has begun
        status_msg = bot.send_message(message.chat.id, 
            "🎥 Received your video. Starting multi-frame posture analysis...")
        
        # Get video file
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Create a unique file name
        unique_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_FOLDER, f"telegram_video_{unique_id}.mp4")
        
        # Save the file
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Update status
        bot.edit_message_text("🎬 Extracting frames from video...", 
                             message.chat.id, status_msg.message_id)
            
        # Create frames directory
        frames_dir = os.path.join(FRAMES_FOLDER, unique_id)
        os.makedirs(frames_dir, exist_ok=True)
        
        # Extract frames
        frame_paths = extract_frames(file_path, frames_dir)
        
        if len(frame_paths) < 5:
            bot.edit_message_text(
                "❌ Could not extract enough frames from video. Please send a clearer video with at least 3 seconds of content.", 
                message.chat.id, status_msg.message_id)
            return
            
        # Update status
        bot.edit_message_text(f"🔍 Analyzing {len(frame_paths)} frames from your video...", 
                             message.chat.id, status_msg.message_id)
        
        # Process each frame
        analysis_results = []
        for i, frame_path in enumerate(frame_paths):
            result = analyze_posture(frame_path, visualization=True, generate_pdf=False, return_data=True)
            if isinstance(result, dict) and not result.get("error"):
                result['frame_number'] = i + 1
                result['frame_path'] = frame_path
                analysis_results.append(result)
        
        if not analysis_results:
            bot.edit_message_text(
                "❌ Failed to analyze frames from your video. Please try with better lighting and positioning.", 
                message.chat.id, status_msg.message_id)
            return
            
        # Update status
        bot.edit_message_text(
            f"📊 Successfully analyzed {len(analysis_results)} frames. Creating your comprehensive report...", 
            message.chat.id, status_msg.message_id)
        
        # Set up report paths
        report_filename = f"video_analysis_{unique_id}.pdf"
        report_path = os.path.join(PDF_FOLDER, report_filename)
        visualization_filename = f"video_visualization_{unique_id}.jpg"
        visualization_path = os.path.join(VISUALIZATIONS_FOLDER, visualization_filename)
        
        # Generate aggregated report
        result = create_aggregated_report(
            analysis_results,
            report_path,
            visualization_path,
            frame_paths[:min(4, len(frame_paths))]
        )
        
        if result.get("error"):
            bot.edit_message_text(f"❌ Error creating report: {result.get('error')}", 
                                 message.chat.id, status_msg.message_id)
            return
            
        # Update status
        bot.edit_message_text("✅ Analysis complete! Sending your results...", 
                             message.chat.id, status_msg.message_id)
        
        # Send visualization image
        with open(visualization_path, 'rb') as vis:
            bot.send_photo(message.chat.id, vis, 
                caption=f"🔍 Multi-frame analysis visualization (from {len(analysis_results)} frames)")
        
        # Send PDF report
        with open(report_path, 'rb') as pdf:
            bot.send_document(message.chat.id, pdf, 
                caption="📋 Your comprehensive multi-frame posture analysis report")
        
        # Send follow-up message with additional info
        bot.send_message(message.chat.id,
            "ℹ️ *About Multi-Frame Analysis:*\n\n"
            "The multi-frame analysis provides a more comprehensive assessment by analyzing "
            "posture from multiple angles. This typically offers more accurate results than "
            "single-image analysis.\n\n"
            "⚠️ *Important:* This analysis is for informational purposes only. For professional "
            "advice, please consult with a healthcare provider.",
            parse_mode="Markdown")
            
    except Exception as e:
        logger.exception(f"Error processing video: {str(e)}")
        bot.send_message(message.chat.id, 
            f"❌ An error occurred during processing: {str(e)}\n\nPlease try again with a different video.")

# Handle other message types
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message, 
        "Please send a photo or video for posture analysis, or use these commands:\n"
        "/start - Start the bot\n"
        "/help - Get help and tips")

# Start the bot
if __name__ == "__main__":
    logger.info("Starting AR-MED Telegram Bot...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.exception(f"Bot crashed: {str(e)}")
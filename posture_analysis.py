import cv2
import mediapipe as mp
import numpy as np
import argparse
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import json
import statistics
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
import uuid
from PIL import Image as PILImage
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize MediaPipe Pose globally to avoid re-initialization for each frame
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Create a single pose detector instance with appropriate settings
pose_detector = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=False,
    min_detection_confidence=0.7
)

def create_pdf_report(image_path, analysis_data, visualization_path=None):
    """
    Create a detailed PDF report of the posture analysis
    
    Args:
        image_path (str): Path to the original image
        analysis_data (dict): Dictionary containing all analysis data
        visualization_path (str): Path to the visualization image if available
    
    Returns:
        str: Path to the generated PDF file
    """
    # Set up the PDF document
    output_dir = os.path.dirname(image_path)
    base_name = os.path.basename(image_path).rsplit('.', 1)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(output_dir, f"{base_name}_posture_analysis_{timestamp}.pdf")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6
    )
    
    subheading_style = ParagraphStyle(
        'Subheading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    important_style = ParagraphStyle(
        'Important',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=colors.red,
        fontName='Helvetica-Bold'
    )
    
    status_style_good = ParagraphStyle(
        'StatusGood',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=8,
        textColor=colors.green,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        borderWidth=1,
        borderColor=colors.green,
        borderPadding=5,
        borderRadius=5
    )
    
    status_style_mild = ParagraphStyle(
        'StatusMild',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=8,
        textColor=colors.orange,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        borderWidth=1,
        borderColor=colors.orange,
        borderPadding=5,
        borderRadius=5
    )
    
    status_style_serious = ParagraphStyle(
        'StatusSerious',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=8,
        textColor=colors.red,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        borderWidth=1,
        borderColor=colors.red,
        borderPadding=5,
        borderRadius=5
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    
    # Start building the content
    content = []
    
    # Title
    content.append(Paragraph(f"Posture Analysis Report", title_style))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    content.append(Paragraph(f"Image: {os.path.basename(image_path)}", normal_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Calculate the ratio of normal to total measurements
    normal_count = 0
    total_count = 0
    for name, data in analysis_data["measurements"].items():
        if 'status' in data and data['status'] != "Informational":
            total_count += 1
            if data['status'] == "Normal":
                normal_count += 1
    
    # Create summary status statement
    if total_count > 0:
        normal_ratio = normal_count / total_count
        
        if normal_ratio >= 0.7:  # More than 70% normal
            status_msg = "NO SERIOUS ISSUES DETECTED"
            status_style = status_style_good
        elif normal_ratio >= 0.5:  # 50-70% normal
            status_msg = "MILD POSTURE CONCERNS"
            status_style = status_style_mild
        else:  # Less than 50% normal
            status_msg = "POSTURE ISSUES REQUIRING ATTENTION"
            status_style = status_style_serious
            
        # Add the status message
        content.append(Paragraph(status_msg, status_style))
        content.append(Spacer(1, 0.1*inch))
    
    # Add original image to report
    if os.path.exists(image_path):
        img_width = 3.5*inch
        content.append(Paragraph("Original Image:", heading_style))
        content.append(Image(image_path, width=img_width, height=img_width*0.75))
        content.append(Spacer(1, 0.2*inch))
    
    # Add visualization to report
    if visualization_path and os.path.exists(visualization_path):
        img_width = 3.5*inch
        content.append(Paragraph("Analysis Visualization:", heading_style))
        content.append(Image(visualization_path, width=img_width, height=img_width*0.75))
        content.append(Spacer(1, 0.2*inch))
    
    # NEW SECTION: What This Means For You
    content.append(Paragraph("What This Means For You", heading_style))
    
    # Check for issues in analysis data and provide simple explanations
    has_issues = False
    simple_explanations = []
    
    # Check knee alignment
    left_knee_dev = None
    right_knee_dev = None
    for name, data in analysis_data["measurements"].items():
        if name == "Left Knee Deviation":
            left_knee_dev = data
        elif name == "Right Knee Deviation":
            right_knee_dev = data
    
    if left_knee_dev and right_knee_dev:
        if left_knee_dev['status'] == "Abnormal" and right_knee_dev['status'] == "Abnormal":
            if left_knee_dev['value'] > 0.1 and right_knee_dev['value'] < -0.1:
                simple_explanations.append(Paragraph("<b>Knee Alignment:</b> Your knees appear to be angling inward (knock knees). This may affect your balance and could contribute to knee pain over time.", normal_style))
                has_issues = True
            elif left_knee_dev['value'] < -0.1 and right_knee_dev['value'] > 0.1:
                simple_explanations.append(Paragraph("<b>Knee Alignment:</b> Your knees appear to be angling outward (bow legs). This can affect how weight is distributed across your joints.", normal_style))
                has_issues = True
    
    # Check shoulder alignment
    shoulder_diff = None
    for name, data in analysis_data["measurements"].items():
        if name == "Shoulder Height Difference":
            shoulder_diff = data
            break
    
    if shoulder_diff and shoulder_diff['status'] == "Abnormal":
        simple_explanations.append(Paragraph("<b>Shoulder Alignment:</b> Your shoulders appear uneven. This could be due to posture habits, muscle imbalance, or how you were standing.", normal_style))
        has_issues = True
    
    # Check hip alignment
    hip_diff = None
    for name, data in analysis_data["measurements"].items():
        if name == "Hip Height Difference":
            hip_diff = data
            break
    
    if hip_diff and hip_diff['status'] == "Abnormal":
        simple_explanations.append(Paragraph("<b>Hip Alignment:</b> Your hips appear uneven. This might affect your walking pattern and could potentially lead to back or knee issues if persistent.", normal_style))
        has_issues = True
    
    # Check vertical alignment
    vertical_align = None
    for name, data in analysis_data["measurements"].items():
        if name == "Vertical Alignment":
            vertical_align = data
            break
    
    if vertical_align and vertical_align['status'] == "Abnormal":
        if vertical_align['value'] > 0.1:
            simple_explanations.append(Paragraph("<b>Overall Posture:</b> You appear to be leaning forward. This can put extra stress on your back and neck.", normal_style))
        else:
            simple_explanations.append(Paragraph("<b>Overall Posture:</b> You appear to be leaning backward. This can put extra stress on your lower back.", normal_style))
        has_issues = True
    
    # If no issues found
    if not has_issues:
        simple_explanations.append(Paragraph("<b>Good news!</b> We didn't detect any significant posture issues in this image. Your body alignment appears to be within normal ranges.", normal_style))
    else:
        # Add overall summary for issues
        content.append(Paragraph("We've identified some potential posture patterns you might want to address. Remember that a single image analysis has limitations - consult with a healthcare professional for a complete assessment.", normal_style))
    
    # Add all explanations
    for explanation in simple_explanations:
        content.append(explanation)
    
    # Add next steps
    content.append(Spacer(1, 0.1*inch))
    content.append(Paragraph("<b>What to do next:</b>", normal_style))
    
    if has_issues and "recommendations" in analysis_data and analysis_data["recommendations"]:
        content.append(Paragraph("Based on this analysis, consider:", normal_style))
        for rec in analysis_data["recommendations"]:
            content.append(Paragraph(f"• {rec}", normal_style))
    else:
        content.append(Paragraph("• Continue maintaining good posture habits", normal_style))
        content.append(Paragraph("• Consider periodic posture checks, especially if you spend long hours sitting", normal_style))
    
    content.append(Spacer(1, 0.2*inch))
    
    # Summary section (original)
    content.append(Paragraph("Analysis Summary", heading_style))
    
    # Create a table for the summary instead of paragraphs
    summary_data = [
        [Paragraph("Finding", table_header_style), 
         Paragraph("Details", table_header_style)]
    ]
    
    # Row styles for the summary table
    summary_row_styles = []
    summary_row_styles.append(('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey))
    summary_row_styles.append(('TEXTCOLOR', (0, 0), (-1, 0), colors.black))
    summary_row_styles.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
    summary_row_styles.append(('ALIGN', (1, 0), (1, -1), 'LEFT'))
    summary_row_styles.append(('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
    summary_row_styles.append(('BOTTOMPADDING', (0, 0), (-1, 0), 12))
    summary_row_styles.append(('GRID', (0, 0), (-1, -1), 1, colors.black))
    summary_row_styles.append(('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
    
    # Keep track of row index
    row_idx = 1
    
    for issue, details in analysis_data["summary"].items():
        # Color code the row based on content
        if any(negative in details.lower() for negative in ["issue", "abnormal", "imbalance", "deviat", "concern", "error"]):
            # Highlight entire row for abnormal
            summary_row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightcoral))
            summary_row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.white))
        elif any(positive in details.lower() for positive in ["normal", "no significant", "good"]):
            # Highlight entire row for normal
            summary_row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightgreen))
            summary_row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.darkgreen))
            
        summary_data.append([issue, details])
        row_idx += 1
    
    # Create and style the table
    summary_table = Table(summary_data, colWidths=[1.5*inch, 5*inch])
    summary_table.setStyle(TableStyle(summary_row_styles))
    
    # Add the table to content
    content.append(summary_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Detailed measurements section
    content.append(Paragraph("Detailed Measurements", heading_style))
    
    # Create tables for each set of measurements
    landmark_data = [
        [Paragraph("Landmark", table_header_style), 
         Paragraph("X (normalized)", table_header_style), 
         Paragraph("Y (normalized)", table_header_style),
         Paragraph("X (pixels)", table_header_style),
         Paragraph("Y (pixels)", table_header_style),
         Paragraph("Visibility", table_header_style)]
    ]
    
    for name, data in analysis_data["landmarks"].items():
        landmark_data.append([
            name,
            f"{data['x_norm']:.4f}",
            f"{data['y_norm']:.4f}",
            f"{data['x_px']:.1f}",
            f"{data['y_px']:.1f}",
            f"{data['visibility']:.4f}"
        ])
    
    landmark_table = Table(landmark_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    landmark_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    content.append(landmark_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Measurements table
    content.append(Paragraph("Posture Measurements", heading_style))
    
    measurements_data = [
        [Paragraph("Measurement", table_header_style), 
         Paragraph("Value", table_header_style), 
         Paragraph("Threshold", table_header_style),
         Paragraph("Status", table_header_style)]
    ]
    
    # Row styles for the measurements table
    row_styles = []
    row_styles.append(('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey))
    row_styles.append(('TEXTCOLOR', (0, 0), (-1, 0), colors.black))
    row_styles.append(('ALIGN', (0, 0), (-1, -1), 'CENTER'))
    row_styles.append(('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
    row_styles.append(('BOTTOMPADDING', (0, 0), (-1, 0), 12))
    row_styles.append(('GRID', (0, 0), (-1, -1), 1, colors.black))
    row_styles.append(('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
    
    # Keep track of row index as we add data
    row_idx = 1
    
    for name, data in analysis_data["measurements"].items():
        # Add color coding for status
        if data['status'] == "Abnormal":
            status_cell = Paragraph(data['status'], ParagraphStyle('Abnormal', parent=normal_style, textColor=colors.white, fontName='Helvetica-Bold'))
            # Highlight entire row for abnormal
            row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightcoral))
            row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.white))
        elif data['status'] == "Normal":
            status_cell = Paragraph(data['status'], ParagraphStyle('Normal', parent=normal_style, textColor=colors.white, fontName='Helvetica-Bold'))
            # Highlight entire row for normal
            row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightgreen))
            row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.darkgreen))
        else:
            status_cell = data['status']
            
        measurements_data.append([
            name,
            f"{data['value']:.4f}",
            f"{data['threshold']:.4f}" if 'threshold' in data else "N/A",
            status_cell
        ])
        row_idx += 1
    
    measurements_table = Table(measurements_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    measurements_table.setStyle(TableStyle(row_styles))
    
    content.append(measurements_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Recommendations section
    if "recommendations" in analysis_data:
        content.append(Paragraph("Recommendations", heading_style))
        for recommendation in analysis_data["recommendations"]:
            content.append(Paragraph(f"• {recommendation}", normal_style))
        content.append(Spacer(1, 0.2*inch))
    
    # Disclaimer
    content.append(Paragraph("Disclaimer", heading_style))
    content.append(Paragraph(
        "This analysis is preliminary and based on 2D image data. For an accurate diagnosis, "
        "please consult a medical professional. The measurements and assessments are intended "
        "for informational purposes only and should not be used as the sole basis for medical decisions.",
        normal_style
    ))
    
    # Build and save the PDF
    doc.build(content)
    
    return pdf_path

def analyze_posture(image_path, visualization=False, min_detection_confidence=0.7, generate_pdf=True, return_data=False):
    """
    Analyze posture from an image, detecting knee and shoulder alignment issues.
    
    Args:
        image_path (str): Path to the input image
        visualization (bool): Whether to save a visualization of the analysis
        min_detection_confidence (float): Threshold for pose detection confidence
        generate_pdf (bool): Whether to generate a PDF report
        return_data (bool): Whether to return analysis data as a dictionary instead of a string
        
    Returns:
        str or dict: Analysis report string, PDF path, or dictionary with analysis data
    """
    try:
        # Load the input image
        image = cv2.imread(image_path)

        if image is None:
            logger.error(f"Could not load image from {image_path}")
            return "Error: Could not load image." if not return_data else {"error": "Could not load image."}

        image_height, image_width, _ = image.shape
        
        # Initialize the report string and data dictionary for PDF
        report = "Posture Analysis Report:\n"
        analysis_data = {
            "summary": {},
            "landmarks": {},
            "measurements": {},
            "recommendations": []
        }

        # Process the image to detect pose landmarks
        # Use the global pose_detector instead of creating a new one
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose_detector.process(rgb_image)

        if not results.pose_landmarks:
            logger.warning(f"No pose landmarks detected in {image_path}")
            return "Error: No pose landmarks detected in the image." if not return_data else {"error": "No pose landmarks detected in the image."}

        landmarks = results.pose_landmarks.landmark
        visualization_path = None
        
        # Create a copy for visualization if needed
        if visualization:
            vis_image = image.copy()
            mp_drawing.draw_landmarks(
                vis_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        # Check if required landmarks are detected with sufficient confidence
        required_landmarks = [
            (mp_pose.PoseLandmark.LEFT_HIP, "Left Hip"),
            (mp_pose.PoseLandmark.RIGHT_HIP, "Right Hip"),
            (mp_pose.PoseLandmark.LEFT_KNEE, "Left Knee"),
            (mp_pose.PoseLandmark.RIGHT_KNEE, "Right Knee"),
            (mp_pose.PoseLandmark.LEFT_SHOULDER, "Left Shoulder"),
            (mp_pose.PoseLandmark.RIGHT_SHOULDER, "Right Shoulder"),
            (mp_pose.PoseLandmark.LEFT_ANKLE, "Left Ankle"),
            (mp_pose.PoseLandmark.RIGHT_ANKLE, "Right Ankle"),
            (mp_pose.PoseLandmark.LEFT_ELBOW, "Left Elbow"),
            (mp_pose.PoseLandmark.RIGHT_ELBOW, "Right Elbow"),
            (mp_pose.PoseLandmark.LEFT_WRIST, "Left Wrist"),
            (mp_pose.PoseLandmark.RIGHT_WRIST, "Right Wrist"),
            (mp_pose.PoseLandmark.NOSE, "Nose"),
            (mp_pose.PoseLandmark.LEFT_EAR, "Left Ear"),
            (mp_pose.PoseLandmark.RIGHT_EAR, "Right Ear")
        ]
        
        # Store all landmark data
        for landmark, name in required_landmarks:
            lm = landmarks[landmark.value]
            analysis_data["landmarks"][name] = {
                "x_norm": lm.x,
                "y_norm": lm.y,
                "z_norm": lm.z,
                "visibility": lm.visibility,
                "x_px": lm.x * image_width,
                "y_px": lm.y * image_height
            }
            
            # Check visibility for critical landmarks
            if landmark.value <= mp_pose.PoseLandmark.RIGHT_SHOULDER.value and lm.visibility < 0.5:
                error_msg = f"Error: {name} landmark not clearly visible (confidence: {lm.visibility:.2f})"
                if return_data:
                    analysis_data["summary"]["Visibility Issues"] = error_msg
                    return analysis_data
                elif not generate_pdf:
                    return error_msg
                analysis_data["summary"]["Visibility Issues"] = error_msg

        # Extract coordinates of relevant landmarks
        LH = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        RH = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        LK = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        RK = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        LS = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        RS = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        LA = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        RA = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        NOSE = landmarks[mp_pose.PoseLandmark.NOSE.value]
        
        # Convert normalized coordinates to pixel values for key points
        LH_x, LH_y = LH.x * image_width, LH.y * image_height
        RH_x, RH_y = RH.x * image_width, RH.y * image_height
        LK_x, LK_y = LK.x * image_width, LK.y * image_height
        RK_x, RK_y = RK.x * image_width, RK.y * image_height
        LS_x, LS_y = LS.x * image_width, LS.y * image_height
        RS_x, RS_y = RS.x * image_width, RS.y * image_height
        LA_x, LA_y = LA.x * image_width, LA.y * image_height
        RA_x, RA_y = RA.x * image_width, RA.y * image_height
        NOSE_x, NOSE_y = NOSE.x * image_width, NOSE.y * image_height
        
        # Compute hip width for normalization (use absolute value to handle any orientation)
        hip_width = abs(RH_x - LH_x)
        
        if hip_width < 1.0:  # Using a small threshold to avoid division by zero
            error_msg = "Warning: Hip landmarks may be misidentified. Hip width too small for reliable analysis."
            if return_data:
                analysis_data["summary"]["Hip Width Issue"] = error_msg
                return analysis_data
            elif not generate_pdf:
                return error_msg
            analysis_data["summary"]["Hip Width Issue"] = error_msg
        
        # ----- DETAILED MEASUREMENTS -----
        
        # 1. Compute knee deviations normalized by hip width
        left_knee_deviation = (LK_x - LH_x) / hip_width
        right_knee_deviation = (RK_x - RH_x) / hip_width

        # 2. Compute shoulder height difference normalized by image height
        shoulder_diff = (LS_y - RS_y) / image_height
        
        # 3. Compute hip height difference normalized by image height
        hip_diff = (LH_y - RH_y) / image_height
        
        # 4. Compute ankle position relative to knees
        left_ankle_knee_diff = (LA_x - LK_x) / hip_width
        right_ankle_knee_diff = (RA_x - RK_x) / hip_width
        
        # 5. Compute shoulder width
        shoulder_width = abs(RS_x - LS_x)
        shoulder_hip_ratio = shoulder_width / hip_width
        
        # 6. Compute vertical alignment (nose to midpoint of hips)
        mid_hip_x = (LH_x + RH_x) / 2
        vertical_alignment = (NOSE_x - mid_hip_x) / hip_width
        
        # Store all measurements in the data dictionary
        analysis_data["measurements"]["Left Knee Deviation"] = {
            "value": left_knee_deviation,
            "threshold": 0.1,
            "status": "Abnormal" if abs(left_knee_deviation) > 0.1 else "Normal"
        }
        
        analysis_data["measurements"]["Right Knee Deviation"] = {
            "value": right_knee_deviation,
            "threshold": 0.1,
            "status": "Abnormal" if abs(right_knee_deviation) > 0.1 else "Normal"
        }
        
        analysis_data["measurements"]["Shoulder Height Difference"] = {
            "value": shoulder_diff,
            "threshold": 0.05,
            "status": "Abnormal" if abs(shoulder_diff) > 0.05 else "Normal"
        }
        
        analysis_data["measurements"]["Hip Height Difference"] = {
            "value": hip_diff,
            "threshold": 0.05,
            "status": "Abnormal" if abs(hip_diff) > 0.05 else "Normal"
        }
        
        analysis_data["measurements"]["Left Ankle-Knee Alignment"] = {
            "value": left_ankle_knee_diff,
            "threshold": 0.15,
            "status": "Abnormal" if abs(left_ankle_knee_diff) > 0.15 else "Normal"
        }
        
        analysis_data["measurements"]["Right Ankle-Knee Alignment"] = {
            "value": right_ankle_knee_diff,
            "threshold": 0.15,
            "status": "Abnormal" if abs(right_ankle_knee_diff) > 0.15 else "Normal"
        }
        
        analysis_data["measurements"]["Shoulder-Hip Ratio"] = {
            "value": shoulder_hip_ratio,
            "status": "Informational"
        }
        
        analysis_data["measurements"]["Vertical Alignment"] = {
            "value": vertical_alignment,
            "threshold": 0.1,
            "status": "Abnormal" if abs(vertical_alignment) > 0.1 else "Normal"
        }

        # Define thresholds for detecting abnormalities
        knee_threshold = 0.1  # Threshold for knee deviation
        shoulder_threshold = 0.05  # Threshold for shoulder imbalance
        
        # ----- ANALYSIS AND RECOMMENDATIONS -----

        # Analyze knee alignment for knocked knees or bow legs
        report += "\nLeg Alignment:\n"
        if left_knee_deviation > knee_threshold and right_knee_deviation < -knee_threshold:
            leg_issue = f"Possible knocked knees detected (Left deviation: {left_knee_deviation:.2f}, Right deviation: {right_knee_deviation:.2f})."
            report += f"- {leg_issue}\n"
            report += "- This condition may affect stability and performance in physical tests.\n"
            analysis_data["summary"]["Leg Alignment"] = leg_issue
            analysis_data["recommendations"].append("Consider exercises that strengthen the hip abductors and improve knee stability.")
        elif left_knee_deviation < -knee_threshold and right_knee_deviation > knee_threshold:
            leg_issue = f"Possible bow legs detected (Left deviation: {left_knee_deviation:.2f}, Right deviation: {right_knee_deviation:.2f})."
            report += f"- {leg_issue}\n"
            report += "- This condition may impact mobility during physical tests.\n"
            analysis_data["summary"]["Leg Alignment"] = leg_issue
            analysis_data["recommendations"].append("Focus on exercises that strengthen the hip adductors and improve knee alignment.")
        else:
            leg_status = f"No significant leg alignment issues detected (Left deviation: {left_knee_deviation:.2f}, Right deviation: {right_knee_deviation:.2f})."
            report += f"- {leg_status}\n"
            analysis_data["summary"]["Leg Alignment"] = leg_status

        # Analyze shoulder alignment
        report += "\nShoulder Alignment:\n"
        if abs(shoulder_diff) > shoulder_threshold:
            shoulder_issue = f"Possible shoulder imbalance detected (Difference: {shoulder_diff:.2f})."
            report += f"- {shoulder_issue}\n"
            report += "- This may indicate asymmetry that could affect upper body strength tests.\n"
            analysis_data["summary"]["Shoulder Alignment"] = shoulder_issue
            analysis_data["recommendations"].append("Work on exercises to improve posture and shoulder alignment, such as rows and face pulls.")
        else:
            shoulder_status = f"No significant shoulder imbalance detected (Difference: {shoulder_diff:.2f})."
            report += f"- {shoulder_status}\n"
            analysis_data["summary"]["Shoulder Alignment"] = shoulder_status
        
        # Analyze hip alignment
        report += "\nHip Alignment:\n"
        if abs(hip_diff) > shoulder_threshold:
            hip_issue = f"Possible hip height imbalance detected (Difference: {hip_diff:.2f})."
            report += f"- {hip_issue}\n"
            report += "- This may indicate potential leg length discrepancy or pelvic tilt.\n"
            analysis_data["summary"]["Hip Alignment"] = hip_issue
            analysis_data["recommendations"].append("Consider assessment for potential leg length discrepancy or pelvic alignment issues.")
        else:
            hip_status = f"No significant hip height imbalance detected (Difference: {hip_diff:.2f})."
            report += f"- {hip_status}\n"
            analysis_data["summary"]["Hip Alignment"] = hip_status
        
        # Analyze overall posture
        report += "\nOverall Posture:\n"
        if abs(vertical_alignment) > 0.1:
            posture_issue = f"Possible forward/backward lean detected (Deviation: {vertical_alignment:.2f})."
            report += f"- {posture_issue}\n"
            analysis_data["summary"]["Overall Posture"] = posture_issue
            analysis_data["recommendations"].append("Practice exercises to strengthen core and improve overall posture alignment.")
        else:
            posture_status = f"Good vertical alignment (Deviation: {vertical_alignment:.2f})."
            report += f"- {posture_status}\n"
            analysis_data["summary"]["Overall Posture"] = posture_status

        # Add a disclaimer
        disclaimer = "Note: This analysis is preliminary and based on 2D image data. For an accurate diagnosis, consult a medical professional."
        report += f"\n{disclaimer}\n"
        
        # Save visualization if requested
        if visualization:
            # Draw lines to show knee alignment
            knee_line_color = (0, 0, 255)  # Red for issues
            normal_line_color = (0, 255, 0)  # Green for normal
            
            # Left knee
            knee_color = knee_line_color if abs(left_knee_deviation) > knee_threshold else normal_line_color
            cv2.line(vis_image, 
                     (int(LH_x), int(LH_y)), 
                     (int(LK_x), int(LK_y)), 
                     knee_color, 2)
            
            # Right knee
            knee_color = knee_line_color if abs(right_knee_deviation) > knee_threshold else normal_line_color
            cv2.line(vis_image, 
                     (int(RH_x), int(RH_y)), 
                     (int(RK_x), int(RK_y)), 
                     knee_color, 2)
            
            # Shoulder alignment
            shoulder_color = knee_line_color if abs(shoulder_diff) > shoulder_threshold else normal_line_color
            cv2.line(vis_image, 
                     (int(LS_x), int(LS_y)), 
                     (int(RS_x), int(RS_y)), 
                     shoulder_color, 2)
            
            # Hip alignment
            hip_color = knee_line_color if abs(hip_diff) > shoulder_threshold else normal_line_color
            cv2.line(vis_image, 
                     (int(LH_x), int(LH_y)), 
                     (int(RH_x), int(RH_y)), 
                     hip_color, 2)
            
            # Vertical alignment
            vertical_color = knee_line_color if abs(vertical_alignment) > 0.1 else normal_line_color
            mid_hip_x_px = int(mid_hip_x)
            mid_hip_y_px = int((LH_y + RH_y) / 2)
            cv2.line(vis_image, 
                     (mid_hip_x_px, mid_hip_y_px), 
                     (int(NOSE_x), int(NOSE_y)), 
                     vertical_color, 2)
            
            # Add labels
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_color = (255, 255, 255)
            line_type = 2
            
            # Add measurements as text on image
            cv2.putText(vis_image, f"LK Dev: {left_knee_deviation:.2f}", 
                        (int(LK_x), int(LK_y)-10), font, font_scale, font_color, line_type)
            cv2.putText(vis_image, f"RK Dev: {right_knee_deviation:.2f}", 
                        (int(RK_x), int(RK_y)-10), font, font_scale, font_color, line_type)
            cv2.putText(vis_image, f"Shoulder Diff: {shoulder_diff:.2f}", 
                        (int((LS_x + RS_x)/2), int((LS_y + RS_y)/2)-10), font, font_scale, font_color, line_type)
            
            # Save the visualization
            visualization_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visualizations")
            os.makedirs(visualization_dir, exist_ok=True)
            visualization_filename = f"visualization_{uuid.uuid4()}.jpg"
            visualization_path = os.path.join(visualization_dir, visualization_filename)
            cv2.imwrite(visualization_path, vis_image)
            report += f"\nVisualization saved as {visualization_path}\n"
            
            # Add visualization path to data if returning data
            if return_data:
                analysis_data["visualization_path"] = visualization_path
        
        # Generate PDF if requested
        if generate_pdf:
            pdf_path = create_pdf_report(image_path, analysis_data, visualization_path)
            
            # If returning data, include the PDF path in the data
            if return_data:
                analysis_data["pdf_path"] = pdf_path
                return analysis_data
            
            return f"Detailed analysis completed. PDF report generated at: {pdf_path}"
        
        # Return data if requested
        if return_data:
            return analysis_data
        
        # Otherwise return report text
        return report

    except Exception as e:
        logger.exception(f"Error in analyze_posture: {str(e)}")
        return {"error": f"Analysis failed: {str(e)}"}

def create_aggregated_report(analysis_results, report_path, visualization_path=None, frame_paths=None):
    """
    Create a detailed PDF report aggregating analyses from multiple video frames
    
    Args:
        analysis_results (list): List of dictionaries with analysis data for each frame
        report_path (str): Path where the PDF report should be saved
        visualization_path (str, optional): Path where a visualization image should be saved
        frame_paths (list, optional): List of paths to frames to include in the visualization
        
    Returns:
        dict: Result dictionary with status or error
    """
    try:
        # Set up the PDF document
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=10
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6
        )
        
        subheading_style = ParagraphStyle(
            'Subheading',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=6
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        important_style = ParagraphStyle(
            'Important',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=colors.red,
            fontName='Helvetica-Bold'
        )
        
        status_style_good = ParagraphStyle(
            'StatusGood',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=8,
            textColor=colors.green,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            borderWidth=1,
            borderColor=colors.green,
            borderPadding=5,
            borderRadius=5
        )
        
        status_style_mild = ParagraphStyle(
            'StatusMild',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=8,
            textColor=colors.orange,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            borderWidth=1,
            borderColor=colors.orange,
            borderPadding=5,
            borderRadius=5
        )
        
        status_style_serious = ParagraphStyle(
            'StatusSerious',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=8,
            textColor=colors.red,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            borderWidth=1,
            borderColor=colors.red,
            borderPadding=5,
            borderRadius=5
        )
        
        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Start building the content
        content = []
        
        # Title
        content.append(Paragraph(f"Multi-Frame Posture Analysis Report", title_style))
        content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        content.append(Paragraph(f"Frames analyzed: {len(analysis_results)}", normal_style))
        content.append(Spacer(1, 0.2*inch))
        
        # Create visualization if frame paths are provided
        if visualization_path and frame_paths and len(frame_paths) > 0:
            try:
                # Create a grid visualization of selected frames
                n_frames = min(4, len(frame_paths))
                rows = (n_frames + 1) // 2  # Ceiling division
                cols = min(2, n_frames)
                
                fig, axes = plt.subplots(rows, cols, figsize=(10, 10 * rows / cols))
                if rows * cols == 1:
                    axes = np.array([axes])
                axes = axes.flatten()
                
                # Add each frame to the grid
                for i, frame_path in enumerate(frame_paths[:n_frames]):
                    img = cv2.imread(frame_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        axes[i].imshow(img)
                        axes[i].set_title(f"Frame {i+1}")
                        axes[i].axis('off')
                
                # Hide any empty subplots
                for i in range(n_frames, len(axes)):
                    axes[i].axis('off')
                
                plt.tight_layout()
                plt.savefig(visualization_path)
                plt.close(fig)
                
                # Add to report
                img_width = 6*inch
                content.append(Paragraph("Frame Samples:", heading_style))
                content.append(Image(visualization_path, width=img_width, height=img_width*0.75))
                content.append(Spacer(1, 0.2*inch))
                
            except Exception as e:
                logger.exception(f"Error creating visualization grid: {str(e)}")
                # Continue with report generation even if visualization fails
        
        # Calculate aggregated measurements
        aggregated_measurements = {}
        measurement_values = {}
        
        # Collect all measurements across frames
        for frame_data in analysis_results:
            if "measurements" in frame_data:
                for measure_name, measure_data in frame_data["measurements"].items():
                    if measure_name not in measurement_values:
                        measurement_values[measure_name] = []
                    
                    measurement_values[measure_name].append(measure_data["value"])
        
        # Calculate statistics for each measurement
        for measure_name, values in measurement_values.items():
            # Skip if no values
            if not values:
                continue
                
            # Get threshold and status from first frame that has this measurement
            threshold = None
            status_type = "Informational"
            
            for frame_data in analysis_results:
                if "measurements" in frame_data and measure_name in frame_data["measurements"]:
                    if "threshold" in frame_data["measurements"][measure_name]:
                        threshold = frame_data["measurements"][measure_name]["threshold"]
                    status_type = frame_data["measurements"][measure_name]["status"]
                    break
            
            # Calculate statistics
            avg_value = statistics.mean(values)
            min_value = min(values)
            max_value = max(values)
            std_dev = statistics.stdev(values) if len(values) > 1 else 0
            
            # Determine aggregated status
            if threshold:
                if abs(avg_value) > threshold:
                    status = "Abnormal"
                else:
                    status = "Normal"
            else:
                status = status_type
                
            # Store aggregated data
            aggregated_measurements[measure_name] = {
                "avg_value": avg_value,
                "min_value": min_value,
                "max_value": max_value,
                "std_dev": std_dev,
                "threshold": threshold,
                "status": status
            }
        
        # Create aggregated recommendations
        all_recommendations = set()
        for frame_data in analysis_results:
            if "recommendations" in frame_data:
                all_recommendations.update(frame_data["recommendations"])
        
        # Calculate overall status summary
        normal_count = 0
        total_count = 0
        for name, data in aggregated_measurements.items():
            if 'status' in data and data['status'] != "Informational":
                total_count += 1
                if data['status'] == "Normal":
                    normal_count += 1
        
        # Create summary status statement
        if total_count > 0:
            normal_ratio = normal_count / total_count
            
            if normal_ratio >= 0.7:  # More than 70% normal
                status_msg = "NO SERIOUS POSTURE ISSUES DETECTED"
                status_style = status_style_good
            elif normal_ratio >= 0.5:  # 50-70% normal
                status_msg = "MILD POSTURE CONCERNS"
                status_style = status_style_mild
            else:  # Less than 50% normal
                status_msg = "POSTURE ISSUES REQUIRING ATTENTION"
                status_style = status_style_serious
                
            # Add the status message
            content.append(Paragraph(status_msg, status_style))
            content.append(Spacer(1, 0.1*inch))
        
        # Overview
        content.append(Paragraph("Analysis Overview", heading_style))
        content.append(Paragraph(
            "This report contains analysis from multiple moments in your video. "
            "Unlike a single photo, this gives us a more complete picture of your posture during movement. "
            "The results show averages across these moments, which can reveal patterns that might not be visible in just one frame.",
            normal_style))
        content.append(Spacer(1, 0.2*inch))
        
        # NEW SECTION: What This Means For You
        content.append(Paragraph("What This Means For You", heading_style))
        
        # Analyze aggregated measurements to provide simple explanations
        has_issues = False
        simple_explanations = []
        
        # Check knee alignment
        left_knee_avg = aggregated_measurements.get("Left Knee Deviation", {}).get("avg_value", 0)
        right_knee_avg = aggregated_measurements.get("Right Knee Deviation", {}).get("avg_value", 0)
        knee_threshold = 0.1
        
        if left_knee_avg > knee_threshold and right_knee_avg < -knee_threshold:
            simple_explanations.append(Paragraph("<b>Knee Alignment:</b> Your knees appear to be consistently angling inward (knock knees). This pattern may affect your balance and could contribute to knee pain over time.", normal_style))
            has_issues = True
        elif left_knee_avg < -knee_threshold and right_knee_avg > knee_threshold:
            simple_explanations.append(Paragraph("<b>Knee Alignment:</b> Your knees appear to be consistently angling outward (bow legs). This pattern can affect how weight is distributed across your joints.", normal_style))
            has_issues = True
        
        # Shoulder alignment
        shoulder_diff_avg = aggregated_measurements.get("Shoulder Height Difference", {}).get("avg_value", 0)
        shoulder_threshold = 0.05
        
        if abs(shoulder_diff_avg) > shoulder_threshold:
            shoulder_diff_max = aggregated_measurements.get("Shoulder Height Difference", {}).get("max_value", 0)
            shoulder_diff_min = aggregated_measurements.get("Shoulder Height Difference", {}).get("min_value", 0)
            
            # Check if the shoulders are consistently uneven or variable
            if abs(shoulder_diff_min) > shoulder_threshold and abs(shoulder_diff_max) > shoulder_threshold and ((shoulder_diff_min > 0) == (shoulder_diff_max > 0)):
                simple_explanations.append(Paragraph(f"<b>Shoulder Alignment:</b> Your shoulders appear consistently uneven throughout the video. This could indicate a muscle imbalance or postural habit.", normal_style))
            else:
                simple_explanations.append(Paragraph(f"<b>Shoulder Alignment:</b> Your shoulder alignment varies during movement, but tends to be uneven. This might be related to how you distribute weight when moving.", normal_style))
            has_issues = True
        
        # Hip alignment
        hip_diff_avg = aggregated_measurements.get("Hip Height Difference", {}).get("avg_value", 0)
        
        if abs(hip_diff_avg) > shoulder_threshold:
            simple_explanations.append(Paragraph(f"<b>Hip Alignment:</b> Your hips appear uneven during movement. This might affect your walking pattern and could potentially lead to lower back issues if persistent.", normal_style))
            has_issues = True
        
        # Overall posture
        vertical_avg = aggregated_measurements.get("Vertical Alignment", {}).get("avg_value", 0)
        
        if abs(vertical_avg) > 0.1:
            if vertical_avg > 0.1:
                simple_explanations.append(Paragraph(f"<b>Overall Posture:</b> You tend to lean forward during movement. This can put extra strain on your back and neck muscles.", normal_style))
            else:
                simple_explanations.append(Paragraph(f"<b>Overall Posture:</b> You tend to lean backward during movement. This can put extra stress on your lower back.", normal_style))
            has_issues = True
        
        # If no issues found
        if not has_issues:
            content.append(Paragraph("<b>Good news!</b> We didn't detect any significant posture issues in your movement. Your body alignment appears to be within normal ranges.", normal_style))
        else:
            # Add overall summary for issues
            content.append(Paragraph("We've identified some potential posture patterns during your movement. The advantage of video analysis is that we can see how your posture changes over time, giving a more complete picture than a single image.", normal_style))
            content.append(Spacer(1, 0.1*inch))
            
            # Add all explanations
            for explanation in simple_explanations:
                content.append(explanation)
        
        # Add consistency information
        content.append(Spacer(1, 0.1*inch))
        content.append(Paragraph("<b>About Your Movement Consistency:</b>", normal_style))
        
        # Find the measurement with highest variation to comment on
        highest_variation = 0
        highest_var_name = None
        
        for name, data in aggregated_measurements.items():
            if "std_dev" in data and "avg_value" in data and data["avg_value"] != 0:
                variation = abs(data["std_dev"] / data["avg_value"]) if data["avg_value"] != 0 else 0
                if variation > highest_variation:
                    highest_variation = variation
                    highest_var_name = name
        
        if highest_var_name and highest_variation > 0.2:
            content.append(Paragraph(f"Your {highest_var_name.lower()} shows the most variation during movement. This suggests you might benefit from focusing on consistency in this area.", normal_style))
        else:
            content.append(Paragraph("Your posture appears relatively consistent throughout the video, which is a positive sign of stability.", normal_style))
        
        # Add next steps
        content.append(Spacer(1, 0.1*inch))
        content.append(Paragraph("<b>What to do next:</b>", normal_style))
        
        if all_recommendations:
            content.append(Paragraph("Based on this analysis, consider:", normal_style))
            # Use set to avoid duplicate recommendations
            for recommendation in all_recommendations:
                content.append(Paragraph(f"• {recommendation}", normal_style))
        else:
            content.append(Paragraph("• Continue maintaining good posture habits", normal_style))
            content.append(Paragraph("• Consider periodic posture checks, especially during activities you do regularly", normal_style))
        
        content.append(Spacer(1, 0.2*inch))
        
        # Summary section
        content.append(Paragraph("Summary of Findings", heading_style))
        
        # Create a summary of the averaged measurements
        summary_data = [
            [Paragraph("Measurement", table_header_style), 
             Paragraph("Average Value", table_header_style), 
             Paragraph("Min Value", table_header_style),
             Paragraph("Max Value", table_header_style),
             Paragraph("Status", table_header_style)]
        ]
        
        # Row styles for the measurements table
        row_styles = []
        row_styles.append(('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey))
        row_styles.append(('TEXTCOLOR', (0, 0), (-1, 0), colors.black))
        row_styles.append(('ALIGN', (0, 0), (-1, -1), 'CENTER'))
        row_styles.append(('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
        row_styles.append(('BOTTOMPADDING', (0, 0), (-1, 0), 12))
        row_styles.append(('GRID', (0, 0), (-1, -1), 1, colors.black))
        row_styles.append(('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
        
        # Keep track of row index as we add data
        row_idx = 1
        
        for name, data in aggregated_measurements.items():
            # Add color coding for status
            if data['status'] == "Abnormal":
                status_cell = Paragraph(data['status'], ParagraphStyle('Abnormal', parent=normal_style, textColor=colors.white, fontName='Helvetica-Bold'))
                # Highlight entire row for abnormal
                row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightcoral))
                row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.white))
            elif data['status'] == "Normal":
                status_cell = Paragraph(data['status'], ParagraphStyle('Normal', parent=normal_style, textColor=colors.white, fontName='Helvetica-Bold'))
                # Highlight entire row for normal
                row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightgreen))
                row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.darkgreen))
            else:
                status_cell = data['status']
                
            row = [
                name,
                f"{data['avg_value']:.4f}",
                f"{data['min_value']:.4f}",
                f"{data['max_value']:.4f}",
                status_cell
            ]
            summary_data.append(row)
            row_idx += 1
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1*inch])
        summary_table.setStyle(TableStyle(row_styles))
        
        content.append(summary_table)
        content.append(Spacer(1, 0.2*inch))
        
        # Key findings section
        content.append(Paragraph("Technical Analysis Details", heading_style))
        
        # Create a table for the technical findings
        findings_data = [
            [Paragraph("Finding", table_header_style), 
             Paragraph("Details", table_header_style)]
        ]
        
        # Row styles for the findings table
        findings_row_styles = []
        findings_row_styles.append(('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey))
        findings_row_styles.append(('TEXTCOLOR', (0, 0), (-1, 0), colors.black))
        findings_row_styles.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
        findings_row_styles.append(('ALIGN', (1, 0), (1, -1), 'LEFT'))
        findings_row_styles.append(('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
        findings_row_styles.append(('BOTTOMPADDING', (0, 0), (-1, 0), 12))
        findings_row_styles.append(('GRID', (0, 0), (-1, -1), 1, colors.black))
        findings_row_styles.append(('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
        
        # Keep track of row index
        row_idx = 1
        
        findings = []
        
        # Knee alignment
        if left_knee_avg > knee_threshold and right_knee_avg < -knee_threshold:
            findings.append(("Knee Alignment", "Possible knocked knees detected based on average measurements."))
        elif left_knee_avg < -knee_threshold and right_knee_avg > knee_threshold:
            findings.append(("Knee Alignment", "Possible bow legs detected based on average measurements."))
        else:
            findings.append(("Knee Alignment", "No significant leg alignment issues detected based on average measurements."))
        
        # Shoulder alignment
        if abs(shoulder_diff_avg) > shoulder_threshold:
            findings.append(("Shoulder Alignment", f"Possible shoulder imbalance detected (Average difference: {shoulder_diff_avg:.2f})."))
        else:
            findings.append(("Shoulder Alignment", f"No significant shoulder imbalance detected (Average difference: {shoulder_diff_avg:.2f})."))
        
        # Hip alignment
        if abs(hip_diff_avg) > shoulder_threshold:
            findings.append(("Hip Alignment", f"Possible hip height imbalance detected (Average difference: {hip_diff_avg:.2f})."))
        else:
            findings.append(("Hip Alignment", f"No significant hip height imbalance detected (Average difference: {hip_diff_avg:.2f})."))
        
        # Overall posture
        if abs(vertical_avg) > 0.1:
            findings.append(("Vertical Alignment", f"Possible forward/backward lean detected (Average deviation: {vertical_avg:.2f})."))
        else:
            findings.append(("Vertical Alignment", f"Good average vertical alignment (Average deviation: {vertical_avg:.2f})."))
        
        # Add findings to table
        for category, detail in findings:
            # Color code the row based on content
            if any(negative in detail.lower() for negative in ["issue", "abnormal", "imbalance", "deviat", "concern", "possible", "detected"]):
                if not any(positive in detail.lower() for positive in ["no significant", "good"]):
                    # Highlight entire row for abnormal
                    findings_row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightcoral))
                    findings_row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.white))
            elif any(positive in detail.lower() for positive in ["normal", "no significant", "good"]):
                # Highlight entire row for normal
                findings_row_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.lightgreen))
                findings_row_styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.darkgreen))
            
            findings_data.append([category, detail])
            row_idx += 1
        
        # Create and style the table
        findings_table = Table(findings_data, colWidths=[1.5*inch, 5*inch])
        findings_table.setStyle(TableStyle(findings_row_styles))
        
        # Add the table to content
        content.append(findings_table)
        content.append(Spacer(1, 0.2*inch))
        
        # Frame-by-frame analysis
        content.append(Paragraph("Frame-by-Frame Analysis", heading_style))
        content.append(Paragraph(
            "The following section shows the analysis of each individual frame. Variations between frames "
            "may indicate changes in posture during movement or different viewing angles.", normal_style))
        
        # For each frame, add a summary
        for i, frame_data in enumerate(analysis_results):
            frame_number = frame_data.get("frame_number", i + 1)
            content.append(Paragraph(f"Frame {frame_number}", subheading_style))
            
            # Add visualization if available
            vis_path = frame_data.get("visualization_path")
            if vis_path and os.path.exists(vis_path):
                img_width = 3*inch
                content.append(Image(vis_path, width=img_width, height=img_width*0.75))
            
            # Add frame-specific measurements
            if "measurements" in frame_data:
                frame_measures = [
                    [Paragraph("Measurement", table_header_style), 
                     Paragraph("Value", table_header_style), 
                     Paragraph("Status", table_header_style)]
                ]
                
                # Row styles for each frame measurement table
                frame_row_styles = []
                frame_row_styles.append(('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey))
                frame_row_styles.append(('TEXTCOLOR', (0, 0), (-1, 0), colors.black))
                frame_row_styles.append(('ALIGN', (0, 0), (-1, -1), 'CENTER'))
                frame_row_styles.append(('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
                frame_row_styles.append(('BOTTOMPADDING', (0, 0), (-1, 0), 12))
                frame_row_styles.append(('GRID', (0, 0), (-1, -1), 1, colors.black))
                frame_row_styles.append(('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
                
                # Keep track of row index
                frame_row_idx = 1
                
                for name, data in frame_data["measurements"].items():
                    # Add color coding for status
                    if data['status'] == "Abnormal":
                        status_cell = Paragraph(data['status'], ParagraphStyle('Abnormal', parent=normal_style, textColor=colors.white, fontName='Helvetica-Bold'))
                        # Highlight entire row for abnormal
                        frame_row_styles.append(('BACKGROUND', (0, frame_row_idx), (-1, frame_row_idx), colors.lightcoral))
                        frame_row_styles.append(('TEXTCOLOR', (0, frame_row_idx), (-1, frame_row_idx), colors.white))
                    elif data['status'] == "Normal":
                        status_cell = Paragraph(data['status'], ParagraphStyle('Normal', parent=normal_style, textColor=colors.white, fontName='Helvetica-Bold'))
                        # Highlight entire row for normal
                        frame_row_styles.append(('BACKGROUND', (0, frame_row_idx), (-1, frame_row_idx), colors.lightgreen))
                        frame_row_styles.append(('TEXTCOLOR', (0, frame_row_idx), (-1, frame_row_idx), colors.darkgreen))
                    else:
                        status_cell = data['status']
                    
                    frame_measures.append([
                        name,
                        f"{data['value']:.4f}",
                        status_cell
                    ])
                    frame_row_idx += 1
                
                frame_table = Table(frame_measures, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
                frame_table.setStyle(TableStyle(frame_row_styles))
                
                content.append(frame_table)
            
            content.append(Spacer(1, 0.2*inch))
        
        # Disclaimer
        content.append(Paragraph("Disclaimer", heading_style))
        content.append(Paragraph(
            "This analysis is based on 2D video frames and has limitations. For a comprehensive assessment, "
            "please consult a healthcare professional. The measurements are for informational purposes only "
            "and should not replace professional medical advice. A video analysis provides more data points "
            "than a single image, but still has inherent limitations compared to in-person evaluation.",
            normal_style
        ))
        
        # Build and save the PDF
        doc.build(content)
        
        return {"status": "success", "pdf_path": report_path}
        
    except Exception as e:
        logger.exception(f"Error in create_aggregated_report: {str(e)}")
        return {"error": f"Failed to create aggregated report: {str(e)}"}

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Analyze posture from an image.')
    parser.add_argument('image_path', type=str, help='Path to the input image')
    parser.add_argument('--visualize', action='store_true', help='Generate visualization of the analysis')
    parser.add_argument('--confidence', type=float, default=0.7, help='Minimum detection confidence (0-1)')
    parser.add_argument('--no-pdf', action='store_true', help='Do not generate PDF report')
    
    args = parser.parse_args()
    
    # Run the analysis
    report = analyze_posture(args.image_path, args.visualize, args.confidence, not args.no_pdf)
    
    # Print the report path or text report
    print(report)

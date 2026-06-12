import easyocr
import cv2
import numpy as np
from PIL import Image
import logging
from typing import Tuple, Optional
import os

logger = logging.getLogger(__name__)

# Initialize reader (will download on first use)
_reader = None


def get_ocr_reader():
    """Get OCR reader instance (lazy loading)"""
    global _reader
    if _reader is None:
        try:
            _reader = easyocr.Reader(['en'], gpu=False)
            logger.info("OCR Reader initialized")
        except Exception as e:
            logger.error(f"Error initializing OCR reader: {e}")
            raise
    return _reader


class OCRService:
    """Handle OCR operations"""

    @staticmethod
    def extract_text_from_image(image_path: str) -> Tuple[str, float]:
        """
        Extract text from image using EasyOCR
        Returns: (extracted_text, confidence_score)
        """
        try:
            reader = get_ocr_reader()
            
            # Read image
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Read image using cv2
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Perform OCR
            results = reader.readtext(image, detail=1)
            
            # Extract text and calculate average confidence
            extracted_text = "\n".join([text[1] for text in results])
            confidences = [text[2] for text in results]
            
            # Calculate average confidence
            avg_confidence = (sum(confidences) / len(confidences)) if confidences else 0.0
            confidence_percentage = round(avg_confidence * 100, 2)
            
            logger.info(f"OCR completed for {image_path} with confidence {confidence_percentage}%")
            
            return extracted_text, confidence_percentage
        
        except Exception as e:
            logger.error(f"Error during OCR extraction: {e}")
            raise

    @staticmethod
    def preprocess_image(image_path: str) -> str:
        """Preprocess image for better OCR results"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return image_path
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 10, 21)
            
            # Apply adaptive thresholding
            processed = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Save processed image
            processed_path = image_path.replace('.', '_processed.')
            cv2.imwrite(processed_path, processed)
            
            logger.info(f"Image preprocessed: {processed_path}")
            return processed_path
        
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return image_path

    @staticmethod
    def validate_image(file_path: str) -> bool:
        """Validate if file is a valid image"""
        try:
            supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.pdf')
            if not file_path.lower().endswith(supported_formats):
                return False
            
            # Try to open and verify with PIL
            if file_path.lower().endswith('.pdf'):
                # For PDF, just check if file exists and has size
                return os.path.exists(file_path) and os.path.getsize(file_path) > 0
            
            # For images, try to open with PIL
            try:
                img = Image.open(file_path)
                # Try to load the image data
                img.load()
                return True
            except Exception as e:
                logger.error(f"PIL validation error: {e}")
                # If PIL fails, try cv2
                img_cv2 = cv2.imread(file_path)
                return img_cv2 is not None
                
        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            return False

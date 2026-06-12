import re
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class EntityExtractor:
    """Extract structured information from visiting card text"""

    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email from text"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_mobile(text: str) -> Optional[str]:
        """Extract mobile number from text"""
        # Supports various formats
        patterns = [
            r'\+91\s*\d{10}',  # +91 9876543210
            r'\+91\d{10}',     # +919876543210
            r'0\d{10}',        # 09876543210
            r'\d{10}',         # 9876543210
            r'\+\d{1,3}\s*\d{3,14}',  # International format
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None

    @staticmethod
    def extract_website(text: str) -> Optional[str]:
        """Extract website from text"""
        pattern = r'(?:www\.|http[s]?://)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_name_and_designation(text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract name and designation from text"""
        lines = text.strip().split('\n')
        name = None
        designation = None

        # First non-empty line is usually the name
        for line in lines:
            line = line.strip()
            if line and len(line) > 2:
                name = line
                break

        # Look for designation keywords
        designation_keywords = [
            'director', 'manager', 'engineer', 'developer', 'designer',
            'analyst', 'consultant', 'coordinator', 'executive', 'officer',
            'ceo', 'cto', 'cfo', 'coo', 'vp', 'president', 'lead',
            'associate', 'senior', 'junior', 'intern', 'specialist'
        ]

        for line in lines:
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in designation_keywords):
                designation = line.strip()
                break

        return name, designation

    @staticmethod
    def extract_company(text: str) -> Optional[str]:
        """Extract company name from text"""
        # Look for patterns like "Ltd", "Pvt", "Inc", "Corp"
        pattern = r'(?:[\w\s&-]+?)\s+(?:Ltd|Pvt|Inc|Corp|Company|Co\.|LLC|LLP)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(0) if match else None

    @staticmethod
    def extract_address(text: str) -> Optional[str]:
        """Extract address from text"""
        # Look for lines after "Address:" keyword or last few lines
        lines = text.split('\n')
        address_lines = []

        for i, line in enumerate(lines):
            if 'address' in line.lower():
                # Get next 2-3 lines as address
                for j in range(i + 1, min(i + 3, len(lines))):
                    if lines[j].strip():
                        address_lines.append(lines[j].strip())
                break

        if not address_lines:
            # Use last 2 lines if they don't contain other info
            for line in lines[-2:]:
                if (line.strip() and 
                    '@' not in line and 
                    not re.search(r'\+\d{1,3}', line)):
                    address_lines.append(line.strip())

        return ' '.join(address_lines) if address_lines else None

    @classmethod
    def extract_all(cls, text: str) -> Dict:
        """Extract all information from visiting card text"""
        try:
            name, designation = cls.extract_name_and_designation(text)
            
            extracted = {
                'name': name or 'Unknown',
                'designation': cls.extract_designation(text, designation),
                'company_name': cls.extract_company(text),
                'mobile': cls.extract_mobile(text),
                'email': cls.extract_email(text),
                'website': cls.extract_website(text),
                'address': cls.extract_address(text),
            }
            return extracted
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}

    @staticmethod
    def extract_designation(text: str, suggested: Optional[str] = None) -> Optional[str]:
        """Extract designation with suggestion"""
        if suggested:
            return suggested
        
        designation_patterns = [
            r'(?:Designation|Title|Position)[\s:]*([^\n]+)',
            r'(?:Sales|Service|Technical|Customer)\s+([A-Za-z\s]+)',
        ]
        
        for pattern in designation_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None

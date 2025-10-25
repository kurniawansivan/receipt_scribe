import base64
import logging
import json
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def encode_image_to_base64(self, image_bytes: bytes) -> str:
        """Encode image bytes to base64 string"""
        return base64.b64encode(image_bytes).decode('utf-8')
    
    async def extract_expense_data(self, image_bytes: bytes) -> dict:
        """Extract expense data from receipt image using GPT-4o"""
        try:
            base64_image = self.encode_image_to_base64(image_bytes)
            
            # Improved prompt for better accuracy
            prompt = """
            Analyze this receipt image and extract financial information accurately.
            
            IMPORTANT: Return ONLY valid JSON with this exact structure:
            {
                "vendor_name": "string or null",
                "date": "YYYY-MM-DD or null", 
                "total_amount": number or null,
                "tax_amount": number or null,
                "items": [{"description": "string", "amount": number}]
            }
            
            Guidelines:
            - vendor_name: The store/restaurant/business name
            - date: Transaction date in YYYY-MM-DD format
            - total_amount: Final total amount paid
            - tax_amount: Tax amount if itemized, otherwise 0 or null
            - items: List of purchased items with descriptions and individual amounts
            
            If you cannot determine a value, use null.
            Be precise with numbers and dates.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Updated to current vision model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                response_format={ "type": "json_object" }  # Force JSON response
            )
            
            # Extract and clean the JSON response
            content = response.choices[0].message.content
            logger.info(f"Raw OpenAI response: {content}")
            
            # Parse and validate the response
            extracted_data = json.loads(content)
            
            # Ensure all required fields are present
            required_fields = ["vendor_name", "date", "total_amount", "tax_amount", "items"]
            for field in required_fields:
                if field not in extracted_data:
                    extracted_data[field] = None if field != "items" else []
            
            # Validate items structure
            if extracted_data["items"]:
                for item in extracted_data["items"]:
                    if "description" not in item:
                        item["description"] = "Unknown"
                    if "amount" not in item:
                        item["amount"] = 0.0
            
            logger.info(f"Successfully extracted data from receipt: {extracted_data}")
            return extracted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            logger.error(f"Raw response that failed: {content}")
            raise Exception("Failed to parse receipt data. Please try again with a clearer image.")
        except Exception as e:
            logger.error(f"Error extracting data from image: {str(e)}")
            raise Exception(f"Failed to process image: {str(e)}")

# Simple global instance
openai_service = OpenAIService()
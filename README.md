# 📧 ReceiptScribe

**ReceiptScribe** is an AI-powered expense management application that automatically extracts and organizes data from receipt images using OpenAI's GPT-4 Vision API. Simply snap a photo of your receipt, and let AI handle the data entry!

![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## 🌟 Features

- 📸 **Smart Receipt Scanning** - Capture receipts with your camera or upload from gallery
- 🤖 **AI-Powered Data Extraction** - Automatically extract vendor, date, amounts, and itemized lists
- 📊 **Expense Dashboard** - View expense summaries and recent transactions
- 🔍 **Detailed Expense View** - Tap any expense to see complete breakdown
- 💾 **Local Storage** - All data stored securely in local SQLite database
- 📱 **Cross-Platform** - Built with Flutter for iOS, Android, and Web

## 🏗️ Architecture

```
ReceiptScribe/
├── receipt_scribe_backend/     # FastAPI Python Backend
│   ├── app/
│   │   ├── api/endpoints/      # REST API endpoints
│   │   ├── core/              # Configuration & security
│   │   ├── models/            # Data schemas
│   │   └── services/          # Business logic
│   └── requirements.txt
└── receipt_scribe_frontend/    # Flutter Frontend
    ├── lib/
    │   ├── models/            # Data models
    │   ├── providers/         # State management
    │   ├── screens/           # UI screens
    │   └── services/          # API services
    └── pubspec.yaml
```

## 🚀 Quick Start

### Prerequisites

**Backend:**
- Python 3.8+
- OpenAI API Key

**Frontend:**
- Flutter SDK 3.0+
- Dart SDK

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd receipt_scribe/receipt_scribe_backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./expenses.db
   MAX_FILE_SIZE_MB=10
   ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,bmp,tiff,webp
   ```

5. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ../receipt_scribe_frontend
   ```

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Run the app:**
   ```bash
   flutter run
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 📋 Get All Expenses
```http
GET /api/expenses/
```

**Response:**
```json
{
  "total_expenses": 290.98,
  "expense_count": 5,
  "recent_expenses": [
    {
      "id": 1,
      "vendor_name": "Test Store",
      "date": "2024-01-15",
      "total_amount": 25.99,
      "tax_amount": 2.99,
      "items": [
        {
          "description": "Test Item 1",
          "amount": 15.99
        }
      ]
    }
  ]
}
```

#### 📤 Upload Receipt
```http
POST /api/expenses/upload
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (required): Receipt image file

**Response:**
```json
{
  "message": "Receipt processed successfully",
  "expense_id": 1,
  "vendor_name": "Store Name",
  "total_amount": 25.99
}
```

#### 🔍 Health Check
```http
GET /api/expenses/health
```

## 🧠 AI Processing

ReceiptScribe uses **OpenAI GPT-4 Vision** to extract structured data from receipt images:

### Extracted Data:
- **Vendor Information** - Store name and location
- **Transaction Details** - Date, total amount, tax
- **Itemized List** - Individual items with descriptions and prices
- **Receipt Metadata** - Receipt number, payment method

### Supported Image Formats:
- JPG, JPEG, PNG, GIF, BMP, TIFF, WebP
- Maximum file size: 10MB
- Automatic image validation and processing

## 📱 Frontend Features

### 🏠 Dashboard Screen
- Expense summary cards
- Recent expenses list
- Quick upload button
- Tap any expense for details

### 📊 Expense Detail Screen
- Complete expense breakdown
- Vendor information
- Itemized purchase list
- Tax calculations
- Receipt metadata

### 📸 Upload Screen
- Camera capture
- Gallery selection
- Image preview
- Upload progress

## 🛠️ Development

### Backend Dependencies
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
openai==1.6.1
python-dotenv==1.0.0
pillow==10.1.0
```

### Frontend Dependencies
```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  http: ^1.1.0
  provider: ^6.1.1
  image_picker: ^1.0.4
  mime: ^1.0.4
```

### Project Structure

**Backend (`receipt_scribe_backend/`):**
```
app/
├── api/
│   └── endpoints/
│       └── expenses.py         # API endpoints
├── core/
│   ├── config.py              # Configuration
│   └── security.py            # Security settings
├── models/
│   └── schemas.py             # Pydantic models
├── services/
│   ├── database_service.py    # Database operations
│   └── openai_service.py      # AI processing
└── main.py                    # FastAPI app
```

**Frontend (`receipt_scribe_frontend/`):**
```
lib/
├── models/
│   ├── api_response.dart      # API response models
│   └── expense.dart           # Expense model
├── providers/
│   └── expense_provider.dart  # State management
├── screens/
│   ├── dashboard_screen.dart  # Main dashboard
│   ├── expense_detail_screen.dart  # Expense details
│   └── upload_screen.dart     # Receipt upload
├── services/
│   └── api_service.dart       # API communication
└── main.dart                  # App entry point
```

## 🔧 Configuration

### Backend Configuration (`.env`)
```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./expenses.db

# File Upload Configuration
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,bmp,tiff,webp

# CORS Configuration
CORS_ORIGINS=["http://localhost:*", "http://127.0.0.1:*"]
```

### Frontend Configuration
The frontend automatically connects to `http://localhost:8000` for API calls. Update the base URL in `lib/services/api_service.dart` if needed.

## 🧪 Testing

### Backend Testing
```bash
cd receipt_scribe_backend
python test_setup.py
```

### Frontend Testing
```bash
cd receipt_scribe_frontend
flutter test
```

## 📊 Database Schema

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_name TEXT,
    date TEXT,
    total_amount REAL,
    tax_amount REAL,
    items_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚨 Error Handling

The application includes comprehensive error handling:

- **File Upload Validation** - Size and format checks
- **AI Processing Errors** - Graceful fallbacks for unclear images
- **Network Error Handling** - Retry mechanisms and user feedback
- **Database Error Recovery** - Transaction rollbacks and data integrity

## 🔒 Security Features

- File type validation
- File size limits
- CORS configuration
- SQL injection prevention
- Input sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for the powerful GPT-4 Vision API
- **Flutter Team** for the excellent cross-platform framework
- **FastAPI** for the modern, fast web framework

## 📞 Support

If you have any questions or need help:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Include logs and error messages

---

**Made with ❤️ and AI-powered automation**

*Transform your receipts into organized expense data with just a photo!*
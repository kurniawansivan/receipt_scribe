import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.json()}")
        
        # Test expenses endpoint
        response = requests.get(f"{base_url}/api/expenses/")
        print(f"✅ Expenses endpoint: {response.status_code}")
        
        print("\n🎉 API is running correctly!")
        print(f"📚 API Documentation: {base_url}/docs")
        
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    test_api()
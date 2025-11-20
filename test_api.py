"""
Test script for Brain Tumor Segmentation API
Tests all endpoints and provides detailed feedback
"""

import requests
import json
from pathlib import Path
import time

API_URL = "http://localhost:8000"

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_root():
    """Test root endpoint"""
    print_header("Testing Root Endpoint (GET /)")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test health check endpoint"""
    print_header("Testing Health Check (GET /health)")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print_header("Testing Model Info (GET /model-info)")
    try:
        response = requests.get(f"{API_URL}/model-info")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction():
    """Test prediction endpoint"""
    print_header("Testing Prediction (POST /predict)")
    
    # Find test images
    test_images_dir = Path("Test_images")
    if not test_images_dir.exists():
        print("❌ Test_images directory not found!")
        return False
    
    test_images = list(test_images_dir.glob("*.png"))
    if not test_images:
        print("❌ No test images found!")
        return False
    
    test_image = test_images[0]
    print(f"Using test image: {test_image.name}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (test_image.name, f, 'image/png')}
            response = requests.post(f"{API_URL}/predict", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Prediction successful!")
            print(f"  • Tumor Pixels: {result['tumor_pixels']}")
            print(f"  • Total Pixels: {result['total_pixels']}")
            print(f"  • Tumor Percentage: {result['tumor_percentage']}%")
            print(f"  • Original Size: {result['original_size']}")
            print(f"  • Model Size: {result['model_size']}")
            print(f"  • Segmented Image: {len(result['segmented_image'])} bytes (base64)")
            print(f"  • Mask: {len(result['mask'])} bytes (base64)")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print_header("Testing Batch Prediction (POST /batch-predict)")
    
    # Find test images
    test_images_dir = Path("Test_images")
    if not test_images_dir.exists():
        print("❌ Test_images directory not found!")
        return False
    
    test_images = list(test_images_dir.glob("*.png"))[:3]  # Use first 3 images
    if not test_images:
        print("❌ No test images found!")
        return False
    
    print(f"Using {len(test_images)} test images")
    
    try:
        files = []
        for img_path in test_images:
            files.append(('files', (img_path.name, open(img_path, 'rb'), 'image/png')))
        
        response = requests.post(f"{API_URL}/batch-predict", files=files)
        
        # Close file handles
        for _, (_, file_handle, _) in files:
            file_handle.close()
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Batch prediction successful!")
            print(f"  • Total Images: {result['total_images']}")
            print(f"  • Successful: {result['successful']}")
            print(f"  • Failed: {result['failed']}")
            print("\n  Results:")
            for r in result['results']:
                if r['success']:
                    print(f"    - {r['filename']}: {r['tumor_percentage']}% tumor")
                else:
                    print(f"    - {r['filename']}: FAILED - {r['error']}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  Brain Tumor Segmentation API - Test Suite")
    print("=" * 60)
    
    print(f"\n📍 Testing API at: {API_URL}")
    print("⏳ Checking if server is running...")
    
    try:
        requests.get(API_URL, timeout=2)
        print("✅ Server is running!\n")
    except:
        print("\n❌ Cannot connect to API!")
        print("   Please ensure the backend is running:")
        print("   python backend.py")
        print("\n   Or use the startup script:")
        print("   .\\start_backend.ps1")
        return
    
    # Run tests
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Model Info", test_model_info),
        ("Single Prediction", test_prediction),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    for test_name, test_func in tests:
        time.sleep(0.5)  # Small delay between tests
        success = test_func()
        results.append((test_name, success))
    
    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\n{'=' * 60}")
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()

"""
Demo script showing how to use the Brain Tumor Segmentation API
"""

import requests
import base64
from pathlib import Path
from PIL import Image
import io

API_URL = "http://localhost:8000"

def save_base64_image(base64_string, output_path):
    """Save a base64 encoded image to file"""
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))
    img.save(output_path)
    print(f"✅ Saved image to: {output_path}")

def example_1_single_prediction():
    """Example 1: Single image prediction"""
    print("\n" + "="*60)
    print("Example 1: Single Image Prediction")
    print("="*60)
    
    # Use first test image
    test_image = Path("Test_images/raw_mri_1.png")
    
    if not test_image.exists():
        print("❌ Test image not found!")
        return
    
    print(f"📤 Uploading: {test_image.name}")
    
    # Send request
    with open(test_image, 'rb') as f:
        files = {'file': (test_image.name, f, 'image/png')}
        response = requests.post(f"{API_URL}/predict", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Prediction successful!")
        print(f"   Tumor pixels: {result['tumor_pixels']}")
        print(f"   Total pixels: {result['total_pixels']}")
        print(f"   Tumor percentage: {result['tumor_percentage']}%")
        
        # Save segmented image
        output_path = "demo_output_segmented.png"
        save_base64_image(result['segmented_image'], output_path)
        
        # Save mask
        mask_path = "demo_output_mask.png"
        save_base64_image(result['mask'], mask_path)
        
    else:
        print(f"❌ Error: {response.json()}")

def example_2_batch_prediction():
    """Example 2: Batch prediction"""
    print("\n" + "="*60)
    print("Example 2: Batch Prediction")
    print("="*60)
    
    # Get all test images
    test_images_dir = Path("Test_images")
    test_images = list(test_images_dir.glob("*.png"))[:3]  # First 3 images
    
    if not test_images:
        print("❌ No test images found!")
        return
    
    print(f"📤 Uploading {len(test_images)} images...")
    
    # Prepare files
    files = []
    for img_path in test_images:
        files.append(('files', (img_path.name, open(img_path, 'rb'), 'image/png')))
    
    # Send request
    response = requests.post(f"{API_URL}/batch-predict", files=files)
    
    # Close file handles
    for _, (_, file_handle, _) in files:
        file_handle.close()
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Batch prediction completed!")
        print(f"   Total images: {result['total_images']}")
        print(f"   Successful: {result['successful']}")
        print(f"   Failed: {result['failed']}")
        
        print("\n📊 Results:")
        for r in result['results']:
            if r['success']:
                print(f"   • {r['filename']}: {r['tumor_percentage']}% tumor")
            else:
                print(f"   • {r['filename']}: FAILED")
    else:
        print(f"❌ Error: {response.json()}")

def example_3_custom_image():
    """Example 3: Using a custom image"""
    print("\n" + "="*60)
    print("Example 3: Custom Image Upload")
    print("="*60)
    
    print("\n💡 To test with your own image:")
    print("   1. Place your MRI image in the project folder")
    print("   2. Update the image path in this function")
    print("   3. Run this script again")
    
    # Example code (commented out - replace with your image path)
    """
    custom_image_path = "my_mri_image.png"
    
    with open(custom_image_path, 'rb') as f:
        files = {'file': ('my_image.png', f, 'image/png')}
        response = requests.post(f"{API_URL}/predict", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Tumor detected: {result['tumor_percentage']}%")
        save_base64_image(result['segmented_image'], "my_result.png")
    """

def example_4_get_model_info():
    """Example 4: Get model information"""
    print("\n" + "="*60)
    print("Example 4: Model Information")
    print("="*60)
    
    response = requests.get(f"{API_URL}/model-info")
    
    if response.status_code == 200:
        info = response.json()
        print("\n📊 Model Details:")
        print(f"   Name: {info['model_name']}")
        print(f"   Input shape: {info['input_shape']}")
        print(f"   Output shape: {info['output_shape']}")
        print(f"   Total parameters: {info['total_params']:,}")
        print(f"   Architecture: {info['architecture']}")
    else:
        print(f"❌ Error: {response.json()}")

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            health = response.json()
            if health.get('model_loaded'):
                return True
            else:
                print("⚠️  Server is running but model is not loaded!")
                return False
        return False
    except:
        return False

def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("  Brain Tumor Segmentation API - Demo Examples")
    print("="*60)
    
    print(f"\n📍 API URL: {API_URL}")
    
    # Check if server is running
    print("🔍 Checking server status...")
    if not check_server():
        print("\n❌ Cannot connect to API server!")
        print("\n📝 To start the server:")
        print("   Option 1: .\\start_backend.ps1")
        print("   Option 2: python backend.py")
        print("\n   Then run this demo script again.")
        return
    
    print("✅ Server is running and model is loaded!")
    
    # Create output directory
    output_dir = Path("demo_outputs")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Outputs will be saved to: {output_dir}/")
    
    # Run examples
    try:
        example_1_single_prediction()
        example_2_batch_prediction()
        example_3_custom_image()
        example_4_get_model_info()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        print("\n📁 Check the following files:")
        print("   • demo_output_segmented.png - Segmentation overlay")
        print("   • demo_output_mask.png - Binary tumor mask")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()

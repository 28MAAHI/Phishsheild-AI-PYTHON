#!/usr/bin/env python3
"""
Test script to verify the deployment setup locally before pushing to Vercel.
Run this to catch issues early.
"""

import sys
import os
import importlib.util

def test_imports():
    """Check if all required packages can be imported."""
    print("✓ Testing imports...")
    required = [
        'flask',
        'sklearn',
        'pandas',
        'numpy',
        'joblib',
        'tldextract',
        'requests',
    ]

    optional = [
        'langdetect',
        'urlextract',
        'dotenv',
    ]

    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace('sklearn', 'sklearn.preprocessing'))
            print(f"  ✓ {pkg}")
        except ImportError as e:
            print(f"  ✗ {pkg}: {e}")
            missing.append(pkg)

    if missing:
        print(f"\n✗ Missing required packages: {', '.join(missing)}")
        print("  Run: pip install -r requirements.txt")
        return False

    print("\n✓ Optional packages:")
    for pkg in optional:
        try:
            __import__(pkg)
            print(f"  ✓ {pkg} (available)")
        except ImportError:
            print(f"  ℹ {pkg} (not installed, feature will degrade gracefully)")

    return True


def test_structure():
    """Check if project structure is correct."""
    print("\n✓ Testing project structure...")

    required_files = [
        'app.py',
        'requirements.txt',
        'vercel.json',
        'runtime.txt',
        'api/index.py',
        'templates/index.html',
    ]

    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}")
            missing.append(file)

    if missing:
        print(f"\n✗ Missing files: {', '.join(missing)}")
        return False

    return True


def test_app_imports():
    """Test if the app can be imported."""
    print("\n✓ Testing app imports...")
    try:
        from app import app
        print(f"  ✓ Flask app imported successfully")
        print(f"  ✓ App name: {app.name}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import app: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_handler():
    """Test if the API handler works."""
    print("\n✓ Testing API handler...")
    try:
        from api.index import app
        print(f"  ✓ API handler imports app correctly")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import API handler: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration loading."""
    print("\n✓ Testing configuration...")
    try:
        from phishshield.config import Settings
        settings = Settings.from_env()
        print(f"  ✓ Configuration loaded")
        print(f"    - Debug mode: {settings.debug}")
        print(f"    - Zero-shot enabled: {settings.enable_zero_shot}")
        print(f"    - Translation enabled: {settings.enable_translation}")
        print(f"    - Max message chars: {settings.max_message_chars}")
        return True
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_models():
    """Test if ML models can be loaded."""
    print("\n✓ Testing ML models...")

    from phishshield.config import Settings
    settings = Settings.from_env()

    # Check spam model
    if os.path.exists(settings.spam_model_path):
        print(f"  ✓ Spam model found: {settings.spam_model_path}")
    else:
        print(f"  ℹ Spam model not found: {settings.spam_model_path}")
        print(f"    (This is OK for Vercel deployment if downloaded at runtime)")

    # Check URL model
    if os.path.exists(settings.url_model_path):
        print(f"  ✓ URL model found: {settings.url_model_path}")
    else:
        print(f"  ℹ URL model not found: {settings.url_model_path}")
        print(f"    (This is OK for Vercel deployment if downloaded at runtime)")

    return True


def test_vercel_json():
    """Check vercel.json configuration."""
    print("\n✓ Testing vercel.json...")

    import json
    try:
        with open('vercel.json', 'r') as f:
            config = json.load(f)

        print(f"  ✓ vercel.json is valid JSON")

        required_keys = ['buildCommand', 'framework', 'rewrites']
        for key in required_keys:
            if key in config:
                print(f"  ✓ {key}: present")
            else:
                print(f"  ✗ {key}: missing")
                return False

        # Check environment variables
        if 'env' in config:
            print(f"  ✓ Environment variables configured:")
            for k, v in config['env'].items():
                print(f"    - {k}: {v}")

        return True
    except json.JSONDecodeError as e:
        print(f"  ✗ vercel.json is invalid: {e}")
        return False
    except FileNotFoundError:
        print(f"  ✗ vercel.json not found")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("PhishShield Deployment Test")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Project Structure", test_structure),
        ("App Configuration", test_config),
        ("Vercel Configuration", test_vercel_json),
        ("App Imports", test_app_imports),
        ("API Handler", test_api_handler),
        ("ML Models", test_models),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Unexpected error in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed! Ready for Vercel deployment.")
        print("\nNext steps:")
        print("1. Commit your changes: git add . && git commit -m 'Add Vercel config'")
        print("2. Push to GitHub: git push origin main")
        print("3. Deploy: vercel --prod")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Fix issues above before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

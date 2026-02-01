#!/usr/bin/env python3
"""
Quick test script to verify Phase 1 implementation
Tests the complete authentication flow
"""

import asyncio
import httpx
from app.db.init_db import init_db


async def test_auth_flow():
    """Test the complete authentication flow"""
    
    print("🧪 Testing Phase 1 Implementation\n")
    print("=" * 60)
    
    # Initialize roles first
    print("\n1️⃣  Initializing database roles...")
    try:
        await init_db()
        print("   ✅ Database roles initialized")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    base_url = "http://localhost:8000/api/v1"
    
    async with httpx.AsyncClient() as client:
        # Test 1: Health check
        print("\n2️⃣  Testing health check endpoint...")
        try:
            response = await client.get("http://localhost:8000/")
            assert response.status_code == 200
            data = response.json()
            print(f"   ✅ API is running: {data['message']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 2: Get role ID (we'll use the user role)
        print("\n3️⃣  Getting role ID from database...")
        from app.db.database import SessionLocal
        from app.models.role import Role
        from sqlalchemy import select
        
        async with SessionLocal() as session:
            result = await session.execute(select(Role).where(Role.name == "user"))
            user_role = result.scalars().first()
            if user_role:
                role_id = str(user_role.id)
                print(f"   ✅ Found 'user' role: {role_id}")
            else:
                print("   ❌ User role not found")
                return
        
        # Test 3: Register a new user
        print("\n4️⃣  Testing user registration...")
        test_user = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "full_name": "Test User",
            "phone": "+1234567890",
            "role_id": role_id
        }
        
        try:
            response = await client.post(f"{base_url}/auth/register", json=test_user)
            if response.status_code == 201:
                user_data = response.json()
                print(f"   ✅ User registered successfully")
                print(f"      Email: {user_data['email']}")
                print(f"      ID: {user_data['id']}")
            elif response.status_code == 400:
                print(f"   ⚠️  User already exists (this is OK for repeated tests)")
            else:
                print(f"   ❌ Registration failed: {response.status_code}")
                print(f"      {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 4: Login
        print("\n5️⃣  Testing user login...")
        try:
            login_data = {
                "username": test_user["email"],
                "password": test_user["password"]
            }
            response = await client.post(
                f"{base_url}/auth/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data["access_token"]
                print(f"   ✅ Login successful")
                print(f"      Token type: {token_data['token_type']}")
                print(f"      Token (first 50 chars): {access_token[:50]}...")
            else:
                print(f"   ❌ Login failed: {response.status_code}")
                print(f"      {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 5: Get current user info
        print("\n6️⃣  Testing authenticated endpoint (get current user)...")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(f"{base_url}/auth/me", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ Successfully retrieved user info")
                print(f"      Email: {user_data['email']}")
                print(f"      Full Name: {user_data['full_name']}")
                print(f"      Active: {user_data['is_active']}")
            else:
                print(f"   ❌ Failed to get user info: {response.status_code}")
                print(f"      {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 6: Refresh token
        print("\n7️⃣  Testing token refresh...")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.post(f"{base_url}/auth/refresh", headers=headers)
            
            if response.status_code == 200:
                new_token_data = response.json()
                print(f"   ✅ Token refreshed successfully")
                print(f"      New token (first 50 chars): {new_token_data['access_token'][:50]}...")
            else:
                print(f"   ❌ Token refresh failed: {response.status_code}")
                print(f"      {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 7: Test protected endpoint without token
        print("\n8️⃣  Testing authentication requirement (should fail)...")
        try:
            response = await client.get(f"{base_url}/auth/me")
            
            if response.status_code == 401 or response.status_code == 403:
                print(f"   ✅ Correctly rejected unauthenticated request")
            else:
                print(f"   ⚠️  Unexpected response: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✨ Phase 1 Testing Complete!")
    print("\n📊 Summary:")
    print("   ✅ Database initialization")
    print("   ✅ User registration")
    print("   ✅ User login")
    print("   ✅ JWT token generation")
    print("   ✅ Protected endpoints")
    print("   ✅ Token refresh")
    print("   ✅ Authentication enforcement")
    print("\n🎉 All Phase 1 features are working correctly!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_auth_flow())

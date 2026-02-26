#!/bin/bash

echo "🧪 Testing AI Integration - Code Submission Flow"
echo "================================================="
echo ""

# Login
echo "🔑 Logging in as student1..."
TOKEN=$(curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student1@example.com","password":"password123"}' \
  -s | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed"
  exit 1
fi

echo "✅ Logged in successfully"
echo ""

# Get user ID
USER_ID=$(curl -s http://localhost:3000/api/auth/me -H "Authorization: Bearer $TOKEN" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "👤 User ID: $USER_ID"
echo ""

# Get Two Sum problem ID
echo "📝 Getting problem list..."
PROBLEMS=$(curl -s http://localhost:3000/api/problems -H "Authorization: Bearer $TOKEN")
TWO_SUM_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*","title":"Two Sum"' | cut -d'"' -f4)

if [ -z "$TWO_SUM_ID" ]; then
  echo "❌ Could not find Two Sum problem"
  exit 1
fi

echo "✅ Found Two Sum problem: $TWO_SUM_ID"
echo ""

# Check skills before submission
echo "📊 Checking skills BEFORE submission..."
curl -s -X POST "http://localhost:8000/profile/$USER_ID" \
  -H "X-Service-Key: dev-secret-key" | python -m json.tool
echo ""

# Submit correct solution
echo "💻 Submitting correct solution for Two Sum..."
SOLUTION='def solution(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []'

SUBMIT_RESPONSE=$(curl -X POST http://localhost:3000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$TWO_SUM_ID\",\"code\":\"$SOLUTION\",\"language\":\"python\"}" \
  -s)

SUBMISSION_ID=$(echo "$SUBMIT_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$SUBMISSION_ID" ]; then
  echo "❌ Submission failed"
  echo "$SUBMIT_RESPONSE"
  exit 1
fi

echo "✅ Submission created: $SUBMISSION_ID"
echo ""

# Wait for execution
echo "⏳ Waiting 10 seconds for code execution..."
sleep 10
echo ""

# Check submission status
echo "📋 Checking submission status..."
RESULT=$(curl -s "http://localhost:3000/api/submissions/$SUBMISSION_ID" -H "Authorization: Bearer $TOKEN")
STATUS=$(echo "$RESULT" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
RUNTIME=$(echo "$RESULT" | grep -o '"runtime":[0-9]*' | cut -d':' -f2)

echo "   Status: $STATUS"
echo "   Runtime: ${RUNTIME}ms"
echo ""

if [ "$STATUS" != "ACCEPTED" ]; then
  echo "❌ Expected ACCEPTED but got $STATUS"
  echo "$RESULT" | python -m json.tool
  exit 1
fi

echo "✅ Code ACCEPTED!"
echo ""

# Wait a bit for skill update
echo "⏳ Waiting 3 seconds for AI service to update skills..."
sleep 3
echo ""

# Check skills after submission
echo "📊 Checking skills AFTER submission..."
curl -s -X POST "http://localhost:8000/profile/$USER_ID" \
  -H "X-Service-Key: dev-secret-key" | python -m json.tool
echo ""

echo "================================================="
echo "✅ AI Integration Test Complete!"
echo ""

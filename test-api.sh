#!/bin/bash

echo "🧪 Testing Adaptive Learning Platform API"
echo "=========================================="
echo ""

BASE_URL="http://localhost:3000/api"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${BLUE}[TEST 1]${NC} Health Check"
echo "GET $BASE_URL/..."
curl -s $BASE_URL 2>&1 | head -3
echo ""
echo ""

# Test 2: Register New User
echo -e "${BLUE}[TEST 2]${NC} Register New User"
echo "POST $BASE_URL/auth/register"
REGISTER_RESPONSE=$(curl -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"testuser@example.com",
    "password":"password123",
    "name":"Test User"
  }' -s 2>&1)

if echo "$REGISTER_RESPONSE" | grep -q "token"; then
    echo -e "${GREEN}✓ Registration successful${NC}"
else
    echo -e "${RED}✗ Registration failed or user already exists${NC}"
fi
echo "$REGISTER_RESPONSE" | python -m json.tool 2>/dev/null | head -10
echo ""
echo ""

# Test 3: Login
echo -e "${BLUE}[TEST 3]${NC} User Login"
echo "POST $BASE_URL/auth/login"
LOGIN_RESPONSE=$(curl -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"student1@example.com",
    "password":"password123"
  }' -s)

TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ ! -z "$TOKEN" ]; then
    echo -e "${GREEN}✓ Login successful${NC}"
    echo "Token: ${TOKEN:0:50}..."
else
    echo -e "${RED}✗ Login failed${NC}"
    echo "$LOGIN_RESPONSE" | python -m json.tool 2>/dev/null
fi
echo ""
echo ""

# Test 4: Get Current User
echo -e "${BLUE}[TEST 4]${NC} Get Current User"
echo "GET $BASE_URL/auth/me"
curl -s $BASE_URL/auth/me \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool 2>/dev/null | head -10
echo ""
echo ""

# Test 5: Get All Problems
echo -e "${BLUE}[TEST 5]${NC} Get All Problems"
echo "GET $BASE_URL/problems"
PROBLEMS=$(curl -s $BASE_URL/problems \
  -H "Authorization: Bearer $TOKEN")
PROBLEM_COUNT=$(echo "$PROBLEMS" | grep -o '"id"' | wc -l)
echo -e "${GREEN}Found $PROBLEM_COUNT problems${NC}"
echo "$PROBLEMS" | python -m json.tool 2>/dev/null | head -30
echo ""
echo ""

# Test 6: Get Specific Problem
echo -e "${BLUE}[TEST 6]${NC} Get Specific Problem"
PROBLEM_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "GET $BASE_URL/problems/$PROBLEM_ID"
curl -s "$BASE_URL/problems/$PROBLEM_ID" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool 2>/dev/null | head -40
echo ""
echo ""

# Test 7: Get All Courses
echo -e "${BLUE}[TEST 7]${NC} Get All Courses"
echo "GET $BASE_URL/courses"
COURSES=$(curl -s $BASE_URL/courses \
  -H "Authorization: Bearer $TOKEN")
COURSE_COUNT=$(echo "$COURSES" | grep -o '"id"' | wc -l)
echo -e "${GREEN}Found $COURSE_COUNT courses${NC}"
echo "$COURSES" | python -m json.tool 2>/dev/null | head -30
echo ""
echo ""

# Test 8: Get User Skills
echo -e "${BLUE}[TEST 8]${NC} Get User Skills"
echo "GET $BASE_URL/skills/me"
curl -s $BASE_URL/skills/me \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool 2>/dev/null | head -20
echo ""
echo ""

# Test 9: Get Recommendations
echo -e "${BLUE}[TEST 9]${NC} Get Problem Recommendations"
echo "GET $BASE_URL/recommendations"
curl -s $BASE_URL/recommendations \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool 2>/dev/null | head -20
echo ""
echo ""

# Test 10: AI Service Health
echo -e "${BLUE}[TEST 10]${NC} AI Service Health Check"
echo "GET http://localhost:8000/health"
AI_HEALTH=$(curl -s http://localhost:8000/health)
if echo "$AI_HEALTH" | grep -q "ok"; then
    echo -e "${GREEN}✓ AI Service is healthy${NC}"
else
    echo -e "${RED}✗ AI Service issue${NC}"
fi
echo "$AI_HEALTH"
echo ""
echo ""

echo "=========================================="
echo -e "${GREEN}✅ API Testing Complete!${NC}"
echo ""

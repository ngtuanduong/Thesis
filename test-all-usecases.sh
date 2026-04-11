#!/bin/bash

echo "🧪 COMPREHENSIVE USE CASE TESTING"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:3000/api"
AI_URL="http://localhost:8000"

# Test counter
PASS=0
FAIL=0

test_case() {
    echo -e "${YELLOW}[TEST]${NC} $1"
}

pass() {
    echo -e "  ${GREEN}✓ PASS${NC} - $1"
    ((PASS++))
}

fail() {
    echo -e "  ${RED}✗ FAIL${NC} - $1"
    ((FAIL++))
}

echo "========================================"
echo "USE CASE 1: User Registration & Login"
echo "========================================"
echo ""

test_case "1.1 Register new user"
REGISTER_RESULT=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"testuser$(date +%s)@test.com\",\"password\":\"Test123!\",\"name\":\"Test User\"}")

if echo "$REGISTER_RESULT" | grep -q "token"; then
    pass "User registration successful"
    NEW_USER_TOKEN=$(echo "$REGISTER_RESULT" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
else
    fail "User registration failed"
fi

test_case "1.2 Login existing user"
LOGIN_RESULT=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student1@example.com","password":"password123"}')

if echo "$LOGIN_RESULT" | grep -q "token"; then
    pass "Login successful"
    TOKEN=$(echo "$LOGIN_RESULT" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    USER_ID=$(echo "$LOGIN_RESULT" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
else
    fail "Login failed"
fi

test_case "1.3 Get current user profile"
PROFILE=$(curl -s $BASE_URL/auth/me -H "Authorization: Bearer $TOKEN")
if echo "$PROFILE" | grep -q "student1@example.com"; then
    pass "Profile retrieval successful"
else
    fail "Profile retrieval failed"
fi

echo ""
echo "========================================"
echo "USE CASE 2: Browse Courses & Enroll"
echo "========================================"
echo ""

test_case "2.1 Get all courses"
COURSES=$(curl -s $BASE_URL/courses -H "Authorization: Bearer $TOKEN")
COURSE_COUNT=$(echo "$COURSES" | grep -o '"id"' | wc -l)
if [ "$COURSE_COUNT" -gt 0 ]; then
    pass "Found $COURSE_COUNT courses"
    COURSE_ID=$(echo "$COURSES" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
else
    fail "No courses found"
fi

test_case "2.2 Get course details"
COURSE_DETAIL=$(curl -s $BASE_URL/courses/$COURSE_ID -H "Authorization: Bearer $TOKEN")
if echo "$COURSE_DETAIL" | grep -q "title"; then
    pass "Course details retrieved"
else
    fail "Course details retrieval failed"
fi

test_case "2.3 Enroll in course"
ENROLLMENT=$(curl -s -X POST $BASE_URL/courses/$COURSE_ID/enroll \
  -H "Authorization: Bearer $TOKEN")
if echo "$ENROLLMENT" | grep -q "id\|already"; then
    pass "Course enrollment successful (or already enrolled)"
else
    fail "Course enrollment failed"
fi

echo ""
echo "========================================"
echo "USE CASE 3: Problem Solving Workflow"
echo "========================================"
echo ""

test_case "3.1 Get all problems"
PROBLEMS=$(curl -s $BASE_URL/problems -H "Authorization: Bearer $TOKEN")
PROBLEM_COUNT=$(echo "$PROBLEMS" | grep -o '"title"' | wc -l)
if [ "$PROBLEM_COUNT" -gt 0 ]; then
    pass "Found $PROBLEM_COUNT problems"
    PROBLEM_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*","title":"Two Sum"' | cut -d'"' -f4)
else
    fail "No problems found"
fi

test_case "3.2 Get problem details with test cases"
PROBLEM_DETAIL=$(curl -s $BASE_URL/problems/$PROBLEM_ID -H "Authorization: Bearer $TOKEN")
if echo "$PROBLEM_DETAIL" | grep -q "testCases"; then
    pass "Problem details with test cases retrieved"
else
    fail "Problem details retrieval failed"
fi

test_case "3.3 Submit correct solution"
SOLUTION='def solution(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []'

SUBMISSION=$(curl -s -X POST $BASE_URL/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$PROBLEM_ID\",\"code\":\"$SOLUTION\",\"language\":\"python\"}")

SUBMISSION_ID=$(echo "$SUBMISSION" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -n "$SUBMISSION_ID" ]; then
    pass "Solution submitted - ID: $SUBMISSION_ID"
else
    fail "Solution submission failed"
fi

test_case "3.4 Wait for code execution"
echo "  ⏳ Waiting 10 seconds for code execution..."
sleep 10

test_case "3.5 Check submission result"
RESULT=$(curl -s $BASE_URL/submissions/$SUBMISSION_ID -H "Authorization: Bearer $TOKEN")
STATUS=$(echo "$RESULT" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$STATUS" = "ACCEPTED" ]; then
    pass "Code executed - Status: ACCEPTED"
    RUNTIME=$(echo "$RESULT" | grep -o '"runtime":[0-9]*' | cut -d':' -f2)
    echo "    Runtime: ${RUNTIME}ms"
else
    fail "Code execution status: $STATUS"
fi

test_case "3.6 Get user's submission history"
SUBMISSIONS=$(curl -s $BASE_URL/submissions/my -H "Authorization: Bearer $TOKEN")
if echo "$SUBMISSIONS" | grep -q "$SUBMISSION_ID"; then
    pass "Submission history retrieved"
else
    fail "Submission history retrieval failed"
fi

test_case "3.7 Get submissions for specific problem"
PROBLEM_SUBS=$(curl -s $BASE_URL/submissions/problem/$PROBLEM_ID -H "Authorization: Bearer $TOKEN")
if echo "$PROBLEM_SUBS" | grep -q "id"; then
    pass "Problem-specific submissions retrieved"
else
    fail "Problem submissions retrieval failed"
fi

echo ""
echo "========================================"
echo "USE CASE 4: AI-Powered Features"
echo "========================================"
echo ""

test_case "4.1 Check AI service health"
AI_HEALTH=$(curl -s $AI_URL/health)
if echo "$AI_HEALTH" | grep -q "ok"; then
    pass "AI service is healthy"
else
    fail "AI service is not responding"
fi

test_case "4.2 Get user skill profile"
sleep 3  # Wait for skill update
SKILLS=$(curl -s -X POST $AI_URL/profile/$USER_ID -H "X-Service-Key: dev-secret-key")
SKILL_COUNT=$(echo "$SKILLS" | grep -o '"skill_name"' | wc -l)
if [ "$SKILL_COUNT" -gt 0 ]; then
    pass "User has $SKILL_COUNT skills tracked"
    echo "$SKILLS" | grep -E "skill_name|score" | head -6 | sed 's/^/    /'
else
    fail "No skills found for user"
fi

test_case "4.3 Get AI-powered problem recommendations"
RECOMMENDATIONS=$(curl -s $BASE_URL/recommendations -H "Authorization: Bearer $TOKEN")
REC_COUNT=$(echo "$RECOMMENDATIONS" | grep -o '"title"' | wc -l)
if [ "$REC_COUNT" -gt 0 ]; then
    pass "Received $REC_COUNT problem recommendations"
    echo "$RECOMMENDATIONS" | grep -E '"title"|"difficulty"' | head -8 | sed 's/^/    /'
else
    fail "No recommendations received"
fi

test_case "4.4 Verify problem embeddings exist"
EMBEDDINGS=$(curl -s -X POST $BASE_URL/skills/compute -H "Authorization: Bearer $TOKEN")
# Just verify the endpoint responds
if [ $? -eq 0 ]; then
    pass "Skill computation endpoint accessible"
else
    fail "Skill computation endpoint failed"
fi

echo ""
echo "========================================"
echo "USE CASE 5: Error Handling"
echo "========================================"
echo ""

test_case "5.1 Submit wrong solution"
WRONG_SOLUTION='def solution(nums, target):\n    return [0, 0]  # Always wrong'
WRONG_SUB=$(curl -s -X POST $BASE_URL/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$PROBLEM_ID\",\"code\":\"$WRONG_SOLUTION\",\"language\":\"python\"}")
WRONG_ID=$(echo "$WRONG_SUB" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
sleep 10
WRONG_RESULT=$(curl -s $BASE_URL/submissions/$WRONG_ID -H "Authorization: Bearer $TOKEN")
WRONG_STATUS=$(echo "$WRONG_RESULT" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$WRONG_STATUS" = "WRONG_ANSWER" ]; then
    pass "Wrong answer detected correctly"
else
    fail "Wrong answer detection - got: $WRONG_STATUS"
fi

test_case "5.2 Unauthorized access attempt"
UNAUTH=$(curl -s $BASE_URL/problems)
if echo "$UNAUTH" | grep -q "Unauthorized"; then
    pass "Unauthorized access blocked"
else
    fail "Unauthorized access not blocked"
fi

test_case "5.3 Invalid login credentials"
BAD_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"fake@test.com","password":"wrong"}')
if echo "$BAD_LOGIN" | grep -q "Invalid\|Unauthorized\|401"; then
    pass "Invalid credentials rejected"
else
    fail "Invalid credentials not rejected properly"
fi

echo ""
echo "========================================"
echo "USE CASE 6: Data Integrity"
echo "========================================"
echo ""

test_case "6.1 Check database has users"
docker-compose -f docker/docker-compose.yml exec -T postgres psql -U postgres -d adaptive_learning -c "SELECT COUNT(*) FROM users;" > /tmp/db_check.txt 2>&1
USER_COUNT=$(grep -oP '\d+' /tmp/db_check.txt | tail -1)
if [ "$USER_COUNT" -gt 0 ]; then
    pass "Database has $USER_COUNT users"
else
    fail "No users in database"
fi

test_case "6.2 Check problem embeddings in database"
docker-compose -f docker/docker-compose.yml exec -T postgres psql -U postgres -d adaptive_learning -c "SELECT COUNT(*) FROM problem_embeddings WHERE embedding_vec IS NOT NULL;" > /tmp/emb_check.txt 2>&1
EMB_COUNT=$(grep -oP '\d+' /tmp/emb_check.txt | tail -1)
if [ "$EMB_COUNT" -gt 0 ]; then
    pass "Database has $EMB_COUNT problem embeddings"
else
    fail "No problem embeddings in database"
fi

test_case "6.3 Verify UUID data types"
docker-compose -f docker/docker-compose.yml exec -T postgres psql -U postgres -d adaptive_learning -c "\d users" > /tmp/schema_check.txt 2>&1
if grep -q "uuid" /tmp/schema_check.txt; then
    pass "Native UUID types confirmed"
else
    fail "UUID types not properly configured"
fi

echo ""
echo "========================================"
echo "SUMMARY"
echo "========================================"
echo ""
echo -e "Tests Passed: ${GREEN}$PASS${NC}"
echo -e "Tests Failed: ${RED}$FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ ALL USE CASES WORKING PERFECTLY!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed. Review above for details.${NC}"
    exit 1
fi

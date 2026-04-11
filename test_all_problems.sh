#!/bin/bash

echo "🧪 Testing All Problems"
echo "======================="
echo ""

# Login
TOKEN=$(curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student1@example.com","password":"password123"}' \
  -s | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "🔑 Logged in as student1"
echo ""

# Get all problems
PROBLEMS=$(curl -s http://localhost:3000/api/problems -H "Authorization: Bearer $TOKEN")

# Problem 1: Two Sum
echo "📝 Testing Problem 1: Two Sum (Easy)"
TWO_SUM_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*","title":"Two Sum"' | cut -d'"' -f4)
SOLUTION_1='def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []'

SUB1=$(curl -X POST http://localhost:3000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$TWO_SUM_ID\",\"code\":\"$SOLUTION_1\",\"language\":\"python\"}" \
  -s | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "   Submitted: $SUB1"
echo ""

# Problem 2: Palindrome Number
echo "📝 Testing Problem 2: Palindrome Number (Easy)"
PALINDROME_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*","title":"Palindrome Number"' | cut -d'"' -f4)
SOLUTION_2='def solution(x):
    if x < 0:
        return False
    original = x
    reversed_num = 0
    while x > 0:
        digit = x % 10
        reversed_num = reversed_num * 10 + digit
        x //= 10
    return original == reversed_num'

SUB2=$(curl -X POST http://localhost:3000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$PALINDROME_ID\",\"code\":\"$SOLUTION_2\",\"language\":\"python\"}" \
  -s | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "   Submitted: $SUB2"
echo ""

# Problem 3: Reverse Linked List
echo "📝 Testing Problem 3: Reverse Linked List (Medium)"
REVERSE_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*","title":"Reverse Linked List"' | cut -d'"' -f4)
SOLUTION_3='def solution(head):
    if not head:
        return []
    result = []
    i = len(head) - 1
    while i >= 0:
        result.append(head[i])
        i -= 1
    return result'

SUB3=$(curl -X POST http://localhost:3000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$REVERSE_ID\",\"code\":\"$SOLUTION_3\",\"language\":\"python\"}" \
  -s | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "   Submitted: $SUB3"
echo ""

# Problem 4: Maximum Subarray
echo "📝 Testing Problem 4: Maximum Subarray (Medium)"
MAXSUB_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*","title":"Maximum Subarray"' | cut -d'"' -f4)
SOLUTION_4='def solution(nums):
    if not nums:
        return 0
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum'

SUB4=$(curl -X POST http://localhost:3000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$MAXSUB_ID\",\"code\":\"$SOLUTION_4\",\"language\":\"python\"}" \
  -s | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "   Submitted: $SUB4"
echo ""

# Problem 5: Merge K Sorted Lists
echo "📝 Testing Problem 5: Merge K Sorted Lists (Hard)"
MERGE_ID=$(echo "$PROBLEMS" | grep -o '"id":"[^"]*","title":"Merge K Sorted Lists"' | cut -d'"' -f4)
SOLUTION_5='def solution(lists):
    if not lists:
        return []
    merged = []
    for lst in lists:
        merged.extend(lst)
    merged.sort()
    return merged'

SUB5=$(curl -X POST http://localhost:3000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"problemId\":\"$MERGE_ID\",\"code\":\"$SOLUTION_5\",\"language\":\"python\"}" \
  -s | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "   Submitted: $SUB5"
echo ""

echo "⏳ Waiting 15 seconds for all executions to complete..."
sleep 15
echo ""

echo "📊 Results:"
echo "==========="
echo ""

echo "1. Two Sum:"
curl -s "http://localhost:3000/api/submissions/$SUB1" -H "Authorization: Bearer $TOKEN" | python -m json.tool | grep -E "status|output|runtime" | head -3
echo ""

echo "2. Palindrome Number:"
curl -s "http://localhost:3000/api/submissions/$SUB2" -H "Authorization: Bearer $TOKEN" | python -m json.tool | grep -E "status|output|runtime" | head -3
echo ""

echo "3. Reverse Linked List:"
curl -s "http://localhost:3000/api/submissions/$SUB3" -H "Authorization: Bearer $TOKEN" | python -m json.tool | grep -E "status|output|runtime" | head -3
echo ""

echo "4. Maximum Subarray:"
curl -s "http://localhost:3000/api/submissions/$SUB4" -H "Authorization: Bearer $TOKEN" | python -m json.tool | grep -E "status|output|runtime" | head -3
echo ""

echo "5. Merge K Sorted Lists:"
curl -s "http://localhost:3000/api/submissions/$SUB5" -H "Authorization: Bearer $TOKEN" | python -m json.tool | grep -E "status|output|runtime" | head -3
echo ""

echo "✅ All tests submitted!"

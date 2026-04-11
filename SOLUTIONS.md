# 📝 Problem Solutions for Testing

## Quick Reference

Copy and paste these solutions into the frontend to test the submission system.

---

## 1. Two Sum (Easy)

**Problem:** Find two numbers that add up to target.

**Solution:**
```python
def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

**Expected Result:** ✅ ACCEPTED

---

## 2. Palindrome Number (Easy)

**Problem:** Check if a number is a palindrome.

**Solution:**
```python
def solution(x):
    if x < 0:
        return False

    original = x
    reversed_num = 0

    while x > 0:
        digit = x % 10
        reversed_num = reversed_num * 10 + digit
        x //= 10

    return original == reversed_num
```

**Expected Result:** ✅ ACCEPTED

---

## 3. Reverse Linked List (Medium)

**Problem:** Reverse a linked list (represented as array).

**Solution:**
```python
def solution(head):
    if not head:
        return []

    result = []
    i = len(head) - 1
    while i >= 0:
        result.append(head[i])
        i -= 1

    return result
```

**Expected Result:** ✅ ACCEPTED

---

## 4. Maximum Subarray (Medium)

**Problem:** Find the contiguous subarray with the largest sum.

**Solution:**
```python
def solution(nums):
    if not nums:
        return 0

    max_sum = current_sum = nums[0]

    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum
```

**Expected Result:** ✅ ACCEPTED

---

## 5. Merge K Sorted Lists (Hard)

**Problem:** Merge k sorted lists into one sorted list.

**Solution:**
```python
def solution(lists):
    if not lists:
        return []

    merged = []
    for lst in lists:
        merged.extend(lst)

    merged.sort()
    return merged
```

**Expected Result:** ✅ ACCEPTED

---

## 🧪 Testing Wrong Solutions

Want to test error cases? Try these:

### Wrong Answer Example
```python
def solution(nums, target):
    return [0, 0]  # Always wrong
```
**Expected:** ❌ WRONG_ANSWER

### Runtime Error Example
```python
def solution(nums, target):
    return 1/0  # Division by zero
```
**Expected:** ❌ RUNTIME_ERROR

### Time Limit Example
```python
def solution(nums, target):
    while True:  # Infinite loop
        pass
```
**Expected:** ⏱️ TIME_LIMIT

---

## 📊 How to Test

1. Go to http://localhost:5173
2. Login as `student1@example.com` / `password123`
3. Navigate to **Problems**
4. Click on any problem
5. Copy the solution above
6. Paste into the code editor
7. Click **Submit**
8. Wait 1-2 seconds for result

---

## ✅ All Solutions Should Pass

All solutions above are correct and should return:
- Status: **ACCEPTED**
- Output: "All test cases passed"
- Runtime: ~300-1500ms

---

## 🎯 Quick Test Checklist

- [ ] Two Sum → ACCEPTED
- [ ] Palindrome Number → ACCEPTED
- [ ] Reverse Linked List → ACCEPTED
- [ ] Maximum Subarray → ACCEPTED
- [ ] Merge K Sorted Lists → ACCEPTED
- [ ] Wrong solution → WRONG_ANSWER
- [ ] Runtime error → RUNTIME_ERROR


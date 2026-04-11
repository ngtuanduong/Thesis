import { SolutionMap } from '../types';

export const TIER2_SOLUTIONS: SolutionMap = {
  // nested_loops
  'Matrix Sum': `def solution(matrix):
    return sum(sum(row) for row in matrix)`,

  'Identity Matrix': `def solution(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]`,

  'Count Pairs with Sum': `def solution(nums, target):
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                count += 1
    return count`,

  'Transpose Matrix': `def solution(matrix):
    if not matrix:
        return []
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]`,

  'Matrix Diagonal Sum': `def solution(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))`,

  // functions / parameters / return_values
  'Min Max Pair': `def solution(nums):
    return [min(nums), max(nums)]`,

  'Sum and Product': `def solution(a, b):
    return [a + b, a * b]`,

  'Apply Discount': `def solution(price, discount_percent):
    return round(price * (1 - discount_percent / 100), 2)`,

  'BMI Calculator': `def solution(weight_kg, height_m):
    return round(weight_kg / (height_m ** 2), 2)`,

  'Compound Interest': `def solution(principal, rate, years):
    return round(principal * (1 + rate) ** years, 2)`,

  // lists
  'List Sum': `def solution(nums):
    total = 0
    for n in nums:
        total += n
    return total`,

  'List Maximum': `def solution(nums):
    m = nums[0]
    for n in nums[1:]:
        if n > m:
            m = n
    return m`,

  'List Minimum': `def solution(nums):
    m = nums[0]
    for n in nums[1:]:
        if n < m:
            m = n
    return m`,

  'Count Occurrences': `def solution(nums, target):
    count = 0
    for n in nums:
        if n == target:
            count += 1
    return count`,

  'Remove Duplicates Preserve Order': `def solution(nums):
    seen = set()
    result = []
    for n in nums:
        if n not in seen:
            seen.add(n)
            result.append(n)
    return result`,

  'Flatten 2D List': `def solution(matrix):
    result = []
    for row in matrix:
        for x in row:
            result.append(x)
    return result`,

  'Rotate List Right': `def solution(nums, k):
    if not nums:
        return []
    k = k % len(nums)
    return nums[-k:] + nums[:-k] if k else nums[:]`,

  'Second Largest': `def solution(nums):
    distinct = sorted(set(nums), reverse=True)
    if len(distinct) < 2:
        return None
    return distinct[1]`,

  'Reverse a List': `def solution(nums):
    result = []
    for i in range(len(nums) - 1, -1, -1):
        result.append(nums[i])
    return result`,

  'Even Numbers Only': `def solution(nums):
    return [n for n in nums if n % 2 == 0]`,

  'Double Each Element': `def solution(nums):
    return [n * 2 for n in nums]`,

  'Concatenate Lists': `def solution(a, b):
    return a + b`,

  // tuples
  'Tuple Swap': `def solution(pair):
    return [pair[1], pair[0]]`,

  'Split Even Odd': `def solution(nums):
    evens = [n for n in nums if n % 2 == 0]
    odds = [n for n in nums if n % 2 != 0]
    return [evens, odds]`,

  'Coordinate Distance': `def solution(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return round((dx * dx + dy * dy) ** 0.5, 2)`,

  // dictionaries
  'Dict from Pairs': `def solution(pairs):
    d = {}
    for k, v in pairs:
        d[k] = v
    return d`,

  'Character Frequency': `def solution(s):
    d = {}
    for c in s:
        d[c] = d.get(c, 0) + 1
    return d`,

  'Word Count': `def solution(sentence):
    d = {}
    if not sentence:
        return d
    for w in sentence.split():
        d[w] = d.get(w, 0) + 1
    return d`,

  'Merge Two Dicts': `def solution(a, b):
    result = dict(a)
    result.update(b)
    return result`,

  'Invert Dict': `def solution(d):
    return {str(v): k for k, v in d.items()}`,

  'Most Frequent Element': `def solution(nums):
    counts = {}
    for n in nums:
        counts[n] = counts.get(n, 0) + 1
    best_count = max(counts.values())
    candidates = [k for k, v in counts.items() if v == best_count]
    return min(candidates)`,

  'Dict Key Sum': `def solution(d):
    return sum(d.values())`,

  'Dict Contains Value': `def solution(d, target):
    return target in d.values()`,

  // searching
  'Linear Search': `def solution(nums, target):
    for i, n in enumerate(nums):
        if n == target:
            return i
    return -1`,

  'Iterative Binary Search': `def solution(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1`,

  'Find Minimum Index': `def solution(nums):
    idx = 0
    for i in range(1, len(nums)):
        if nums[i] < nums[idx]:
            idx = i
    return idx`,

  'Count Less Than': `def solution(nums, threshold):
    return sum(1 for n in nums if n < threshold)`,

  'Find Pair with Sum': `def solution(nums, target):
    seen = set()
    for n in nums:
        if target - n in seen:
            return True
        seen.add(n)
    return False`,

  'First Duplicate': `def solution(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return n
        seen.add(n)
    return None`,

  'Range Contains': `def solution(nums, lo, hi):
    return sum(1 for n in nums if lo <= n <= hi)`,

  // extras
  'Sum Even Indices': `def solution(nums):
    return sum(nums[i] for i in range(0, len(nums), 2))`,

  'Running Sum': `def solution(nums):
    result = []
    total = 0
    for n in nums:
        total += n
        result.append(total)
    return result`,

  'Move Zeros to End': `def solution(nums):
    non_zero = [n for n in nums if n != 0]
    zeros = [0] * (len(nums) - len(non_zero))
    return non_zero + zeros`,

  'Odd Length Strings': `def solution(words):
    return [w for w in words if len(w) % 2 == 1]`,

  'Dict from Keys': `def solution(keys, default_value):
    return {k: default_value for k in keys}`,
};

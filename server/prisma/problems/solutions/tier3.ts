import { SolutionMap } from '../types';

export const TIER3_SOLUTIONS: SolutionMap = {
  // scope
  'Counter Accumulator': `def solution(nums):
    def count_positive(arr):
        return sum(1 for x in arr if x > 0)
    return count_positive(nums)`,

  'Closure Multiplier': `def solution(factor, nums):
    def make_multiplier(f):
        def mul(x):
            return f * x
        return mul
    m = make_multiplier(factor)
    return [m(n) for n in nums]`,

  'Running Max with Helper': `def solution(nums):
    result = []
    max_so_far = None
    def step(x):
        nonlocal max_so_far
        if max_so_far is None or x > max_so_far:
            max_so_far = x
        return max_so_far
    for n in nums:
        result.append(step(n))
    return result`,

  // recursion
  'Recursive Factorial': `def solution(n):
    if n <= 1:
        return 1
    return n * solution(n - 1)`,

  'Recursive Fibonacci': `def solution(n):
    memo = {}
    def f(k):
        if k < 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = f(k - 1) + f(k - 2)
        return memo[k]
    return f(n)`,

  'Recursive Sum of Digits': `def solution(n):
    if n < 10:
        return n
    return n % 10 + solution(n // 10)`,

  'Recursive Power': `def solution(base, exp):
    if exp == 0:
        return 1
    return base * solution(base, exp - 1)`,

  'Recursive String Reverse': `def solution(s):
    if len(s) <= 1:
        return s
    return solution(s[1:]) + s[0]`,

  'Recursive List Sum': `def solution(nums):
    if not nums:
        return 0
    return nums[0] + solution(nums[1:])`,

  'Tower of Hanoi Moves': `def solution(n):
    if n <= 0:
        return 0
    return 2 * solution(n - 1) + 1`,

  // sets
  'Unique Elements Count': `def solution(nums):
    return len(set(nums))`,

  'Set Intersection Sorted': `def solution(a, b):
    return sorted(set(a) & set(b))`,

  'Set Union Sorted': `def solution(a, b):
    return sorted(set(a) | set(b))`,

  'Symmetric Difference': `def solution(a, b):
    return sorted(set(a) ^ set(b))`,

  // stacks
  'Valid Parentheses Simple': `def solution(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in '([{':
            stack.append(c)
        else:
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack`,

  'Reverse Using Stack': `def solution(nums):
    stack = []
    for n in nums:
        stack.append(n)
    result = []
    while stack:
        result.append(stack.pop())
    return result`,

  'Stack Operations Result': `def solution(ops):
    stack = []
    for op in ops:
        if op[0] == 'push':
            stack.append(op[1])
        elif op[0] == 'pop' and stack:
            stack.pop()
    return stack`,

  'Next Greater Element': `def solution(nums):
    result = [-1] * len(nums)
    stack = []
    for i, n in enumerate(nums):
        while stack and nums[stack[-1]] < n:
            result[stack.pop()] = n
        stack.append(i)
    return result`,

  // queues
  'Queue FIFO Simulation': `def solution(ops):
    queue = []
    for op in ops:
        if op[0] == 'enq':
            queue.append(op[1])
        elif op[0] == 'deq' and queue:
            queue.pop(0)
    return queue`,

  'Rotate Queue Left': `def solution(nums, k):
    if not nums:
        return []
    k = k % len(nums)
    return nums[k:] + nums[:k]`,

  'Level Order Sum': `def solution(tree):
    return sum(x for x in tree if x is not None)`,

  // classes
  'BankAccount Class': `class BankAccount:
    def __init__(self):
        self.balance = 0
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount

def solution(ops):
    acc = BankAccount()
    for op in ops:
        if op[0] == 'deposit':
            acc.deposit(op[1])
        elif op[0] == 'withdraw':
            acc.withdraw(op[1])
    return acc.balance`,

  'Counter Class': `class Counter:
    def __init__(self):
        self.count = 0
    def inc(self):
        self.count += 1
    def dec(self):
        self.count -= 1
    def reset(self):
        self.count = 0

def solution(ops):
    c = Counter()
    for op in ops:
        getattr(c, op[0])()
    return c.count`,

  'Point Class Distance': `class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

def solution(p1, p2):
    return Point(p1[0], p1[1]).manhattan(Point(p2[0], p2[1]))`,

  'Inventory Class': `class Inventory:
    def __init__(self):
        self.items = {}
    def add(self, name, qty):
        self.items[name] = self.items.get(name, 0) + qty
    def remove(self, name, qty):
        if name in self.items:
            self.items[name] = max(0, self.items[name] - qty)

def solution(ops):
    inv = Inventory()
    for op in ops:
        if op[0] == 'add':
            inv.add(op[1], op[2])
        elif op[0] == 'remove':
            inv.remove(op[1], op[2])
    return dict(sorted(inv.items.items()))`,

  'Timer Class Elapsed': `class Timer:
    def __init__(self):
        self.total = 0
    def record(self, start, end):
        self.total += end - start

def solution(intervals):
    t = Timer()
    for iv in intervals:
        t.record(iv[0], iv[1])
    return t.total`,

  // sorting
  'Bubble Sort Ascending': `def solution(nums):
    arr = list(nums)
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr`,

  'Selection Sort': `def solution(nums):
    arr = list(nums)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr`,

  'Insertion Sort': `def solution(nums):
    arr = list(nums)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr`,

  'Sort Descending': `def solution(nums):
    return sorted(nums, reverse=True)`,

  'Sort by Absolute Value': `def solution(nums):
    return sorted(nums, key=lambda x: (abs(x), x))`,

  'Sort Words by Length': `def solution(words):
    return sorted(words, key=lambda w: (len(w), w))`,

  'Merge Two Sorted': `def solution(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result`,

  // sliding_window
  'Max Sum Subarray of Size K': `def solution(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        if window > best:
            best = window
    return best`,

  'Longest Substring No Repeat': `def solution(s):
    seen = {}
    best = 0
    left = 0
    for right, c in enumerate(s):
        if c in seen and seen[c] >= left:
            left = seen[c] + 1
        seen[c] = right
        if right - left + 1 > best:
            best = right - left + 1
    return best`,

  'Min Subarray Sum \u2265 Target': `def solution(nums, target):
    left = 0
    window = 0
    best = 0
    for right in range(len(nums)):
        window += nums[right]
        while window >= target:
            length = right - left + 1
            if best == 0 or length < best:
                best = length
            window -= nums[left]
            left += 1
    return best`,

  'Average of Subarrays': `def solution(nums, k):
    result = []
    window = sum(nums[:k])
    result.append(round(window / k, 2))
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        result.append(round(window / k, 2))
    return result`,

  'Count Distinct in Windows': `def solution(nums, k):
    if k > len(nums):
        return []
    result = []
    counts = {}
    for i in range(k):
        counts[nums[i]] = counts.get(nums[i], 0) + 1
    result.append(len(counts))
    for i in range(k, len(nums)):
        counts[nums[i]] = counts.get(nums[i], 0) + 1
        out = nums[i - k]
        counts[out] -= 1
        if counts[out] == 0:
            del counts[out]
        result.append(len(counts))
    return result`,

  'Longest Substring K Distinct': `def solution(s, k):
    if k == 0:
        return 0
    counts = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        counts[c] = counts.get(c, 0) + 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best`,

  'Fixed Window Max': `def solution(nums, k):
    from collections import deque
    dq = deque()
    result = []
    for i, n in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] < n:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result`,
};

import { SolutionMap } from '../types';

export const TIER5_SOLUTIONS: SolutionMap = {
  // dynamic_programming
  'Climbing Stairs DP': `def solution(n):
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a`,

  'House Robber': `def solution(nums):
    prev = curr = 0
    for n in nums:
        prev, curr = curr, max(curr, prev + n)
    return curr`,

  'Coin Change DP': `def solution(coins, amount):
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
    return dp[amount] if dp[amount] != INF else -1`,

  'Longest Common Subsequence': `def solution(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]`,

  'Longest Increasing Subsequence': `def solution(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)`,

  'Zero One Knapsack': `def solution(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    return dp[n][W]`,

  // trees
  'Binary Tree Max Depth': `def solution(tree):
    if not tree:
        return 0
    # level order: compute depth from index formula
    n = len(tree)
    def depth(i):
        if i >= n or tree[i] is None:
            return 0
        return 1 + max(depth(2 * i + 1), depth(2 * i + 2))
    return depth(0)`,

  'Count Tree Nodes': `def solution(tree):
    return sum(1 for x in tree if x is not None)`,

  'Tree Level Order Traversal': `def solution(tree):
    if not tree:
        return []
    # Build level-by-level using BFS over indices; skip nulls.
    result = []
    # children of tree[i] at 2i+1, 2i+2 — but only if they are within bounds and non-null.
    from collections import deque
    n = len(tree)
    q = deque([0])
    while q:
        level = []
        size = len(q)
        for _ in range(size):
            idx = q.popleft()
            if idx >= n or tree[idx] is None:
                continue
            level.append(tree[idx])
            q.append(2 * idx + 1)
            q.append(2 * idx + 2)
        if level:
            result.append(level)
    return result`,

  'Sum of Left Leaves': `def solution(tree):
    if not tree:
        return 0
    n = len(tree)
    total = 0
    def walk(i, is_left):
        nonlocal total
        if i >= n or tree[i] is None:
            return
        left_idx, right_idx = 2 * i + 1, 2 * i + 2
        left_val = tree[left_idx] if left_idx < n else None
        right_val = tree[right_idx] if right_idx < n else None
        is_leaf = left_val is None and right_val is None
        if is_leaf and is_left:
            total += tree[i]
        walk(left_idx, True)
        walk(right_idx, False)
    walk(0, False)
    return total`,

  // graphs
  'Number of Islands': `def solution(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if visited[r][c] or grid[r][c] == 0:
            return
        visited[r][c] = True
        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                count += 1
                dfs(r, c)
    return count`,

  'BFS Shortest Path in Grid': `def solution(grid):
    from collections import deque
    if not grid or not grid[0]:
        return -1
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return -1
    q = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while q:
        r, c, d = q.popleft()
        if r == rows - 1 and c == cols - 1:
            return d
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == 0:
                visited.add((nr, nc))
                q.append((nr, nc, d + 1))
    return -1`,

  'Course Schedule Cycle Detect': `def solution(num_courses, prerequisites):
    from collections import deque, defaultdict
    graph = defaultdict(list)
    indeg = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(num_courses) if indeg[i] == 0])
    taken = 0
    while q:
        x = q.popleft()
        taken += 1
        for y in graph[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                q.append(y)
    return taken == num_courses`,

  // backtracking
  'All Permutations': `def solution(nums):
    result = []
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i + 1:])
            path.pop()
    backtrack([], sorted(nums))
    return sorted(result)`,

  'Subsets': `def solution(nums):
    nums = sorted(nums)
    result = [[]]
    for n in nums:
        result.extend([sub + [n] for sub in result])
    result.sort(key=lambda x: (len(x), x))
    return result`,

  'N-Queens Count': `def solution(n):
    count = 0
    cols = set()
    diag1 = set()
    diag2 = set()
    def backtrack(r):
        nonlocal count
        if r == n:
            count += 1
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c); diag1.add(r - c); diag2.add(r + c)
            backtrack(r + 1)
            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)
    backtrack(0)
    return count`,

  // bit_manipulation
  'Single Number XOR': `def solution(nums):
    result = 0
    for n in nums:
        result ^= n
    return result`,

  'Count Set Bits': `def solution(n):
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1
    return count`,

  'Power of Two Check': `def solution(n):
    return n > 0 and (n & (n - 1)) == 0`,

  'Missing Number XOR': `def solution(nums):
    result = len(nums)
    for i, n in enumerate(nums):
        result ^= i ^ n
    return result`,
};

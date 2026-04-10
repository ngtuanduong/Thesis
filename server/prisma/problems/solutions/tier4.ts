import { SolutionMap } from '../types';

export const TIER4_SOLUTIONS: SolutionMap = {
  // inheritance
  'Shape Area Polymorphism': `class Shape:
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r * self.r

class Square(Shape):
    def __init__(self, s):
        self.s = s
    def area(self):
        return self.s * self.s

def solution(shapes):
    total = 0
    for spec in shapes:
        if spec[0] == 'circle':
            total += Circle(spec[1]).area()
        elif spec[0] == 'square':
            total += Square(spec[1]).area()
    return round(total, 2)`,

  'Employee Salary Hierarchy': `class Employee:
    def __init__(self, base):
        self.base = base
    def pay(self):
        return float(self.base)

class Manager(Employee):
    def pay(self):
        return float(self.base) * 1.2

def solution(staff):
    total = 0
    for spec in staff:
        if spec[0] == 'manager':
            total += Manager(spec[1]).pay()
        else:
            total += Employee(spec[1]).pay()
    return total`,

  'Animal Sound Polymorphism': `class Animal:
    def sound(self):
        return "generic"

class Dog(Animal):
    def sound(self):
        return "woof"

class Cat(Animal):
    def sound(self):
        return "meow"

class Cow(Animal):
    def sound(self):
        return "moo"

def solution(animals):
    reg = {'dog': Dog, 'cat': Cat, 'cow': Cow}
    return [reg[a]().sound() for a in animals]`,

  'Vehicle Speed Override': `class Vehicle:
    def max_speed(self):
        return 100

class Car(Vehicle):
    def max_speed(self):
        return 150

class Bike(Vehicle):
    def max_speed(self):
        return 40

def solution(vehicles):
    reg = {'car': Car, 'bike': Bike}
    return sum(reg[v]().max_speed() for v in vehicles)`,

  // encapsulation
  'Private Balance Protection': `class SafeAccount:
    def __init__(self):
        self._balance = 0
    def deposit(self, amt):
        if amt > 0:
            self._balance += amt
    def withdraw(self, amt):
        if amt <= self._balance:
            self._balance -= amt

def solution(ops):
    a = SafeAccount()
    for op in ops:
        if op[0] == 'deposit':
            a.deposit(op[1])
        else:
            a.withdraw(op[1])
    return a._balance`,

  'Temperature Validator': `class Thermometer:
    def __init__(self):
        self._celsius = 0
    def read(self, v):
        if v > 100:
            self._celsius = 100
        elif v < -50:
            self._celsius = -50
        else:
            self._celsius = v

def solution(readings):
    t = Thermometer()
    for r in readings:
        t.read(r)
    return t._celsius`,

  'Password Strength Check': `class User:
    def __init__(self):
        self._pw = None
    def set_password(self, pw):
        if len(pw) >= 8 and any(c.isdigit() for c in pw):
            self._pw = pw
            return True
        return False

def solution(passwords):
    u = User()
    for pw in passwords:
        if not u.set_password(pw):
            return False
    return True`,

  // polymorphism
  'Payment Processor Strategies': `class Payment:
    rate = 0
    def fee(self, amount):
        return amount * self.rate

class CreditCard(Payment):
    rate = 0.02

class DebitCard(Payment):
    rate = 0.01

class Cash(Payment):
    rate = 0

def solution(txs):
    reg = {'credit': CreditCard, 'debit': DebitCard, 'cash': Cash}
    total = 0
    for tx in txs:
        total += reg[tx[0]]().fee(tx[1])
    return round(total, 2)`,

  'Notification Dispatcher': `class Notifier:
    prefix = ""
    def format(self, msg):
        return self.prefix + msg

class EmailNotifier(Notifier):
    prefix = "email: "

class SmsNotifier(Notifier):
    prefix = "sms: "

class PushNotifier(Notifier):
    prefix = "push: "

def solution(items):
    reg = {'email': EmailNotifier, 'sms': SmsNotifier, 'push': PushNotifier}
    return [reg[ch]().format(msg) for ch, msg in items]`,

  // two_pointers
  'Two Sum Sorted': `def solution(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return [-1, -1]`,

  'Is Palindrome Two Pointers': `def solution(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True`,

  'Remove Target In-Place': `def solution(nums, target):
    return [x for x in nums if x != target]`,

  'Container With Most Water': `def solution(heights):
    if not heights:
        return 0
    lo, hi = 0, len(heights) - 1
    best = 0
    while lo < hi:
        h = min(heights[lo], heights[hi])
        area = h * (hi - lo)
        if area > best:
            best = area
        if heights[lo] < heights[hi]:
            lo += 1
        else:
            hi -= 1
    return best`,

  'Move Zeroes End Two Pointer': `def solution(nums):
    result = list(nums)
    write = 0
    for i in range(len(result)):
        if result[i] != 0:
            result[write], result[i] = result[i], result[write]
            write += 1
    return result`,

  'Sorted Squares': `def solution(nums):
    n = len(nums)
    result = [0] * n
    lo, hi = 0, n - 1
    idx = n - 1
    while lo <= hi:
        if abs(nums[lo]) > abs(nums[hi]):
            result[idx] = nums[lo] * nums[lo]
            lo += 1
        else:
            result[idx] = nums[hi] * nums[hi]
            hi -= 1
        idx -= 1
    return result`,

  // greedy
  'Assign Cookies': `def solution(greed, cookies):
    greed = sorted(greed)
    cookies = sorted(cookies)
    i = j = 0
    while i < len(greed) and j < len(cookies):
        if cookies[j] >= greed[i]:
            i += 1
        j += 1
    return i`,

  'Jump Game Reachable': `def solution(nums):
    reach = 0
    for i, n in enumerate(nums):
        if i > reach:
            return False
        if i + n > reach:
            reach = i + n
    return True`,

  'Gas Station Circuit': `def solution(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start`,

  'Activity Scheduling': `def solution(activities):
    if not activities:
        return 0
    sorted_acts = sorted(activities, key=lambda a: a[1])
    count = 0
    last_end = float('-inf')
    for s, e in sorted_acts:
        if s >= last_end:
            count += 1
            last_end = e
    return count`,

  'Coin Change Greedy': `def solution(amount):
    coins = [25, 10, 5, 1]
    count = 0
    for c in coins:
        count += amount // c
        amount %= c
    return count`,

  // divide_and_conquer
  'Merge Sort': `def solution(nums):
    if len(nums) <= 1:
        return list(nums)
    mid = len(nums) // 2
    left = solution(nums[:mid])
    right = solution(nums[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result`,

  'Quick Sort': `def solution(nums):
    if len(nums) <= 1:
        return list(nums)
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    mid = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return solution(left) + mid + solution(right)`,

  'Max Subarray Sum DNC': `def solution(nums):
    def helper(lo, hi):
        if lo == hi:
            return nums[lo]
        mid = (lo + hi) // 2
        left = helper(lo, mid)
        right = helper(mid + 1, hi)
        # cross
        left_sum = float('-inf')
        s = 0
        for i in range(mid, lo - 1, -1):
            s += nums[i]
            if s > left_sum:
                left_sum = s
        right_sum = float('-inf')
        s = 0
        for i in range(mid + 1, hi + 1):
            s += nums[i]
            if s > right_sum:
                right_sum = s
        cross = left_sum + right_sum
        return max(left, right, cross)
    return helper(0, len(nums) - 1)`,

  'Find Kth Smallest': `def solution(nums, k):
    arr = sorted(nums)
    return arr[k - 1]`,

  'Fast Power': `def solution(base, exp):
    MOD = 1_000_000_007
    result = 1
    b = base % MOD
    while exp > 0:
        if exp & 1:
            result = (result * b) % MOD
        b = (b * b) % MOD
        exp >>= 1
    return result`,
};

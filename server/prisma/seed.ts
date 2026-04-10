import { PrismaClient, Role, Difficulty } from '@prisma/client';
import * as bcrypt from 'bcrypt';
import { seedAdaptive } from './seed-adaptive';
import { generateStarterCode } from '../src/problems/starter-code.util';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seed...');

  // Clean existing data (skip if tables don't exist)
  console.log('🗑️  Cleaning existing data...');
  try {
    await prisma.submission.deleteMany();
    await prisma.testCase.deleteMany();
    await prisma.problemEmbedding.deleteMany();
    await prisma.skillEmbedding.deleteMany();
    await prisma.problem.deleteMany();
    await prisma.enrollment.deleteMany();
    await prisma.course.deleteMany();
    await prisma.user.deleteMany();
  } catch (error) {
    console.log('   (Tables may not exist yet, skipping cleanup)');
  }

  // Create users
  console.log('👥 Creating users...');
  const hashedPassword = await bcrypt.hash('password123', 10);

  const admin = await prisma.user.create({
    data: {
      email: 'admin@example.com',
      password: hashedPassword,
      name: 'Admin User',
      role: Role.ADMIN,
    },
  });

  const instructor = await prisma.user.create({
    data: {
      email: 'instructor@example.com',
      password: hashedPassword,
      name: 'Dr. John Smith',
      role: Role.INSTRUCTOR,
    },
  });

  const student1 = await prisma.user.create({
    data: {
      email: 'student1@example.com',
      password: hashedPassword,
      name: 'Alice Johnson',
      role: Role.STUDENT,
    },
  });

  const student2 = await prisma.user.create({
    data: {
      email: 'student2@example.com',
      password: hashedPassword,
      name: 'Bob Williams',
      role: Role.STUDENT,
    },
  });

  console.log(`✅ Created ${4} users`);

  // Create courses
  console.log('📚 Creating courses...');
  const course1 = await prisma.course.create({
    data: {
      title: 'Introduction to Python Programming',
      description:
        'Learn the fundamentals of Python programming including data structures, algorithms, and problem-solving.',
      instructorId: instructor.id,
    },
  });

  const course2 = await prisma.course.create({
    data: {
      title: 'Data Structures and Algorithms',
      description:
        'Advanced course covering sorting algorithms, trees, graphs, dynamic programming, and complexity analysis.',
      instructorId: instructor.id,
    },
  });

  console.log(`✅ Created ${2} courses`);

  // Create enrollments
  console.log('📝 Creating enrollments...');
  await prisma.enrollment.createMany({
    data: [
      { userId: student1.id, courseId: course1.id },
      { userId: student1.id, courseId: course2.id },
      { userId: student2.id, courseId: course1.id },
    ],
  });
  console.log(`✅ Created ${3} enrollments`);

  // Create problems with test cases
  console.log('❓ Creating problems...');

  // Problem 1: Two Sum (Easy)
  const problem1 = await prisma.problem.create({
    data: {
      title: 'Two Sum',
      description: `Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

**Example:**
\`\`\`
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
\`\`\`

**Constraints:**
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9`,
      difficulty: Difficulty.EASY,
      courseId: course1.id,
      tags: ['array', 'hash-table'],
      starterCode: generateStarterCode([{ input: JSON.stringify({ nums: [2, 7, 11, 15], target: 9 }) }]),
      testCases: {
        create: [
          {
            input: JSON.stringify({ nums: [2, 7, 11, 15], target: 9 }),
            expected: JSON.stringify([0, 1]),
            isHidden: false,
          },
          {
            input: JSON.stringify({ nums: [3, 2, 4], target: 6 }),
            expected: JSON.stringify([1, 2]),
            isHidden: false,
          },
          {
            input: JSON.stringify({ nums: [3, 3], target: 6 }),
            expected: JSON.stringify([0, 1]),
            isHidden: true,
          },
        ],
      },
    },
  });

  // Problem 2: Palindrome Number (Easy)
  const problem2 = await prisma.problem.create({
    data: {
      title: 'Palindrome Number',
      description: `Given an integer x, return true if x is a palindrome, and false otherwise.

**Example 1:**
\`\`\`
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.
\`\`\`

**Example 2:**
\`\`\`
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
\`\`\`

**Constraints:**
- -2^31 <= x <= 2^31 - 1`,
      difficulty: Difficulty.EASY,
      courseId: course1.id,
      tags: ['math'],
      starterCode: generateStarterCode([{ input: '121' }]),
      testCases: {
        create: [
          { input: '121', expected: 'true', isHidden: false },
          { input: '-121', expected: 'false', isHidden: false },
          { input: '10', expected: 'false', isHidden: false },
          { input: '12321', expected: 'true', isHidden: true },
        ],
      },
    },
  });

  // Problem 3: Reverse Linked List (Medium)
  const problem3 = await prisma.problem.create({
    data: {
      title: 'Reverse Linked List',
      description: `Given the head of a singly linked list, reverse the list, and return the reversed list.

**Example 1:**
\`\`\`
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
\`\`\`

**Example 2:**
\`\`\`
Input: head = [1,2]
Output: [2,1]
\`\`\`

**Constraints:**
- The number of nodes in the list is the range [0, 5000].
- -5000 <= Node.val <= 5000`,
      difficulty: Difficulty.MEDIUM,
      courseId: course2.id,
      tags: ['linked-list', 'recursion'],
      starterCode: generateStarterCode([{ input: JSON.stringify([1, 2, 3, 4, 5]) }]),
      testCases: {
        create: [
          {
            input: JSON.stringify([1, 2, 3, 4, 5]),
            expected: JSON.stringify([5, 4, 3, 2, 1]),
            isHidden: false,
          },
          {
            input: JSON.stringify([1, 2]),
            expected: JSON.stringify([2, 1]),
            isHidden: false,
          },
          {
            input: JSON.stringify([]),
            expected: JSON.stringify([]),
            isHidden: true,
          },
        ],
      },
    },
  });

  // Problem 4: Maximum Subarray (Medium)
  const problem4 = await prisma.problem.create({
    data: {
      title: 'Maximum Subarray',
      description: `Given an integer array nums, find the subarray with the largest sum, and return its sum.

**Example 1:**
\`\`\`
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
\`\`\`

**Example 2:**
\`\`\`
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.
\`\`\`

**Constraints:**
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4`,
      difficulty: Difficulty.MEDIUM,
      courseId: course2.id,
      tags: ['array', 'dynamic-programming', 'divide-and-conquer'],
      starterCode: generateStarterCode([{ input: JSON.stringify([-2, 1, -3, 4, -1, 2, 1, -5, 4]) }]),
      testCases: {
        create: [
          {
            input: JSON.stringify([-2, 1, -3, 4, -1, 2, 1, -5, 4]),
            expected: '6',
            isHidden: false,
          },
          { input: JSON.stringify([1]), expected: '1', isHidden: false },
          {
            input: JSON.stringify([5, 4, -1, 7, 8]),
            expected: '23',
            isHidden: true,
          },
        ],
      },
    },
  });

  // Problem 5: Merge K Sorted Lists (Hard)
  const problem5 = await prisma.problem.create({
    data: {
      title: 'Merge K Sorted Lists',
      description: `You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

**Example 1:**
\`\`\`
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6
\`\`\`

**Constraints:**
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4`,
      difficulty: Difficulty.HARD,
      courseId: course2.id,
      tags: ['linked-list', 'divide-and-conquer', 'heap', 'merge-sort'],
      starterCode: generateStarterCode([{ input: JSON.stringify([[1, 4, 5], [1, 3, 4], [2, 6]]) }]),
      testCases: {
        create: [
          {
            input: JSON.stringify([[1, 4, 5], [1, 3, 4], [2, 6]]),
            expected: JSON.stringify([1, 1, 2, 3, 4, 4, 5, 6]),
            isHidden: false,
          },
          {
            input: JSON.stringify([]),
            expected: JSON.stringify([]),
            isHidden: false,
          },
          {
            input: JSON.stringify([[]]),
            expected: JSON.stringify([]),
            isHidden: true,
          },
        ],
      },
    },
  });

  console.log(`✅ Created ${5} problems with test cases`);

  // Seed adaptive learning data (concepts, KG edges, new problems, Elo, embeddings).
  // course1 receives T1/T2 (Python Intro), course2 receives T3/T4/T5 (DSA).
  await seedAdaptive(course1.id, course2.id);

  const finalCount = await prisma.problem.count();

  console.log('\n✨ Database seeding completed successfully!');
  console.log('\n📊 Summary:');
  console.log(`   - Users: 4 (1 admin, 1 instructor, 2 students)`);
  console.log(`   - Courses: 2`);
  console.log(`   - Enrollments: 3`);
  console.log(`   - Problems: ${finalCount} total`);
  console.log('\n🔑 Login Credentials (all users):');
  console.log(`   - Email: admin@example.com | student1@example.com | student2@example.com`);
  console.log(`   - Password: password123`);
}

main()
  .catch((e) => {
    console.error('❌ Error during seeding:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

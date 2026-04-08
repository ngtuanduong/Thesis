import { Test, TestingModule } from '@nestjs/testing';
import { JwtService } from '@nestjs/jwt';
import { ConflictException, UnauthorizedException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { AuthService } from './auth.service';
import { UsersService } from '../users/users.service';

jest.mock('bcrypt');

describe('AuthService', () => {
  let authService: AuthService;
  let mockCreate: jest.Mock;
  let mockFindByEmail: jest.Mock;
  let mockSign: jest.Mock;

  const mockUser = {
    id: 'user-1',
    email: 'test@example.com',
    name: 'Test User',
    password: '$2b$10$hashedpassword',
    role: 'STUDENT',
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  beforeEach(async () => {
    mockCreate = jest.fn();
    mockFindByEmail = jest.fn();
    mockSign = jest.fn().mockReturnValue('mock-jwt-token');

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        { provide: UsersService, useValue: { create: mockCreate, findByEmail: mockFindByEmail } },
        { provide: JwtService, useValue: { sign: mockSign } },
      ],
    }).compile();

    authService = module.get<AuthService>(AuthService);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('register', () => {
    const registerDto = {
      email: 'test@example.com',
      password: 'password123',
      name: 'Test User',
      role: 'STUDENT' as const,
    };

    it('should create a user with hashed password and return token', async () => {
      (bcrypt.hash as jest.Mock).mockResolvedValue('hashed-password');
      mockCreate.mockResolvedValue(mockUser);

      const result = await authService.register(registerDto);

      expect(bcrypt.hash).toHaveBeenCalledWith('password123', 10);
      expect(mockCreate).toHaveBeenCalledWith({
        ...registerDto,
        password: 'hashed-password',
      });
      expect(mockSign).toHaveBeenCalledWith({
        sub: mockUser.id,
        role: mockUser.role,
      });
      expect(result).toEqual({
        user: {
          id: mockUser.id,
          email: mockUser.email,
          name: mockUser.name,
          role: mockUser.role,
        },
        token: 'mock-jwt-token',
      });
    });

    it('should throw ConflictException if email already exists', async () => {
      (bcrypt.hash as jest.Mock).mockResolvedValue('hashed-password');
      mockCreate.mockRejectedValue(
        new ConflictException('Email already exists'),
      );

      await expect(authService.register(registerDto)).rejects.toThrow(
        ConflictException,
      );
    });
  });

  describe('login', () => {
    const loginDto = {
      email: 'test@example.com',
      password: 'password123',
    };

    it('should return token on valid credentials', async () => {
      mockFindByEmail.mockResolvedValue(mockUser);
      (bcrypt.compare as jest.Mock).mockResolvedValue(true);

      const result = await authService.login(loginDto);

      expect(mockFindByEmail).toHaveBeenCalledWith(loginDto.email);
      expect(bcrypt.compare).toHaveBeenCalledWith(
        loginDto.password,
        mockUser.password,
      );
      expect(result).toEqual({
        user: {
          id: mockUser.id,
          email: mockUser.email,
          name: mockUser.name,
          role: mockUser.role,
        },
        token: 'mock-jwt-token',
      });
    });

    it('should throw UnauthorizedException on wrong password', async () => {
      mockFindByEmail.mockResolvedValue(mockUser);
      (bcrypt.compare as jest.Mock).mockResolvedValue(false);

      await expect(authService.login(loginDto)).rejects.toThrow(
        UnauthorizedException,
      );
    });

    it('should throw UnauthorizedException on non-existent user', async () => {
      mockFindByEmail.mockResolvedValue(null);

      await expect(authService.login(loginDto)).rejects.toThrow(
        UnauthorizedException,
      );
    });
  });
});

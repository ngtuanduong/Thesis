import { LoggingMiddleware } from './logging.middleware';

describe('LoggingMiddleware', () => {
  let middleware: LoggingMiddleware;
  let mockReq: any;
  let mockRes: any;
  let mockNext: jest.Mock;
  let finishCallback: () => void;

  beforeEach(() => {
    middleware = new LoggingMiddleware();
    mockReq = { method: 'GET', originalUrl: '/api/problems' };
    mockRes = {
      statusCode: 200,
      on: jest.fn((event: string, cb: () => void) => {
        if (event === 'finish') finishCallback = cb;
      }),
    };
    mockNext = jest.fn();
  });

  it('should call next()', () => {
    middleware.use(mockReq, mockRes, mockNext);
    expect(mockNext).toHaveBeenCalled();
  });

  it('should register a finish event listener on response', () => {
    middleware.use(mockReq, mockRes, mockNext);
    expect(mockRes.on).toHaveBeenCalledWith('finish', expect.any(Function));
  });

  it('should log request details on finish', () => {
    const logSpy = jest.spyOn((middleware as any).logger, 'log').mockImplementation();

    middleware.use(mockReq, mockRes, mockNext);
    mockRes.statusCode = 200;
    finishCallback();

    expect(logSpy).toHaveBeenCalledWith(
      expect.stringContaining('GET /api/problems 200'),
    );
  });

  it('should use warn level for status >= 400', () => {
    const warnSpy = jest.spyOn((middleware as any).logger, 'warn').mockImplementation();

    middleware.use(mockReq, mockRes, mockNext);
    mockRes.statusCode = 404;
    finishCallback();

    expect(warnSpy).toHaveBeenCalledWith(
      expect.stringContaining('GET /api/problems 404'),
    );
  });

  it('should use warn level for 500 errors', () => {
    const warnSpy = jest.spyOn((middleware as any).logger, 'warn').mockImplementation();

    middleware.use(mockReq, mockRes, mockNext);
    mockRes.statusCode = 500;
    finishCallback();

    expect(warnSpy).toHaveBeenCalledWith(
      expect.stringContaining('GET /api/problems 500'),
    );
  });

  it('should include duration in ms in log message', () => {
    const logSpy = jest.spyOn((middleware as any).logger, 'log').mockImplementation();

    middleware.use(mockReq, mockRes, mockNext);
    mockRes.statusCode = 200;
    finishCallback();

    expect(logSpy).toHaveBeenCalledWith(expect.stringMatching(/\d+ms/));
  });
});

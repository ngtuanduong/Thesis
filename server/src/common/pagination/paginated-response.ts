export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}

/**
 * Generic Prisma pagination helper.
 * Runs findMany + count in parallel and returns a standardised paginated response.
 */
export async function paginate<T>(
  model: {
    findMany: (args: any) => Promise<T[]>;
    count: (args: any) => Promise<number>;
  },
  args: {
    where?: any;
    orderBy?: any;
    include?: any;
    select?: any;
  },
  pagination: { page: number; pageSize: number },
): Promise<PaginatedResponse<T>> {
  const { page, pageSize } = pagination;
  const skip = (page - 1) * pageSize;

  const [data, total] = await Promise.all([
    model.findMany({ ...args, skip, take: pageSize }),
    model.count({ where: args.where }),
  ]);

  return { data, total, page, pageSize };
}

# Backend Core App

**File**: `packages/server/src/index.ts`

## App Class

Main application orchestrator managing all subsystems.

```typescript
class App {
  app: express.Application
  AppDataSource: DataSource          // TypeORM
  nodesPool: NodesPool               // Component nodes
  abortControllerPool: AbortControllerPool
  cachePool: CachePool               // Response cache
  telemetry: Telemetry               // Analytics
  rateLimiterManager: RateLimiterManager
  sseStreamer: SSEStreamer           // Real-time events
  identityManager: IdentityManager   // Auth
  metricsProvider: IMetricsProvider  // Prometheus/OTEL
  queueManager: QueueManager         // BullMQ
  redisSubscriber: RedisEventSubscriber
  usageCacheManager: UsageCacheManager
}
```

## Initialization Sequence

**Location**: `src/index.ts:81-157`

1. Database connection (TypeORM)
2. Run migrations
3. Initialize Identity Manager
4. Load Nodes Pool
5. Setup Abort Controllers
6. Initialize encryption key
7. Setup Rate Limiters
8. Initialize Cache Pool
9. Setup Usage Cache Manager
10. Initialize Telemetry
11. Setup SSE Streamer
12. Setup Queue Manager (if MODE=QUEUE)
13. Connect Redis Subscriber (if MODE=QUEUE)

## Configuration Phase

```typescript
async config() {
  // Body parsing
  app.use(express.json({ limit: '50mb' }))

  // Trust proxy
  app.set('trust proxy', true)

  // CORS
  app.use(cors(getCorsOptions()))

  // Cookie parsing
  app.use(cookieParser())

  // Security headers
  app.disable('x-powered-by')

  // Sanitization
  app.use(sanitizeMiddleware)

  // Routes
  app.use('/api/v1', flowiseApiV1Router)

  // Error handling
  app.use(errorHandlerMiddleware)
}
```

## Server Startup

```typescript
async start() {
  await this.initDatabase()
  await this.config()

  const server = http.createServer(this.app)
  server.listen(PORT, () => {
    logger.info(`Server listening on port ${PORT}`)
  })
}
```

## Middleware Pipeline

1. CORS
2. Body Parser
3. Cookie Parser
4. Session
5. Sanitization
6. Request Logger
7. Rate Limiting
8. Authentication
9. Authorization
10. Route Handler
11. Error Handler

## Key Imports

```typescript
import express from 'express'
import { DataSource } from 'typeorm'
import { NodesPool } from './NodesPool'
import { CachePool } from './CachePool'
import flowiseApiV1Router from './routes'
```

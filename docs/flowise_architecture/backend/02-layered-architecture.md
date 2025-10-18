# Backend Layered Architecture

## Architecture Pattern

**Pattern**: Routes → Controllers → Services → Database

## Layer 1: Routes

**Location**: `src/routes/`

Define API endpoints and attach middleware.

```typescript
// routes/chatflows/index.ts
const router = express.Router()

router.get('/', verifyToken, chatflowsController.getAllChatflows)
router.post('/', verifyToken, chatflowsController.createChatflow)
router.put('/:id', verifyToken, chatflowsController.updateChatflow)
router.delete('/:id', verifyToken, chatflowsController.deleteChatflow)

export default router
```

**Responsibilities**:
- URL mapping
- Middleware attachment
- Parameter parsing

## Layer 2: Controllers

**Location**: `src/controllers/`

Handle HTTP request/response.

```typescript
// controllers/chatflows/index.ts
const getAllChatflows = async (req: Request, res: Response) => {
  try {
    const chatflows = await chatflowsService.getAllChatflows(
      req.user.workspaceId
    )
    return res.json(chatflows)
  } catch (error) {
    return res.status(500).json({ error: error.message })
  }
}
```

**Responsibilities**:
- Parse request
- Validate input
- Call service layer
- Format response
- Handle errors

## Layer 3: Services

**Location**: `src/services/`

Contain business logic.

```typescript
// services/chatflows/index.ts
const getAllChatflows = async (workspaceId: string) => {
  const repo = getRepository(ChatFlow)
  const chatflows = await repo.find({
    where: { workspaceId }
  })

  return chatflows.map(flow => ({
    ...flow,
    flowData: JSON.parse(flow.flowData)
  }))
}
```

**Responsibilities**:
- Business logic
- Data transformation
- External API calls
- Transaction management

## Layer 4: Database

**Location**: `src/database/entities/`

TypeORM entities.

```typescript
@Entity()
export class ChatFlow {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  name: string

  @Column({ type: 'text' })
  flowData: string
}
```

## Request Flow Example

```
POST /api/v1/chatflows
  ↓
[Middleware Pipeline]
  ↓
routes/chatflows/index.ts
  ↓
controllers/chatflows/index.ts
  ↓
services/chatflows/index.ts
  ↓
database/entities/ChatFlow.ts
  ↓
PostgreSQL Database
  ↓
Response: { id, name, ... }
```

## Error Handling

Controllers catch errors and format responses:

```typescript
try {
  const result = await service.method()
  return res.json(result)
} catch (error) {
  logger.error(error)
  return res.status(500).json({
    error: error.message
  })
}
```

Global error handler:

```typescript
app.use((err, req, res, next) => {
  logger.error(err)
  res.status(err.statusCode || 500).json({
    error: err.message
  })
})
```

## Separation of Concerns

**Routes**: HTTP layer
**Controllers**: Request/Response handling
**Services**: Business logic
**Database**: Data persistence

Each layer has single responsibility and clear boundaries.

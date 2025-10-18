# Core Database Entities

**ORM**: TypeORM
**Location**: `packages/server/src/database/entities/`

## ChatFlow

Flow/workflow configuration.

```typescript
@Entity()
export class ChatFlow {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  name: string

  @Column({ type: 'text' })
  flowData: string              // JSON: Node graph

  @Column({ nullable: true })
  deployed: boolean

  @Column({ nullable: true })
  isPublic: boolean

  @Column({ nullable: true, type: 'text' })
  chatbotConfig: string         // JSON: UI config

  @Column({ type: 'varchar', length: 20 })
  type: ChatflowType            // CHATFLOW | AGENTFLOW | MULTIAGENT

  @Column({ nullable: true, type: 'text' })
  workspaceId: string

  @CreateDateColumn()
  createdDate: Date

  @UpdateDateColumn()
  updatedDate: Date
}
```

## ChatMessage

Conversation messages.

```typescript
@Entity()
export class ChatMessage {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  role: MessageType             // user | assistant | system

  @Index()
  @Column({ type: 'uuid' })
  chatflowid: string

  @Column({ type: 'text' })
  content: string

  @Column({ nullable: true, type: 'text' })
  sourceDocuments: string       // JSON: Retrieved docs

  @Column({ nullable: true, type: 'text' })
  usedTools: string             // JSON: Tools used

  @Column()
  chatType: string

  @Column({ type: 'varchar' })
  chatId: string                // Session ID

  @Column({ nullable: true, type: 'varchar' })
  sessionId: string

  @CreateDateColumn()
  createdDate: Date
}
```

## Credential

Encrypted API keys.

```typescript
@Entity()
export class Credential {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  name: string                  // Display name

  @Column()
  credentialName: string        // Type: openAIApi, etc.

  @Column({ type: 'text' })
  encryptedData: string         // AES-256-GCM encrypted

  @Column({ nullable: true, type: 'text' })
  workspaceId: string

  @CreateDateColumn()
  createdDate: Date

  @UpdateDateColumn()
  updatedDate: Date
}
```

## Tool

Custom tools for agents.

```typescript
@Entity()
export class Tool {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  name: string

  @Column({ type: 'text' })
  description: string

  @Column({ type: 'text' })
  schema: string                // JSON: Input schema

  @Column({ type: 'text' })
  func: string                  // JavaScript function

  @Column({ nullable: true })
  iconSrc: string

  @CreateDateColumn()
  createdDate: Date
}
```

## Variable

Global variables.

```typescript
@Entity()
export class Variable {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  name: string

  @Column({ type: 'text' })
  value: string

  @Column()
  type: string                  // string | number | json

  @CreateDateColumn()
  createdDate: Date
}
```

## Supported Databases

- PostgreSQL (recommended)
- MySQL/MariaDB
- SQLite (default, development)

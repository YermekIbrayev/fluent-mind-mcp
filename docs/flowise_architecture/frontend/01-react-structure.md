# Frontend React Structure

**Package**: `packages/ui`
**Tech**: React 18 + Material-UI v5 + Vite

## Directory Structure

```
packages/ui/src/
├── App.jsx              # Root component
├── index.jsx            # Entry point
├── views/               # Page components
├── ui-component/        # Reusable components
├── layout/              # Layout templates
├── store/               # Redux store
├── api/                 # API client
├── routes/              # Route definitions
├── themes/              # MUI theme
└── hooks/               # Custom hooks
```

## Entry Point

```jsx
// index.jsx
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import store from './store'

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
)
```

## App Component

```jsx
// App.jsx
import { ThemeProvider } from '@mui/material/styles'
import { CssBaseline } from '@mui/material'
import Routes from './routes'
import themes from './themes'

const App = () => {
  const customization = useSelector((state) => state.customization)

  return (
    <ThemeProvider theme={themes(customization)}>
      <CssBaseline />
      <NavigationScroll>
        <Routes />
      </NavigationScroll>
    </ThemeProvider>
  )
}
```

## Key Views

**Location**: `src/views/`

- `chatflows/` - Flow management
- `canvas/` - Flow editor (ReactFlow)
- `chatbot/` - Chat interface
- `credentials/` - Credential management
- `assistants/` - OpenAI Assistants
- `agentflowsv2/` - Agent workflows
- `tools/` - Tool management
- `variables/` - Variable management
- `apikey/` - API key management

## UI Components

**Location**: `src/ui-component/`

- `button/` - Custom buttons
- `dialog/` - Modal dialogs
- `input/` - Form inputs
- `table/` - Data tables
- `editor/` - Code editors
- `json/` - JSON viewers
- `markdown/` - Markdown renderers

## Layouts

**MainLayout**: Sidebar + header + content
**MinimalLayout**: Simple header + content
**AuthLayout**: Centered form

## API Client

**Location**: `src/api/`

```javascript
// api/chatflows.js
import axios from 'axios'

export const getAllChatflows = async () => {
  const { data } = await axios.get('/api/v1/chatflows')
  return data
}

export const createChatflow = async (body) => {
  const { data } = await axios.post('/api/v1/chatflows', body)
  return data
}
```

## Build Tool

**Vite**: Fast HMR, production builds
**Output**: `packages/ui/build/`

```bash
pnpm dev      # Dev server on port 8080
pnpm build    # Production build
```

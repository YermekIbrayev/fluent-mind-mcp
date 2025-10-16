# Chrome DevTools

**Category**: DevTools | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Browser automation, testing, performance analysis, and debugging.

---

## Capabilities

**Page Management**: Navigate, open, close, select pages
**Interaction**: Click, fill, hover, drag, upload
**Inspection**: Snapshots, screenshots, JavaScript execution
**Network & Console**: Request analysis, console logs
**Performance**: Trace recording and analysis
**Emulation**: Network throttling, CPU throttling, viewport resizing

---

## Key Function Groups

### Page Management

- `list_pages` - List all open pages
- `select_page` - Switch context to page by index
- `new_page` - Open new page with URL
- `close_page` - Close page by index (can't close last page)
- `navigate_page` - Go to URL
- `navigate_page_history` - Back/forward navigation

### Interaction

- `click` - Click element by UID (supports double-click)
- `fill` - Type into input/select by UID
- `fill_form` - Fill multiple form fields at once
- `hover` - Hover over element by UID
- `drag` - Drag element to another element
- `upload_file` - Upload file through input
- `handle_dialog` - Accept/dismiss browser dialogs

### Inspection

- `take_snapshot` - Text snapshot with UIDs (preferred over screenshot)
- `take_screenshot` - Visual screenshot (full page or element)
- `evaluate_script` - Execute JavaScript, returns JSON-serializable result

### Network & Console

- `list_network_requests` - View network activity (with pagination, filters)
- `get_network_request` - Get specific request details
- `list_console_messages` - View console logs since last navigation

### Performance

- `performance_start_trace` - Start recording (with optional reload, auto-stop)
- `performance_stop_trace` - Stop recording and analyze
- `performance_analyze_insight` - Deep dive into specific insight

### Emulation

- `emulate_network` - Throttle network (Offline, Slow 3G, Fast 3G, Slow 4G, Fast 4G)
- `emulate_cpu` - Throttle CPU (1-20x slowdown)
- `resize_page` - Change viewport dimensions

---

## Common Workflows

**UI Testing**:
```
1. new_page with URL
2. take_snapshot to see elements with UIDs
3. click/fill elements by UID
4. take_screenshot to verify
```

**Performance Analysis**:
```
1. performance_start_trace(reload: true, autoStop: true)
2. Review Core Web Vitals
3. performance_analyze_insight for details
4. Optimize based on findings
```

**Network Debugging**:
```
1. list_network_requests (filter by type)
2. get_network_request for details
3. Check status codes, timing, payload
```

**Cross-Device Testing**:
```
1. resize_page to mobile dimensions
2. emulate_network to Slow 3G
3. Test user flows
4. take_screenshot for documentation
```

---

## Best Practices

- **Always use take_snapshot** before interactions (get UIDs)
- Prefer snapshots over screenshots (more efficient)
- Use full page screenshots for documentation only
- Filter network requests by resource type for performance
- Set appropriate timeouts for slow operations
- Remember: last page cannot be closed

---

## Related

- [Workflows](../workflows.md) - Testing workflow integration

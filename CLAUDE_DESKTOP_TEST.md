# Claude Desktop Integration Test Checklist

**Date**: 2025-10-17
**Task**: T122 - Test Claude Desktop integration
**Status**: Configuration created, manual testing required

---

## ✅ Automated Pre-Testing (COMPLETE)

- ✅ **MCP Server starts**: Server initializes successfully
- ✅ **All 8 tools registered**: list_chatflows, get_chatflow, run_prediction, create_chatflow, update_chatflow, deploy_chatflow, delete_chatflow, generate_agentflow_v2
- ✅ **Configuration created**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- ✅ **Flowise connection**: Connected to http://192.168.51.32:3000 (88 chatflows available)

---

## 🔄 Manual Testing Steps

### Step 1: Restart Claude Desktop

1. **Quit Claude Desktop completely** (⌘Q or Quit from menu)
2. **Wait 5 seconds** for process to fully terminate
3. **Relaunch Claude Desktop**
4. **Wait 10 seconds** for MCP server initialization

**Expected**: Claude Desktop starts without errors

---

### Step 2: Verify MCP Server Connection

In Claude Desktop, type:
```
What MCP servers are connected?
```

**Expected response**: Should mention "fluent-mind" server with 8 tools

**Alternative verification**: Check Claude Desktop logs
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

---

### Step 3: Test Each Tool

#### Tool 1: list_chatflows

**Test command**:
```
List my Flowise chatflows
```

**Expected**:
- Returns list of chatflows with names, types, deployment status
- Should show ~88 chatflows from http://192.168.51.32:3000
- Response time <5 seconds

**Verification**: ✅ Pass / ❌ Fail

---

#### Tool 2: get_chatflow

**Test command** (use an actual chatflow ID from list):
```
Get details for chatflow [CHATFLOW_ID]
```

**Expected**:
- Returns complete chatflow details
- Includes workflow structure (nodes, edges)
- Response time <5 seconds

**Verification**: ✅ Pass / ❌ Fail

---

#### Tool 3: run_prediction

**Test command** (use a deployed chatflow ID):
```
Run chatflow [CHATFLOW_ID] with question "What is AI?"
```

**Expected**:
- Executes chatflow and returns response
- Response includes text from chatflow
- Response time <5 seconds (varies by chatflow complexity)

**Verification**: ✅ Pass / ❌ Fail

---

#### Tool 4: create_chatflow

**Test command**:
```
Create a new Flowise chatflow named "Test Flow" with this structure:
{
  "nodes": [
    {"id": "start", "type": "chatOpenAI", "data": {"model": "gpt-4"}, "position": {"x": 100, "y": 100}}
  ],
  "edges": []
}
```

**Expected**:
- Creates new chatflow
- Returns chatflow ID
- Chatflow appears in Flowise UI
- Response time <10 seconds

**Verification**: ✅ Pass / ❌ Fail

---

#### Tool 5: update_chatflow

**Test command** (use chatflow ID from create test):
```
Update chatflow [CHATFLOW_ID] to set name to "Updated Test Flow"
```

**Expected**:
- Updates chatflow name
- Returns updated chatflow details
- Change visible in Flowise UI
- Response time <10 seconds

**Verification**: ✅ Pass / ❌ Fail

---

#### Tool 6: deploy_chatflow

**Test command** (use chatflow ID from create test):
```
Deploy chatflow [CHATFLOW_ID]
```

**Expected**:
- Sets deployed=true
- Chatflow becomes available for execution
- Response time <10 seconds

**Verification**: ✅ Pass / ❌ Fail

---

#### Tool 7: delete_chatflow

**Test command** (use chatflow ID from create test):
```
Delete chatflow [CHATFLOW_ID]
```

**Expected**:
- Deletes chatflow permanently
- Chatflow no longer in list
- Response time <10 seconds

**Verification**: ✅ Pass / ❌ Fail

---

#### Tool 8: generate_agentflow_v2

**Test command**:
```
Generate an AgentFlow V2 for a research agent that searches the web and summarizes findings
```

**Expected**:
- Generates AgentFlow V2 structure
- Returns flowData with nodes and edges
- Structure is valid for chatflow creation
- Response time <10 seconds

**Verification**: ✅ Pass / ❌ Fail

**Note**: This tool may fail with 500 error if Flowise API is not properly configured for AgentFlow generation

---

## 📋 Complete Workflow Test

### End-to-End Scenario

1. **Generate** an AgentFlow V2 structure
2. **Create** a chatflow from the generated structure
3. **List** chatflows and verify the new one appears
4. **Get** details of the created chatflow
5. **Update** the chatflow name
6. **Deploy** the chatflow
7. **Execute** the deployed chatflow with a test question
8. **Undeploy** the chatflow
9. **Delete** the chatflow
10. **List** chatflows and verify it's gone

**Expected**: All operations succeed in sequence, demonstrating full lifecycle management

**Verification**: ✅ Pass / ❌ Fail

---

## 🐛 Troubleshooting

### Issue: MCP server not found in Claude Desktop

**Solutions**:
1. Verify config file exists: `cat ~/Library/Application\ Support/Claude/claude_desktop_config.json`
2. Check JSON syntax is valid
3. Restart Claude Desktop (full quit and relaunch)
4. Check logs: `tail -f ~/Library/Logs/Claude/mcp*.log`

### Issue: "Connection refused" errors

**Solutions**:
1. Verify Flowise is running: `curl http://192.168.51.32:3000/api/v1/chatflows`
2. Check FLOWISE_API_URL is correct in config
3. Verify network connectivity

### Issue: "Authentication failed" errors

**Solutions**:
1. Verify API key is correct in config
2. Check Flowise instance security settings
3. Test with curl: `curl -H "Authorization: Bearer [KEY]" http://192.168.51.32:3000/api/v1/chatflows`

### Issue: Tools are slow or timeout

**Solutions**:
1. Check network latency to Flowise instance
2. Verify Flowise instance is not overloaded
3. Check for large chatflows that may slow down list operations

---

## ✅ Test Summary

**Date**: _________________
**Tested by**: _________________

**Results**:
- [ ] All 8 tools verified
- [ ] End-to-end workflow completed
- [ ] Performance acceptable (<5s list/get/execute, <10s create/update/delete)
- [ ] Error handling appropriate
- [ ] Logs show no errors

**Overall Status**: ⬜ PASS / ⬜ FAIL

**Notes**:
```
[Add any observations, issues, or comments here]
```

---

## 📝 Post-Testing Actions

- [ ] Update tasks.md with test results
- [ ] File issues for any failures
- [ ] Document any limitations discovered
- [ ] Update README.md with usage examples
- [ ] Consider creating video demo

---

**Configuration File**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Log Files**: `~/Library/Logs/Claude/mcp*.log`
**Test Script**: `test_mcp_tools.py` (automated pre-check)

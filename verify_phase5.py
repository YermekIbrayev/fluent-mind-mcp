#!/usr/bin/env python3
"""Phase 5 Verification Script - User Story 3: Update and Deploy Chatflows

This script demonstrates and verifies the update_chatflow and deploy_chatflow
functionality by running 3 different test cases:
1. Update chatflow name only
2. Toggle deployment status using deploy_chatflow
3. Update multiple fields (name + deployed) simultaneously
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fluent_mind_mcp.models.config import FlowiseConfig
from fluent_mind_mcp.models.chatflow import ChatflowType
from fluent_mind_mcp.server import MCPServer


# Simple test flowData structure
SIMPLE_FLOW_DATA = {
    "nodes": [
        {
            "id": "llm-1",
            "type": "chatOpenAI",
            "data": {
                "label": "ChatOpenAI",
                "name": "chatOpenAI",
                "version": 1.0,
                "type": "ChatOpenAI",
                "category": "Chat Models",
                "inputs": {
                    "modelName": "gpt-3.5-turbo",
                    "temperature": 0.7,
                    "streaming": True
                },
                "outputs": {
                    "output": "ChatOpenAI"
                }
            },
            "position": {"x": 250, "y": 100}
        }
    ],
    "edges": []
}


def print_separator(title: str):
    """Print a formatted separator for test sections."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_chatflow_info(chatflow: dict, title: str):
    """Print formatted chatflow information."""
    print(f"{title}:")
    print(f"  ID: {chatflow['id']}")
    print(f"  Name: {chatflow['name']}")
    print(f"  Type: {chatflow['type']}")
    print(f"  Deployed: {chatflow['deployed']}")
    print(f"  Created: {chatflow.get('createdDate', 'N/A')}")
    print(f"  Updated: {chatflow.get('updatedDate', 'N/A')}")


async def main():
    """Run Phase 5 verification tests."""

    print_separator("Phase 5 Verification - User Story 3: Update and Deploy Chatflows")

    # Initialize MCP Server
    config = FlowiseConfig.from_env()
    server = MCPServer(config)

    print(f"Connected to Flowise: {config.api_url}")
    print(f"Timeout: {config.timeout}s")
    print(f"Max connections: {config.max_connections}\n")

    chatflow_id = None

    try:
        # ====================================================================
        # SETUP: Create a test chatflow
        # ====================================================================
        print_separator("SETUP: Create Test Chatflow")

        flow_data_json = json.dumps(SIMPLE_FLOW_DATA)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        created_chatflow = await server.create_chatflow(
            name=f"Phase5_Test_{timestamp}",
            flow_data=flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created_chatflow['id']
        print_chatflow_info(created_chatflow, "✓ Created Test Chatflow")


        # ====================================================================
        # TEST 1: Update chatflow name only
        # ====================================================================
        print_separator("TEST 1: Update Chatflow Name Only")

        print("Updating name from '{}' to 'Phase5_Test_Updated_{}'...".format(
            created_chatflow['name'],
            timestamp
        ))

        updated_chatflow = await server.update_chatflow(
            chatflow_id=chatflow_id,
            name=f"Phase5_Test_Updated_{timestamp}"
        )

        print_chatflow_info(updated_chatflow, "✓ Updated Chatflow")

        # Verify only name changed
        assert updated_chatflow['name'] == f"Phase5_Test_Updated_{timestamp}", \
            "Name should be updated"
        assert updated_chatflow['deployed'] == created_chatflow['deployed'], \
            "Deployed status should not change"
        assert updated_chatflow['id'] == chatflow_id, \
            "ID should remain the same"

        print("✓ Verification: Name updated successfully, other fields unchanged")


        # ====================================================================
        # TEST 2: Toggle deployment using deploy_chatflow
        # ====================================================================
        print_separator("TEST 2: Toggle Deployment Status Using deploy_chatflow")

        print(f"Current deployed status: {updated_chatflow['deployed']}")
        print("Deploying chatflow using deploy_chatflow(deployed=True)...")

        deployed_chatflow = await server.deploy_chatflow(
            chatflow_id=chatflow_id,
            deployed=True
        )

        print_chatflow_info(deployed_chatflow, "✓ Deployed Chatflow")

        # Verify deployment changed
        assert deployed_chatflow['deployed'] is True, \
            "Chatflow should be deployed"
        assert deployed_chatflow['name'] == updated_chatflow['name'], \
            "Name should not change"
        assert deployed_chatflow['id'] == chatflow_id, \
            "ID should remain the same"

        print("✓ Verification: Deployment status changed, other fields unchanged")

        # Now undeploy it
        print("\nUndeploying chatflow using deploy_chatflow(deployed=False)...")

        undeployed_chatflow = await server.deploy_chatflow(
            chatflow_id=chatflow_id,
            deployed=False
        )

        print_chatflow_info(undeployed_chatflow, "✓ Undeployed Chatflow")

        assert undeployed_chatflow['deployed'] is False, \
            "Chatflow should be undeployed"

        print("✓ Verification: Successfully toggled deployment on and off")


        # ====================================================================
        # TEST 3: Update multiple fields simultaneously
        # ====================================================================
        print_separator("TEST 3: Update Multiple Fields (name + deployed)")

        new_name = f"Phase5_Test_MultiUpdate_{timestamp}"
        print(f"Updating name to '{new_name}' AND deploying simultaneously...")

        multi_updated_chatflow = await server.update_chatflow(
            chatflow_id=chatflow_id,
            name=new_name,
            deployed=True
        )

        print_chatflow_info(multi_updated_chatflow, "✓ Multi-Updated Chatflow")

        # Verify both changes
        assert multi_updated_chatflow['name'] == new_name, \
            "Name should be updated"
        assert multi_updated_chatflow['deployed'] is True, \
            "Chatflow should be deployed"
        assert multi_updated_chatflow['id'] == chatflow_id, \
            "ID should remain the same"

        print("✓ Verification: Both name and deployment status updated successfully")


        # ====================================================================
        # VERIFICATION SUMMARY
        # ====================================================================
        print_separator("VERIFICATION SUMMARY")

        # Fetch final state from Flowise
        final_chatflow = await server.get_chatflow(chatflow_id)

        print("Final Chatflow State:")
        print_chatflow_info(final_chatflow, "  Current State")

        print("\n✓ All Phase 5 Tests Passed!")
        print("\nCovered Test Cases:")
        print("  1. ✓ Update name only (partial update)")
        print("  2. ✓ Toggle deployment on/off using deploy_chatflow")
        print("  3. ✓ Update multiple fields simultaneously")
        print("\nPhase 5 (User Story 3) verification SUCCESSFUL!")

    except Exception as e:
        print(f"\n✗ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # ====================================================================
        # CLEANUP: Delete test chatflow
        # ====================================================================
        if chatflow_id:
            print_separator("CLEANUP: Delete Test Chatflow")

            try:
                # Note: delete functionality is Phase 6 (User Story 4)
                # For now, we'll leave the test chatflow but note its ID
                print(f"Test chatflow ID: {chatflow_id}")
                print(f"Name: {final_chatflow['name']}")
                print("\nNote: Delete functionality is part of Phase 6 (User Story 4)")
                print("You can manually delete this chatflow from Flowise UI if needed")
            except Exception as e:
                print(f"Cleanup note: {e}")

        # Close HTTP connections
        await server.close()
        print("\n✓ Closed server connections")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

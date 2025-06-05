from typing import Any, List, Optional
import httpx
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("openregister")

# Constants
OPENREGISTER_API_BASE = os.getenv("OPENREGISTER_API_URL", "https://api.openregister.de/v0")
API_KEY = os.getenv("OPENREGISTER_API_KEY")

async def make_openregister_request(url: str, params: Optional[dict] = None) -> dict[str, Any] | None:
    """Make a request to the OpenRegister API with proper error handling."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

@mcp.tool()
async def search_companies(
    query: Optional[str] = None,
    register_number: Optional[str] = None,
    register_type: Optional[str] = None,
    register_court: Optional[str] = None,
    active: bool = True,
    legal_form: Optional[str] = None
) -> dict[str, Any]:
    """Search for companies based on various criteria.

    Args:
        query: Text search query to find companies by name (e.g., "Descartes Technologies UG")
        register_number: Company register number for exact matching (e.g., "230633")
        register_type: Type of register to filter results (e.g., "HRB", "HRA", "PR", "GnR", "VR")
        register_court: Court where the company is registered (e.g., "Berlin (Charlottenburg)")
        active: Filter for active or inactive companies (default: true)
        legal_form: Legal form of the company (e.g., "gmbh", "ag", "ug")
    """
    search_url = f"{OPENREGISTER_API_BASE}/search/company"
    
    # Build query parameters, excluding None values
    params = {}
    if query:
        params["query"] = query
    if register_number:
        params["register_number"] = register_number
    if register_type:
        params["register_type"] = register_type
    if register_court:
        params["register_court"] = register_court
    if active is not None:
        params["active"] = str(active).lower()
    if legal_form:
        params["legal_form"] = legal_form
    
    # Make the API request
    response_data = await make_openregister_request(search_url, params)
    
    if not response_data:
        return {"error": "Unable to fetch company data."}
    
    return response_data

@mcp.tool()
async def get_company_info(
    company_id: str,
    history: bool = True,
    financials: bool = True,
    documents: bool = True
) -> dict[str, Any]:
    """Get detailed information about a company using its unique ID.

    Args:
        company_id: Unique company identifier (e.g., "DE-HRB-F1103-267645")
        history: Include historical company data when set to true
        financials: Include financial data when set to true
        documents: Include document metadata when set to true
    """
    company_url = f"{OPENREGISTER_API_BASE}/company/{company_id}"
    
    # Build query parameters
    params = {
        "history": str(history).lower(),
        "financials": str(financials).lower(),
        "documents": str(documents).lower()
    }
    
    # Make the API request
    company_data = await make_openregister_request(company_url, params)
    
    if not company_data:
        return {"error": f"Unable to fetch information for company ID: {company_id}"}
    
    return company_data

@mcp.tool()
async def get_company_shareholders(
    company_id: str
) -> dict[str, Any]:
    """Retrieve the shareholders of a company.
    
    Args:
        company_id: Unique company identifier (e.g., "DE-HRB-F1103-267645")
    
    Note:
        This endpoint currently only supports companies with the legal form GmbH.
        The request can take up to 60 seconds to complete.
    """
    shareholders_url = f"{OPENREGISTER_API_BASE}/company/{company_id}/shareholders"
    
    # Make the API request
    shareholders_data = await make_openregister_request(shareholders_url)
    
    if not shareholders_data:
        return {"error": f"Unable to fetch shareholders for company ID: {company_id}"}
    
    return shareholders_data

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

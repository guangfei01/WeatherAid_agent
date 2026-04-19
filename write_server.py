from mcp.server.fastmcp import FastMCP

mcp = FastMCP("writeServer")

@mcp.tool()
async def write_to_file(filename: str, content: str) -> str:
    """
    Write content to a file.
    :param filename: name of the file to write to (e.g., "output.txt")
    :param content: the text content to write into the file
    :return: success or error message
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to '{filename}'."
    except Exception as e:
        return f"Error writing to file: {str(e)}"

@mcp.tool()
async def append_to_file(filename: str, content: str) -> str:
    """
    Append content to an existing file, or create it if it doesn't exist.
    :param filename: name of the file to append to
    :param content: the text content to append
    :return: success or error message
    """
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Successfully appended to '{filename}'."
    except Exception as e:
        return f"Error appending to file: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
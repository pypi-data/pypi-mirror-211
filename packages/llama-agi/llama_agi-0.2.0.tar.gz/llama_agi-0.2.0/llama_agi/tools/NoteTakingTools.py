from langchain.agents import tool
from llama_index import Document
from llama_agi.utils import initialize_search_index

note_index = initialize_search_index([])


@tool("Record Note")
def record_note(note: str) -> str:
    """Useful for when you need to record a note or reminder for yourself to reference in the future."""
    global note_index
    note_index.insert(Document(note))
    return "Note successfully recorded."


@tool("Search Notes")
def search_notes(query_str: str) -> str:
    """Useful for searching through notes that you previously recorded."""
    global note_index
    response = note_index.as_query_engine(
        similarity_top_k=3,
    ).query(query_str)
    return str(response)

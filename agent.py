from typing import Optional

def extract_proof(text: str) -> Optional[str]:
    """ Extract the proof from the agent's response. """
    text_split = text.split("<proof>", maxsplit=1)
    if len(text_split) <= 1:
        return None
    else:
        text_end = text_split[1]
        text_end_split = text_end.split("</proof>", maxsplit=1)
        if len(text_end_split) <= 1:
            return None
        else:
            proof = text_end_split[0]
            return proof.strip()

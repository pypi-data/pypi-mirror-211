from typing import Any, Dict, Optional

from spacy.language import Language

from .lymphoma import Lymphoma

DEFAULT_CONFIG = dict(patterns=None)


@Language.factory(
    "eds.lymphoma",
    default_config=DEFAULT_CONFIG,
    assigns=["doc.ents", "doc.spans"],
)
def create_component(
    nlp: Language,
    name: str,
    patterns: Optional[Dict[str, Any]],
):
    return Lymphoma(nlp, patterns=patterns)

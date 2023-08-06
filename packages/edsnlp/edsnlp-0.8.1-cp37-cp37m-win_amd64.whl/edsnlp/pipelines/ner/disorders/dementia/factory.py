from typing import Any, Dict, Optional

from spacy.language import Language

from .dementia import Dementia

DEFAULT_CONFIG = dict(patterns=None)


@Language.factory(
    "eds.dementia",
    default_config=DEFAULT_CONFIG,
    assigns=["doc.ents", "doc.spans"],
)
def create_component(
    nlp: Language,
    name: str,
    patterns: Optional[Dict[str, Any]],
):
    return Dementia(nlp, patterns=patterns)

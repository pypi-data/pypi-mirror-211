from typing import Any, Dict, Optional

from spacy.language import Language

from .congestive_heart_failure import CongestiveHeartFailure

DEFAULT_CONFIG = dict(patterns=None)


@Language.factory(
    "eds.congestive_heart_failure",
    default_config=DEFAULT_CONFIG,
    assigns=["doc.ents", "doc.spans"],
)
def create_component(
    nlp: Language,
    name: str,
    patterns: Optional[Dict[str, Any]],
):
    return CongestiveHeartFailure(nlp, patterns=patterns)

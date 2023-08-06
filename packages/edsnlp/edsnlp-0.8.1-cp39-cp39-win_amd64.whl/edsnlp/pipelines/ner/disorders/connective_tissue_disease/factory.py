from typing import Any, Dict, Optional

from spacy.language import Language

from .connective_tissue_disease import ConnectiveTissueDisease

DEFAULT_CONFIG = dict(patterns=None)


@Language.factory(
    "eds.connective_tissue_disease",
    default_config=DEFAULT_CONFIG,
    assigns=["doc.ents", "doc.spans"],
)
def create_component(
    nlp: Language,
    name: str,
    patterns: Optional[Dict[str, Any]],
):
    return ConnectiveTissueDisease(nlp, patterns=patterns)

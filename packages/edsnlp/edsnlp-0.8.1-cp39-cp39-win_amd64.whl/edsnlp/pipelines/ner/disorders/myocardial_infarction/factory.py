from typing import Any, Dict, Optional

from spacy.language import Language

from .myocardial_infarction import MyocardialInfarction

DEFAULT_CONFIG = dict(patterns=None)


@Language.factory(
    "eds.myocardial_infarction",
    default_config=DEFAULT_CONFIG,
    assigns=["doc.ents", "doc.spans"],
)
def create_component(
    nlp: Language,
    name: str,
    patterns: Optional[Dict[str, Any]],
):
    return MyocardialInfarction(nlp, patterns=patterns)

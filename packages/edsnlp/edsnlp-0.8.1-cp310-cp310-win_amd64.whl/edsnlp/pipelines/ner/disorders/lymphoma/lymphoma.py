"""`eds.lymphoma` pipeline"""
from edsnlp.pipelines.ner.disorders.base import DisorderMatcher

from .patterns import default_patterns


class Lymphoma(DisorderMatcher):
    def __init__(self, nlp, patterns):

        self.nlp = nlp
        if patterns is None:
            patterns = default_patterns

        super().__init__(
            nlp=nlp,
            name="lymphoma",
            patterns=patterns,
        )

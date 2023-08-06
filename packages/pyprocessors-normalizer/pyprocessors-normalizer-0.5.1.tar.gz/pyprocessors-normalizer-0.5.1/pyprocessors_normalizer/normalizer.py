from collections import defaultdict
from enum import Enum
from functools import reduce
from itertools import groupby
from typing import List, Type, cast

from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Annotation, Document, AltText

from .normalizers import (
    CleanText,
    CleanDate,
    NormalizeDate,
    CleanAmount,
    NormalizeAmount,
    NormalizeForme, CleanForme,
)
from .reducers import Deduplicate, FuzzyDeduplicate, MostRecent


class OutputFormat(str, Enum):
    xlsx = "xlsx"


class NormalizerParameters(ProcessorParameters):
    format: OutputFormat = Field(OutputFormat.xlsx, description="Output format")
    as_altText: str = Field(
        "slots",
        description="""If defined generate the slots as an alternative text of the input document,
    if not replace the text of the input document.""",
    )


def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def compose_functions(functions):
    composed_fun = (
        compose(*reversed(functions)) if isinstance(functions, List) else functions
    )
    return composed_fun


Normalizers = {
    "NOM_ATTRIBUE": [
        CleanText,
    ],
    "DENOMINATION": [
        CleanText,
    ],
    "ADRESSE_SIEGE": [
        CleanText,
    ],
    "FAIT_LE": [
        CleanDate,
        NormalizeDate,
    ],
    "MIS_A_JOUR": [
        CleanDate,
        NormalizeDate,
    ],
    "NOMBRE_ACTIONS": [CleanAmount, NormalizeAmount],
    "FORME": [CleanForme, NormalizeForme],
}

Reducers = {
    "NOM_ATTRIBUE": FuzzyDeduplicate,
    "DENOMINATION": FuzzyDeduplicate,
    "ADRESSE_SIEGE": FuzzyDeduplicate,
    "FAIT_LE": [Deduplicate, MostRecent],
    "MIS_A_JOUR": [Deduplicate, MostRecent],
    "NOMBRE_ACTIONS": Deduplicate,
    "FORME": Deduplicate
}


class NormalizerProcessor(ProcessorBase):
    """Mazars normalizer."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: NormalizerParameters = cast(NormalizerParameters, parameters)
        try:
            for document in documents:
                slots = []
                filtered_annotations = [
                    a
                    for a in document.annotations
                    if a.label in Normalizers.keys() and a.status != "KO"
                ]
                document.annotations = filtered_annotations
                ann_groups = group_annotations(document, by_label)
                for group, anns in ann_groups.items():
                    if group in Normalizers:
                        normalizer_fun = compose_functions(Normalizers[group])
                        for a in anns:
                            text = a.text
                            a.properties = a.properties or {}
                            a.properties["normalized"] = normalizer_fun(text)
                ann_groups["Dated'Effet"] = ann_groups.pop(
                    "Dated'Effet (date)", None
                ) or ann_groups.pop("Dated'Effet (en lettre)", [])
                ann_groups["DépôtdeGarantie"] = ann_groups.pop("DépôtdeGarantie", [])
                if "DépôtdeGarantie (en lettre)" in ann_groups:
                    ann_groups["DépôtdeGarantie"].extend(
                        ann_groups.pop("DépôtdeGarantie (en lettre)")
                    )
                ann_groups["Franchise"] = ann_groups.pop(
                    "Franchise (en mois)", None
                ) or ann_groups.pop("Franchise (chiffre)", [])
                for col, reducers in Reducers.items():
                    reducer_fun = compose_functions(reducers)
                    anns = ann_groups.get(col, [])
                    texts = [a.properties["normalized"] for a in anns]
                    dedups = reducer_fun(texts)
                    slots.append(f"{col} : {' | '.join(dedups)}")
                slot = "\n".join(slots)
                if params.as_altText is not None and len(params.as_altText):
                    document.altTexts = document.altTexts or []
                    altTexts = [
                        alt
                        for alt in document.altTexts
                        if alt.name != params.as_altText
                    ]
                    altTexts.append(AltText(name=params.as_altText, text=slot))
                    document.altTexts = altTexts
                else:
                    document.text = slot
                    document.annotations = None
                    document.sentences = None
        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return NormalizerParameters


def group_annotations(doc: Document, keyfunc):
    def get_sort_key(a: Annotation):
        return a.end - a.start, -a.start

    groups = defaultdict(list)
    for k, g in groupby(sorted(doc.annotations, key=keyfunc), keyfunc):
        sorted_group = sorted(g, key=get_sort_key, reverse=True)
        groups[k] = sorted_group
    return groups


def by_label(a: Annotation):
    return a.label

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

class LanguageStatus(str,Enum):
    RESTORED="RESTORED"; CANONICAL="CANONICAL"; PROPOSED="PROPOSED"

@dataclass(frozen=True)
class NativeLanguage:
    language_id:str; name:str; purpose:str; syntax:str; semantics:str; types:tuple[str,...]
    state:str; events:str; contracts:str; compiler:str; ir:str; runtime_binding:str
    verification:str; boundaries:tuple[str,...]; differences:tuple[str,...]; examples:tuple[str,...]
    status:LanguageStatus
    def specification(self): return {k:v.value if isinstance(v,Enum) else (list(v) if isinstance(v,tuple) else v)
        for k,v in self.__dict__.items()}

class NativeLanguageRegistry:
    def __init__(self): self._languages={}
    def register(self,language):
        if language.language_id in self._languages: raise ValueError("duplicate language")
        self._languages[language.language_id]=language
    def get(self,language_id): return self._languages[language_id]
    def all(self): return tuple(self._languages[k] for k in sorted(self._languages))
    def compile_boundary(self,language_id,source,translator:Callable[[str],Any]):
        if not source.strip(): raise ValueError("source cannot be empty")
        return translator(source)

def proposed_nxl_registry():
    r=NativeLanguageRegistry()
    specs=(("NXL-S","Semantic","meaning and truth claims"),("NXL-SYS","System","system declarations"),
    ("NXL-ARCH","Architecture","architecture candidates"),("NXL-CON","Contract","pre/postconditions and invariants"),
    ("NXL-PROOF","Proof","proof obligations and evidence"),("NXL-EXEC","Execution","authorized execution"),
    ("NXL-EVO","Evolution","bounded mutations"),("NXL-Q","Query","relation and evidence queries"),
    ("NXL-VIS","Visual","model-derived visual declarations"))
    for lid,name,purpose in specs:
        r.register(NativeLanguage(lid,name,purpose,"PROPOSED grammar; versioned before implementation.",
        "PROPOSED semantic layer.",("Entity","Reference","Constraint","Expression","Artifact"),
        "explicit state declarations","typed ledger events","preconditions/postconditions/invariants",
        "NEXENT compiler boundary","NEXENT UIR","explicit runtime adapter","syntax + semantic + contract + evidence",
        ("not a host-language replacement","syntax alone grants no execution"),("meaning precedes implementation","host runtime is not truth"),
        (lid+" :: DECLARE ...",),LanguageStatus.PROPOSED))
    return r

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import hashlib,json,uuid
class RecordKind(str,Enum):
    INPUT="INPUT"; COMPUTATION="COMPUTATION"; PHYSICAL_STATE="PHYSICAL_STATE"; SOFTWARE_STATE="SOFTWARE_STATE"; OBSERVATION="OBSERVATION"; EVIDENCE="EVIDENCE"
@dataclass(frozen=True)
class OperationalRecord:
    kind: RecordKind; payload: dict; source: str
    id: str=field(default_factory=lambda:"OR-"+uuid.uuid4().hex)
    created_at: str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    schema_version: int=1
    @property
    def digest(self):
        body=json.dumps({"id":self.id,"kind":self.kind.value,"payload":self.payload,"source":self.source,"created_at":self.created_at,"schema_version":self.schema_version},sort_keys=True,separators=(",",":"),default=str)
        return hashlib.sha256(body.encode()).hexdigest()

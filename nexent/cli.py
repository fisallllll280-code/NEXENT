import argparse, json
from .kernel import NexentKernel
from .model import Capability, EntitySpec, Intent
from .dsl import NexentDSL

def build_demo() -> NexentKernel:
    k=NexentKernel()
    k.register_entity(EntitySpec("nexent.kernel","kernel","core",("execute","govern","prove"),()))
    k.register_entity(EntitySpec("nexent.ledger","ledger","evidence",("ledger",),("nexent.kernel",)))
    k.register_capability(Capability("echo","1.0","deterministic echo",lambda p:{"echo":p}))
    return k

def main() -> None:
    p=argparse.ArgumentParser(prog="nexent")
    p.add_argument("command",choices=["demo","status","run"])
    p.add_argument("--intent")
    a=p.parse_args()
    k=build_demo()
    if a.command=="status":
        print(json.dumps(k.status(),indent=2)); return
    if a.command=="demo":
        r=k.execute(Intent("demo","CLI","demo","echo",{"message":"NEXENT"}))
        print(json.dumps(r.public(),indent=2)); return
    d=NexentDSL.parse(a.intent or "INTENT demo BY CLI USING echo WITH message=NEXENT")
    r=k.execute(Intent(d.name,d.actor,d.name,d.capability,d.payload))
    print(json.dumps(r.public(),indent=2))

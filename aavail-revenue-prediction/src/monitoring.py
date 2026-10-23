from collections import deque
from threading import Lock
import math, time
class PerformanceMonitor:
    def __init__(self,max_events=1000): self._events=deque(maxlen=max_events); self._lock=Lock()
    def record(self,runtime_ms,ok=True):
        with self._lock: self._events.append({"runtime_ms":float(runtime_ms),"ok":bool(ok),"timestamp":time.time()})
    def summary(self):
        with self._lock: events=list(self._events)
        if not events: return {"count":0,"success_rate":None,"mean_runtime_ms":None}
        values=[e["runtime_ms"] for e in events if math.isfinite(e["runtime_ms"])]
        return {"count":len(events),"success_rate":sum(e["ok"] for e in events)/len(events),"mean_runtime_ms":sum(values)/len(values) if values else None}

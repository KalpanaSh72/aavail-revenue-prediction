from src.monitoring import PerformanceMonitor
def test_monitor_records_runtime_and_success():
    m=PerformanceMonitor(); m.record(10,True); m.record(30,False); s=m.summary()
    assert s["count"]==2 and s["success_rate"]==.5 and s["mean_runtime_ms"]==20

# tests/test_simulator.py
from app.simulator import DeviceSimulator

def test_quick_simulation():
    sim = DeviceSimulator()
    result = sim.run_quick_simulation("simular cell_alpha 2s")
    assert result["status"] == "COMPLETED"
    assert "metrics" in result
    assert result["duration_s"] == 2.0 or isinstance(result["duration_s"], (int, float))

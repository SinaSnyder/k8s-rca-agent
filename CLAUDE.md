# K8s RCA Agent Context

- **Target Context**: Ensure you are connected to the main production/k3s remote cluster (NOT k3d-mycluster).
- **Target Namespace**: `test-ns`
- **Prometheus/VictoriaMetrics Endpoint**: `http://10.43.70.108:8428`

## System Boundaries
1. Read-only access to `test-ns` namespace only.
2. Never execute mutating commands (apply, delete, edit, patch).
3. Always verify cluster context using `kubectl config current-context` before running diagnostics.

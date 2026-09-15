# Kubernetes RCA Troubleshooting Skill

When diagnosing issues in namespace `test-ns`, follow this STRICT order of steps:

1. **Pods Checklist**: List all pods to check status (CrashLoopBackOff, Pending, ImagePullBackOff, etc.).
   - Command: `kubectl get pods -n test-ns`
2. **Events Analysis**: Read namespace events to check for OOMKilled, failed scheduling, or probe failures.
   - Command: `kubectl get events -n test-ns --sort-by='.metadata.creationTimestamp'`
3. **Describe Resources**: Describe unhealthy pods or deployments.
   - Command: `kubectl describe pod <pod-name> -n test-ns`
4. **Logs Extraction**: Check standard logs and previous container instance logs if crashed.
   - Command: `kubectl logs <pod-name> -n test-ns --previous`
5. **Deployment & Config Inspection**: Check YAML configurations, env vars, configmaps, and resource limits.
6. **Endpoints & Connectivity**: Check related services and endpoints.
7. **Formulate Hypothesis**: Only suggest root causes after evidence collection.

## Mandatory Output Format
You MUST format your final response strictly as follows:

ROOT CAUSE: <one sentence summary>

EVIDENCE:
  - <command executed> -> <what it showed>

CONFIDENCE: high | medium | low

PROPOSED PATCH:
  <yaml patch or fix description>

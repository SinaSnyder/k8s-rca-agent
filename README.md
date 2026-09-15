# Autonomous Kubernetes RCA Agent (OpenCode AI)

An autonomous Root Cause Analysis (RCA) agent built with **OpenCode AI**, designed to inspect, diagnose, and propose fixes for Kubernetes cluster failures in real-time. The agent operates under strict **read-only constraints** enforced by both Kubernetes RBAC and custom security hooks.

---

## 🏗 System Architecture & Security Boundary

To ensure the agent never alters or destabilizes the infrastructure, a **Defense-in-Depth** security model is applied:

1. **Kubernetes RBAC (`rbac/`)**  
   Bound to a dedicated `rca-agent` ServiceAccount in `test-ns`. Granted only `get`, `list`, and `watch` verbs on workload resources.

2. **Pre-Tool Hook (`hooks/pre_tool_use.py`)**  
   Intercepts LLM tool executions and blocks mutating operations such as `apply`, `delete`, `edit`, `patch`, `scale`, and `replace`.

3. **Post-Tool Hook (`hooks/post_tool_use.py`)**  
   Automatically redacts sensitive fields such as passwords, tokens, secrets, and API keys from raw CLI outputs using regular expressions before sending them back to the LLM context.

4. **Context Constraints (`CLAUDE.md`)**  
   Forces context verification prior to execution, restricting operations solely to the targeted `test-ns` namespace.

---

## 📂 Project Structure

```text
.
├── CLAUDE.md                 # System boundaries & environment guidelines
├── hooks/
│   ├── pre_tool_use.py       # Pre-execution hook for blocking mutating commands
│   └── post_tool_use.py      # Post-execution hook for redacting sensitive data
├── rbac/
│   ├── service-account.yaml  # Dedicated SA for the RCA Agent
│   ├── role.yaml             # Read-only cluster role definitions
│   └── role-binding.yaml     # RoleBinding targeting test-ns
└── skills/
    └── k8s-rca/
        └── SKILL.md          # Mandatory diagnostic process & structured output schema
```

---

## ⚡ RCA Workflow & Output Schema (`SKILL.md`)

When triggered, the agent strictly follows a systematic troubleshooting workflow:

1. **Pod State Check**
   ```bash
   kubectl get pods -n test-ns
   ```

2. **Event Analysis**
   ```bash
   kubectl get events -n test-ns
   ```

3. **Resource Descriptions**
   ```bash
   kubectl describe pod <pod-name> -n test-ns
   ```

4. **Container Logs**
   ```bash
   kubectl logs <pod-name> -n test-ns --previous
   ```

5. **Config & Connectivity**
   Manifest, Endpoint, and Service verifications.

### Output Format

All diagnostic responses are structured as follows:

- **ROOT CAUSE**: A concise single-sentence summary of the defect.
- **EVIDENCE**: Command execution logs paired with direct observations.
- **CONFIDENCE**: `high` | `medium` | `low`
- **PROPOSED PATCH**: Non-applied YAML manifest or remediation command.

---

## 🧪 Live Chaos Testing & Verification

You can test the agent's capabilities using the following live chaos scenarios.

### Scenario 1: ImagePullBackOff

```bash
kubectl create deployment broken-app --image=nginx:non-existent-tag -n test-ns
```

### Scenario 2: OOMKilled (Memory Limit Breach)

```bash
kubectl run oom-app -n test-ns --image=polinux/stress --overrides='{"spec":{"containers":[{"name":"oom-app","image":"polinux/stress","resources":{"limits":{"memory":"10Mi"}},"args":["stress","--vm","1","--vm-bytes","50M"]}]}}'
```

---

## ▶️ Running the Diagnostic Prompt

Inside OpenCode CLI, run:

> **"Inspect the pods in namespace `test-ns` and conduct a root cause analysis for any failing components according to `skills/k8s-rca/SKILL.md`."**

---

## 🔐 Security Model Summary

| Layer | Component | Purpose |
|---|---|---|
| **RBAC** | `rbac/` | Restricts Kubernetes permissions to read-only operations |
| **Pre-Tool Security** | `hooks/pre_tool_use.py` | Blocks mutating Kubernetes commands |
| **Post-Tool Security** | `hooks/post_tool_use.py` | Redacts sensitive information from command output |
| **Context Control** | `CLAUDE.md` | Restricts diagnostics to `test-ns` and enforces context verification |
| **Diagnostic Policy** | `skills/k8s-rca/SKILL.md` | Defines the mandatory RCA workflow and response format |

---

## 🎯 Goals

The project is designed to provide:

- Autonomous Kubernetes failure diagnosis
- Strict read-only infrastructure access
- Defense-in-depth security controls
- Automated sensitive-data redaction
- Structured and evidence-based RCA reports
- Safe remediation proposals without automatic execution

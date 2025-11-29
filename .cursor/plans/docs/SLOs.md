## Service-Level Objectives (SLOs) for KVSHVL Platform

This document defines lightweight SLOs for reliability, performance, and cost across ASK, Reframe, and Sketch2BIM.

These SLOs are intentionally simple and are meant to be enforced using existing monitoring primitives (health checks, Groq usage tracking, Redis metrics, and Razorpay data).

---

### 1. Availability & Errors

- **ASK API**
  - **Availability SLO**: `/health` returns HTTP 200 for **≥ 99.5%** of 5‑minute intervals over a rolling 30‑day window.
  - **Error Rate SLO**: 5xx responses constitute **< 1%** of total requests over any 1‑hour window.

- **Reframe API**
  - Same as ASK:
    - `/health` ≥ 99.5% 5‑minute interval success over 30 days.
    - 5xx error rate < 1% per 1‑hour window.

- **Sketch2BIM API**
  - **Availability SLO**: `/health` returns HTTP 200 for **≥ 99.0%** of 5‑minute intervals over a rolling 30‑day window (allowing for heavier workloads).
  - **Error Rate SLO**: 5xx responses constitute **< 2%** of total requests over any 1‑hour window.

**How to measure**

- Use Render health status plus periodic probes (for example, a small cron job calling the `/health` endpoints and logging/updating a counter in Redis or the database).
- For error rates, aggregate request logs or gateway logs (if available) and compute 5xx percentage per time window.

---

### 2. Latency

Key endpoints:

- **ASK**
  - `/api/generate` (question generation)
  - `/api/feasibility/platform/*` (platform dashboard)
- **Reframe**
  - Reframe main POST endpoint (text reframing)
- **Sketch2BIM**
  - `/api/v1/generate` (core conversion job submission)

**Latency SLOs**

- **ASK**
  - p95 latency for `/api/generate` and feasibility endpoints **< 500 ms** over a rolling 1‑hour window (excluding Groq upstream latency spikes beyond our control).

- **Reframe**
  - p95 latency for reframing endpoint **< 400 ms** over a rolling 1‑hour window.

- **Sketch2BIM**
  - p95 latency for job submission endpoint **< 800 ms** (job processing itself is asynchronous and not part of this SLO).

**How to measure**

- Log per‑request duration (start/end timestamps) and periodically compute p95 over the last N minutes.
- Alternatively, add simple Prometheus metrics (as already present in Sketch2BIM) and configure external alerting on p95 histograms.

---

### 3. Cost SLOs

These SLOs align with the Groq monitoring and Redis/DB‑backed cost tracking already implemented.

- **Groq usage (all apps combined)**
  - **Monthly cost SLO**: total Groq spend **≤ $50 / month**.
  - **Daily spike SLO**: daily Groq request count not exceeding **2× the 7‑day rolling average** without an accompanying alert/justification.

- **Razorpay fees and infra costs**
  - **ASK / Sketch2BIM**
    - Razorpay fees for each app should not exceed **10% of monthly revenue** for that app.
  - **Shared infrastructure**
    - Infra + Groq + Razorpay combined should keep the platform‑wide gross margin **≥ 60%** in realistic scenarios (as visible in the platform dashboard).

**How to measure**

- **ASK**: use the `apps/ask/api/utils/groq_monitor.py` utilities and DB cost tables.
- **Reframe**: use `apps/reframe/backend/app/services/groq_monitor.py` plus Redis aggregates.
- **Sketch2BIM**: rely on Redis‑backed usage and DB cost data tracked via the backend.

Alerts should be raised when:

- Monthly Groq usage crosses `GROQ_MONTHLY_COST_THRESHOLD` (already wired in Groq monitors).
- Derived cost metrics in the admin platform dashboard show margin dropping below thresholds (manual review or future automated checks).

---

### 4. Alerting Hooks (Email / Slack)

Current state:

- **ASK**
  - `apps/ask/api/utils/groq_monitor.py` already supports:
    - Email alerts (via `ASK_ALERT_EMAIL_ENABLED` / `ASK_ALERT_EMAIL_RECIPIENTS`).
    - Slack alerts (via `ASK_ALERT_SLACK_ENABLED` / `ASK_ALERT_SLACK_WEBHOOK_URL`).
- **Reframe**
  - Groq monitor writes usage and alerts to Redis; external alerting can be added by:
    - Polling Redis metrics from a scheduled job.
    - Triggering email/Slack notifications when thresholds are exceeded.
- **Sketch2BIM**
  - Uses Upstash Redis and existing resource‑alert thresholds (`SKETCH2BIM_RESOURCE_ALERT_WARNING_THRESHOLD`, `SKETCH2BIM_RESOURCE_ALERT_CRITICAL_THRESHOLD`).

Recommended minimal setup:

1. **ASK**
   - Set:
     - `ASK_ALERT_EMAIL_ENABLED=true`
     - `ASK_ALERT_EMAIL_RECIPIENTS=<comma-separated emails>`
     - Optionally `ASK_ALERT_SLACK_ENABLED=true` and `ASK_ALERT_SLACK_WEBHOOK_URL=<webhook>`.
   - Run a daily or hourly job that:
     - Uses `check_groq_usage_alerts` to compute alerts.
     - Sends them via `send_groq_alert`.

2. **Reframe / Sketch2BIM**
   - Add a small scheduled task (cron, Render job, or external worker) that:
     - Reads Redis metrics (Groq usage and resource limits).
     - Compares to SLO thresholds defined above.
     - Sends notifications through the same channels used for ASK (email/Slack), or logs to a central place.

---

### 5. Tying SLOs into the Admin Platform Dashboard

- The admin platform dashboard already surfaces:
  - Consolidated feasibility metrics.
  - Cost / revenue / margin data across apps.
- To make SLOs visible:
  - Display Groq and Razorpay alerts (from `/api/monitoring/alerts`) in an **“Alerts”** panel.
  - Highlight when:
    - Monthly Groq cost ≥ threshold.
    - Gross margin < 60% in realistic scenarios.
    - Any app’s error rate or availability falls below SLOs (using aggregated metrics once available).

This keeps SLOs observable directly from the dashboard instead of only in logs.



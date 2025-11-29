## API Versioning Strategy

### Current State

- **ASK backend (`apps/ask/api`)**
  - Routes are mounted under the `/api` prefix (for example, `/api/feasibility/...`).
  - There is **no explicit version segment** in the path.
- **Reframe backend (`apps/reframe/backend/app`)**
  - Routes are mounted directly on the FastAPI app without an `/api` prefix.
  - Public endpoints are effectively versionless (for example, `/reframe`-specific routes under the root).
- **Sketch2BIM backend (`apps/sketch2bim/backend/app`)**
  - All public API routes are mounted under an explicit `/api/v1` prefix.
  - This is the most “mature” API and is designed with long‑term compatibility in mind.

This mix of patterns is intentional:

- Sketch2BIM uses explicit versioning because its external API surface is expected to evolve while preserving backwards compatibility.
- ASK and Reframe are newer and their APIs can still tolerate breaking changes behind feature work.

---

### When to Introduce `/api/v2` (or Higher)

Introduce a new versioned prefix (for example, `/api/v2` or `/api/v2/...`) when **any** of the following are true:

- **Breaking request changes**
  - Required fields are removed or renamed.
  - Request body shape, query parameters, or path parameters change incompatibly.
- **Breaking response changes**
  - Response payload structure changes in a way that would break existing clients (for example, keys removed or fundamental type changes).
  - Error response format changes in a way that existing consumers cannot handle.
- **Behavioral changes**
  - Semantics of an endpoint change significantly (for example, different pricing semantics, units, or guarantees) while keeping the same path.

Non‑breaking changes (for example, adding optional fields) **should not** trigger a new version.

---

### Recommended Patterns Per App

- **ASK**
  - Keep existing endpoints under `/api` for now.
  - When you need breaking changes for a given logical area (for example, platform feasibility or cost tracking), introduce explicit versioned prefixes:
    - Example: `/api/v1/feasibility/...` (current), `/api/v2/feasibility/...` (future breaking changes).
  - Continue to treat the unversioned `/api` prefix as “v1” for now.

- **Reframe**
  - For now, keep the current simple routing.
  - For any external clients that depend on stability, prefer to add a version prefix early, similar to Sketch2BIM (for example, `/api/v1/reframe/...`).

- **Sketch2BIM**
  - Continue to use `/api/v1` as the stable, documented surface.
  - When introducing breaking changes, add parallel `/api/v2/...` routes rather than modifying `/api/v1` in place.

---

### Migration Strategy for New Versions

When adding `/api/v2` (or a higher version):

1. **Add v2 endpoints in parallel**
   - Implement `/api/v2/...` alongside existing `/api/v1/...`.
   - Keep `/api/v1` behavior unchanged.
2. **Document changes clearly**
   - For each endpoint, document:
     - Request differences.
     - Response differences.
     - Behavior/semantics differences.
3. **Support a deprecation window**
   - Keep `/api/v1` live for a defined period (for example, 3–6 months) while clients migrate.
   - Mark `/api/v1` as deprecated in documentation and response headers if appropriate (for example, a `Deprecation` header).
4. **Update clients incrementally**
   - Frontend apps in this monorepo should switch to `/api/v2` first.
   - Any external consumers should be given a clear migration guide and timeline.
5. **Remove old versions deliberately**
   - After the deprecation window, remove `/api/v1` handlers and update docs to reflect the new default.

---

### Client Guidance

For clients consuming platform APIs (ASK dashboard, Reframe frontend, Sketch2BIM frontend, or external tools):

- Prefer **explicitly versioned** endpoints when available (for example, `/api/v1/...`).
- Treat unversioned endpoints:
  - As “best effort” during early iteration.
  - As equivalent to “v1” once the API stabilizes; future breaking changes should be introduced via `/api/v2`.
- When a new version becomes available:
  - Switch client code to the new prefix.
  - Handle any payload or behavior differences as documented in the corresponding app’s README or API docs.

---

### Where to Document Per‑App Details

- High‑level strategy: this file (`docs/API_VERSIONING.md`).
- Per‑app specifics:
  - **ASK**: `apps/ask/api/README.md` (or equivalent) should list core `/api` endpoints and note any versioned ones.
  - **Reframe**: `apps/reframe/backend/README.md` (or equivalent) should document public routes and plans for versioning.
  - **Sketch2BIM**: `apps/sketch2bim/backend/README.md` should treat `/api/v1` as canonical and outline any `/api/v2` migrations when they are introduced.



# GitHub Profile Console Design

Build `deevyanshoo/deevyanshoo` as `DEEVYANSHOO // OPERATOR`: a GitHub-native, Bloomberg-dense, AI-lab console with automatic light/dark SVGs and a concise native Markdown fallback.

The approved public GitHub avatar is the source portrait. Reduce it to custom ASCII showing the hair, glasses, beard, and black hoodie; omit the laptop and room. Lead with Nnomi, keep Chauffit secondary, and tell the selected-build story through JARVIS hybrid/on-device inference, a decentralized DAG ledger, and large-scale aviation forecasting. Position AI Architect at ZS subtly; include UPenn MSE Data Science, `Gurugram ↔ wherever`, `making large models fit small boxes`, `runtime v26`, and `garage_target 911`.

The implementation is a dependency-free Python 3.13 package with frozen typed data, a scalar-only GitHub GraphQL client, immutable portrait/content modules, and a pure renderer. The same input must produce byte-identical SVG output. The API query must never request, persist, log, or render private repository names, URLs, descriptions, languages, topics, branches, commits, or other identifying metadata. It may request only aggregate scalar counts, including restricted contribution totals.

Display year-to-date contributions, merged pull requests, public repositories, repositories contributed to, and stars earned on public owned repositories. State that private activity is aggregated without identifying it. Do not expose DOB/time, followers, streaks, language percentages, badge walls, or misleading vanity metrics.

CI uses `contents: read` and receives no private secret. Scheduled/manual generation uses `contents: write`, `actions/checkout@v7`, `actions/setup-python@v7`, `PROFILE_TOKEN` for read-only telemetry, and `github.token` for repository writes. If the optional profile token is absent, generation falls back to public data. Commit only when rendered bytes change.

Tests cover query privacy, raw-data minimization, XML escaping, byte determinism, light/dark palettes, README accessibility, workflow permissions, and rendered-output leakage.

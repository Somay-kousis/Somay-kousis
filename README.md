<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/title-dark.svg" />
  <img src="assets/title-light.svg" width="110" alt="ME!?" />
</picture>

<img align="left" src="assets/knight.svg" width="150" alt="" />

**Somay Kousis**, I build agent systems, and the checks that keep them honest.

Co-founder of [aye aye](https://ayeayecaptain.vercel.app). The person shipping a risky AI-written change explains it out loud, and an independent judge checks the answer against the real diff. I also freelance for Standout, where I shipped a live LinkedIn networking product from an empty repo in 7 days as the only engineer. Third year of CS at ABV-IIITM Gwalior.

Right now I am writing an AI control paper and getting fixes merged upstream.

<br clear="left" />

<p><sub><b>MERGED UPSTREAM INTO</b></sub></p>

<p>
<a href="https://github.com/NVIDIA/NeMo-Agent-Toolkit/pulls?q=is%3Apr+author%3ASomay-kousis+is%3Amerged"><img src="https://img.shields.io/badge/NVIDIA-NeMo_Agent_Toolkit-76B900?style=for-the-badge&logo=nvidia&logoColor=white&labelColor=111111" alt="NVIDIA NeMo Agent Toolkit" /></a>&nbsp;
<a href="https://github.com/microsoft/agent-framework/pulls?q=is%3Apr+author%3ASomay-kousis+is%3Amerged"><img src="https://img.shields.io/badge/Microsoft-Agent_Framework-0078D4?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMyAyMyI%2BPHBhdGggZmlsbD0iI2YyNTAyMiIgZD0iTTEgMWgxMHYxMEgxeiIvPjxwYXRoIGZpbGw9IiM3ZmJhMDAiIGQ9Ik0xMiAxaDEwdjEwSDEyeiIvPjxwYXRoIGZpbGw9IiMwMGE0ZWYiIGQ9Ik0xIDEyaDEwdjEwSDF6Ii8%2BPHBhdGggZmlsbD0iI2ZmYjkwMCIgZD0iTTEyIDEyaDEwdjEwSDEyeiIvPjwvc3ZnPg%3D%3D&labelColor=111111" alt="Microsoft Agent Framework" /></a>&nbsp;
<a href="https://github.com/google/adk-python/pull/7541"><img src="https://img.shields.io/badge/Google-ADK-4285F4?style=for-the-badge&logo=google&logoColor=white&labelColor=111111" alt="Google ADK" /></a>
</p>

<br />

Most of my work comes back to one question. What does an agent do when nobody is checking, and how would you know? Pocket Change limits what it can take. Apocalypse checks whether it stays contained after it breaks out. aye aye checks whether the human understood what it wrote. Perceived Oversight asks whether it behaves differently when it thinks it is being watched.

Every number below comes with the command that produced it.

## [Pocket Change](https://github.com/Somay-kousis/Pocket-Change)

Spending authority for AI agents. Ed25519 Biscuit tokens attenuate down a delegation tree, so a sub-agent can never hold more than its parent was given. 7 bounds, checked deterministically across trees of 121 agents.

```console
$ pytest tests/attacks -q
400 attacks, 394 blocked, 6 known limits (282 agent, 38 seller, 80 network)
396 passed, 6 xfailed in 21.11s

$ pytest -q
825 passed, 6 xfailed in 27.23s
```

No model calls and no API keys, so anyone can clone it and get the same output. The 6 xfails are the known limits, written down instead of hidden.

The bug I learned the most from never failed a test. I made a payment agent the parent of a page-reading agent, and the payment agent quietly inherited read access to attacker-controlled text, because a parent has to hold everything it hands down. Isolation has to sit sideways, not stack. I found it weeks later re-reading my own threat model.

Runs on Cloud Run with Vertex AI. [Live demo](https://pocket-change-klwjhco2ta-el.a.run.app).

## [Apocalypse](https://github.com/Somay-kousis/Apocalypse)

Apart x CeSIA AI Incident Response Sprint, team of 3, **top 10%**. The July 2026 frontier-model sandbox escape had no standard you could test a lab against, so we wrote 9 containment rules, each mapped to a documented step of the real attack, and built a broken lab with the real misconfiguration next to a fixed one. I wrote rules 4, 5 and 9, the scorecard runner and the architecture.

The same runner on both labs, trimmed to my three rules:

```console
$ python -m validation.run_checks --target environments/fixed_lab/configs
  [PASS] rule 4: Loader refuses external refs
  [PASS] rule 5: No template eval on untrusted config
  [PASS] rule 9: Origin-scoped credentials + blast-radius bound
  9/9 controls PASS

$ python -m validation.run_checks --target environments/broken_lab/configs
  [FAIL] rule 4: loader followed external refs and leaked 2 value(s)
  [FAIL] rule 5: SSTI reached Python internals (17076 chars of subclass list)
  [FAIL] rule 9: credential is 'raw', not an attenuated capability token
  0/9 controls PASS
```

Offline, runs in seconds on a laptop. 118 tests.

## [Perceived Oversight](https://github.com/Somay-kousis/Perceived-Oversight)

The paper. Does an untrusted agent reveal more of a hidden objective to an overseer it thinks is a collaborator than to one it knows is a monitor? The real monitoring never changes, only what the agent believes about its partner. Built on SHADE-Arena through ControlArena, and scoped to detection, so the real monitor can act on a flagged attack. No results yet, so none claimed.

## Merged upstream

| Repo | What was broken |
|---|---|
| [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2354) | The profiler paired each LLM end event with the latest start, so overlapping calls dropped out of latency stats. Now paired by UUID. |
| [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2325) | Environment variable values were re-read as YAML, so a `#` in a value cut it short. |
| [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2320) | Resuming an eval crashed on items whose output was a list. |
| [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2332) | The JSON dataset loader turned `"001"` into `1`. |
| [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2344) | An eval output section without `dir` ignored `output_dir`, so cleanup and S3 upload hit the wrong folder. |
| [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2327) | `--override 0.7` was rejected for a setting written as `0` in YAML. |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework/pull/9428) | Declarative `SetValue` ignored the `variable` field, so YAML using it wrote nothing. |
| [Google ADK](https://github.com/google/adk-python/pull/7541) | SQLite memory search missed stored words starting with a capital dotted İ. |
| [OpenVINO GenAI](https://github.com/openvinotoolkit/openvino.genai/pull/4627) | A string `stop_strings` in `generation_config.json` was silently dropped. |
| [krkn](https://github.com/krkn-chaos/krkn/pull/1632) | Container chaos scenarios without `expected_recovery_time` crashed with a KeyError. |

## Also built

**[PaperPlanes](https://github.com/Somay-kousis/PaperPlanes)**, 3rd at the CockroachDB Hackathon, solo. Research memory where a superseded fact is closed with `valid_to` instead of overwritten. 25 concurrent writers on one counter: all 25 held under SERIALIZABLE retries, where a flat file kept 1.

**[RabbitHole](https://github.com/Somay-kousis/RabbitHole)**. A LangGraph courtroom that, asked for 2 perspectives, kept generating 6 to 8 and hit Groq's rate limit. Prompt rewording never fixed it. Moving the count into a state schema the moderator schedules against did, and time to verdict went from 19.8s to 9.8s.

**[podman-flake-agent](https://github.com/Somay-kousis/podman-flake-agent)**. Prototype for the LFX Mentorship on CI flake triage. Sending only the failing block cuts payload 76% to 93% before inference, and `unknown` is a valid verdict, because calling a real race condition a flake tells a maintainer to re-run a genuine bug.

**[Something](https://github.com/SomethingDuality/Somethingv1)**. My first startup, Apr to Jun 2026. 573 people on the waitlist in the first month with no paid distribution. It did not become a company, and the code is open now.

<details>
<summary>Older</summary>
<br />

- [Co-op Purchase Coordinator](https://github.com/Somay-kousis/Co-op-Purchase-Coordinator): second-price auctions and coalition discounts for agents buying from the same seller.
- [Co-Founder Memory](https://github.com/Somay-kousis/Co-Founder-Memory): a 19-node LangGraph with a nightly dossier pipeline on pgvector.
- [Oeuvre](https://github.com/Somay-kousis/Oeuvre), [The Last Library](https://github.com/Somay-kousis/The-Last-Library): RAG projects from when I was learning retrieval.
- [SteelCareer](https://github.com/Somay-kousis/SteelCareer): a hiring platform shipped to a real client.
- [House Price Prediction System](https://github.com/Somay-kousis/House-Price-Prediction-System): my first ML project, kept on purpose.

</details>

## On the record

<img align="right" src="assets/hornet.svg" width="130" alt="" />

- Top 10%, Apart x CeSIA AI Incident Response Sprint
- Winner, Egoistic Ideathon 2026, captain of a team of 4
- 3rd, CockroachDB Hackathon, solo
- 6th of 500 on our problem statement, Smart India Hackathon 2025
- 2nd, Hacksagon 2024, hardware track
- Agentic AI domain lead, GDG on Campus ABV-IIITM
- Published poetry in *Camas* (Linfield University)

I also teach math and English to kids every week with the SGM social initiative.

Still getting DSA wrong. I open a problem, get an idea, and build that instead. Most of the list above started that way.

<br clear="right" />

[LinkedIn](https://linkedin.com/in/somay-kousis-630ab1313) · [X](https://x.com/somaykousis) · somaykousis@gmail.com

<img align="left" src="assets/knight.svg" width="130" alt="" />

**Somay Kousis**, I build agent systems, and the checks that keep them honest.

Co-founder of [aye aye](https://ayeayecaptain.vercel.app). The person shipping a risky AI-written change explains it out loud, and an independent judge checks the answer against the real diff. I also freelance for Standout, where I shipped a live LinkedIn networking product from an empty repo in 7 days as the only engineer. Third year of CS at ABV-IIITM Gwalior.

Right now I am writing an AI control paper and getting fixes merged upstream.

<br clear="left" />

```
merged upstream since Oct 13          52

NVIDIA     NeMo Agent Toolkit         26
NVIDIA     NeMo Relay                  7
NVIDIA     garak                       1
Google     ADK                         6
Microsoft  Agent Framework             3
Intel      OpenVINO                    6
Intel      OpenVINO GenAI              1
CNCF       krkn                        2
```

**NVIDIA NeMo Agent Toolkit** [#2365](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2365). Agents ran one tool call past `max_tool_calls`, and no `recursion_limit` could stop it, because the graph counts node steps, not tool calls. All four agent types now stop before call N+1.

**NVIDIA garak** [#2315](https://github.com/NVIDIA/garak/pull/2315). The WebSocket generator ignored `--target_name`, so a scan of your own endpoint sent every prompt to a public echo server and scored the echoes.

**NVIDIA NeMo Agent Toolkit** [#2325](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2325). `${VAR}` was spliced into raw YAML before parsing, so a `#` in a secret cut it short. Merged as a breaking change.

**Google ADK** [7541](https://github.com/google/adk-python/commit/2416f66). Memory search never found a stored word starting with a capital dotted İ, because lowercasing it adds a combining dot that split the token.

**Microsoft Agent Framework** [#9428](https://github.com/microsoft/agent-framework/pull/9428). Declarative `SetValue` accepted a `variable` field the executor never read, so the workflow ran and the value stayed unset.

<details>
<summary><b>47 more</b></summary>
<br />

| Repo | Fix | What was broken |
|---|---|---|
| NeMo Agent Toolkit | [#2462](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2462) | A failed streamed request logged `QueueClosed` "Task exception was never retrieved" tracebacks next to the real error. |
| NeMo Agent Toolkit | [#2460](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2460) | A logging handler set to `DEBUG` got nothing below the CLI's `--log-level`, because the root level could only be raised, never lowered. |
| NeMo Agent Toolkit | [#2458](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2458) | A workflow that failed mid-stream sent its error as a bare line SSE parsers drop, so `nat serve` clients saw a stream that just stopped. |
| NeMo Agent Toolkit | [#2456](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2456) | `nat mcp serve` failed to start with a function group that had no `include`, because the builder only looked in the global registry. |
| NeMo Agent Toolkit | [#2454](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2454) | Span batching stopped after the first run of a long-lived workflow, so `nat serve` and `nat eval` made one export call per span. |
| NeMo Agent Toolkit | [#2450](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2450) | Automatic retries used a fixed backoff and gave up before a rate-limited provider's `Retry-After` ran out. Now LiteLLM, Bedrock and OpenAI wait for it. |
| NeMo Agent Toolkit | [#2424](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2424) | A function that raised was exported to tracing as OK, even when the agent recovered from the failed tool. |
| NeMo Agent Toolkit | [#2422](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2422) | A failed or cancelled run never exported its root span, so Phoenix, Langfuse and OTel got spans with no root. |
| NeMo Agent Toolkit | [#2410](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2410) | The Semantic Kernel clients ignored `temperature`, `top_p`, `seed` and `max_retries` from the LLM config. |
| NeMo Agent Toolkit | [#2408](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2408) | Turning on `thinking` turned off automatic retries, because the second patch replaced the first on the same methods. |
| NeMo Agent Toolkit | [#2406](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2406) | ADK clients ignored the retry and `thinking` options that every other framework wrapper honoured. |
| NeMo Agent Toolkit | [#2404](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2404) | The reasoning agent ignored its configured `description`, so calling agents always saw a hard-coded one. |
| NeMo Agent Toolkit | [#2394](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2394) | An interrupted `nat eval` lost every finished item and started over. Items now stay on disk and `--resume` runs only the rest. |
| NeMo Agent Toolkit | [#2377](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2377) | The ReAct and ReWOO agents reported word counts as token usage instead of what the model reported. |
| NeMo Agent Toolkit | [#2369](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2369) | `nat serve` sent the A365 auth token to its workers as `**********`, because it was masked when the config was copied for them. |
| NeMo Agent Toolkit | [#2371](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2371) | The router agent sent `web_search` requests to the `search` branch, because it took the first name that matched. |
| NeMo Agent Toolkit | [#2367](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2367) | The per-user ReAct agent ignored `raise_on_parsing_failure` and `use_native_tool_calling`. |
| NeMo Agent Toolkit | [#2361](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2361) | The MCP client dropped an explicit `null` for a required tool argument, so the server got a call missing a required key. |
| NeMo Agent Toolkit | [#2354](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2354) | The profiler paired each LLM end event with the latest start, so two overlapping 10 s calls became one 9 s sample. |
| NeMo Agent Toolkit | [#2352](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2352) | An eval run where no evaluator returned a result wrote no `workflow_output.json`. |
| NeMo Agent Toolkit | [#2344](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2344) | An eval output section without `dir` ignored `output_dir`, so `cleanup: true` deleted the wrong folder. |
| NeMo Agent Toolkit | [#2332](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2332) | The JSON dataset loader turned `"001"` into `1`, so `.json` and `.jsonl` gave different eval inputs. |
| NeMo Agent Toolkit | [#2327](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2327) | `--override 0.7` was rejected for a setting written as `0` in YAML. |
| NeMo Agent Toolkit | [#2320](https://github.com/NVIDIA/NeMo-Agent-Toolkit/pull/2320) | Resuming an eval crashed on items whose output was a list. |
| NeMo Relay | [#1531](https://github.com/NVIDIA/NeMo-Relay/pull/1531) | With a codec active, hints written to `metadata.relay_hints` replaced the request's own `metadata` instead of adding to it. |
| NeMo Relay | [#1525](https://github.com/NVIDIA/NeMo-Relay/pull/1525) | `adaptive_hints.inject_header` and `inject_body_path` did nothing: hints always went in a header and in `nvext.agent_hints`. |
| NeMo Relay | [#1511](https://github.com/NVIDIA/NeMo-Relay/pull/1511) | A typo'd key in `[gateway]`, `[upstream]` or `[agents]` was ignored without a word. Now it logs a warning and the rest still loads. |
| NeMo Relay | [#1513](https://github.com/NVIDIA/NeMo-Relay/pull/1513) | An empty or relative `XDG_CONFIG_HOME` put Relay's config and plugins in a `nemo-relay` folder under whatever directory you ran it from. |
| NeMo Relay | [#1508](https://github.com/NVIDIA/NeMo-Relay/pull/1508) | Azure OpenAI streams kept the empty `id`, `model` and `created` from Azure's leading prompt-filter chunk instead of the real ones. |
| NeMo Relay | [#1504](https://github.com/NVIDIA/NeMo-Relay/pull/1504) | The Python, Node and Go log helpers rejected level names the logging config accepts, like `"WARNING"` and `"Info"`. |
| NeMo Relay | [#1509](https://github.com/NVIDIA/NeMo-Relay/pull/1509) | A streamed Anthropic tool call with no arguments came out as `"input": ""` instead of `{}`. |
| Google ADK | [7634](https://github.com/google/adk-python/commit/da786ed) | `AnthropicLlm` always sent `tool_choice: auto`, so `NONE`, `ANY` and a single allowed function never reached Claude. |
| Google ADK | [7596](https://github.com/google/adk-python/commit/12c7bed) | An AgentTool's wrapped agent never saw the caller's `temp:` state. |
| Google ADK | [7605](https://github.com/google/adk-python/commit/6727f8f) | After a paused single-turn sub-agent, the next turn went to the wrong agent instead of back to its delegator. |
| Google ADK | [7577](https://github.com/google/adk-python/commit/db432db) | The SQLite session store turned state integers beyond 64 bits into floats, even on later unrelated writes. |
| Google ADK | [7561](https://github.com/google/adk-python/commit/8ff9941) | Client token-usage metrics came back empty when the last streamed response had no usage data. |
| Microsoft Agent Framework | [#9720](https://github.com/microsoft/agent-framework/pull/9720) | A workflow agent run with `stream=True` ended with no token usage, though the same run without streaming reported it. |
| Microsoft Agent Framework | [#9399](https://github.com/microsoft/agent-framework/pull/9399) | Bedrock non-streaming responses, and the traces built from them, named the client's default model instead of the one requested. |
| OpenVINO | [#39181](https://github.com/openvinotoolkit/openvino/pull/39181) | `ops.read_value(variable_id=..., ...)` with keywords only picked the wrong overload and failed on a missing `init_value`. |
| OpenVINO | [#39179](https://github.com/openvinotoolkit/openvino/pull/39179) | `OVDict.to_dict()` returned the result's own dict, so `.clear()` on it emptied the inference result. |
| OpenVINO | [#39174](https://github.com/openvinotoolkit/openvino/pull/39174) | `ops.read_value` rejected a type name like `"f32"` for `variable_type`, though its signature accepts strings. |
| OpenVINO | [#38810](https://github.com/openvinotoolkit/openvino/pull/38810) | `pack_data` kept only the low bits, so u4 `16` packed as `0` and i4 `8` became `-8`, with no error. |
| OpenVINO | [#38951](https://github.com/openvinotoolkit/openvino/pull/38951) | float32 data fed to a bf16 model input was read as raw bits, so `[1.5, 3.0]` came out as `[0.125, 32.0]` with no error. |
| OpenVINO | [#38884](https://github.com/openvinotoolkit/openvino/pull/38884) | `from_torchvision` CenterCrop lost the last row or column, so a CLIP-style 224 crop came out 223x224 and failed a static-shape model. |
| OpenVINO GenAI | [#4627](https://github.com/openvinotoolkit/openvino.genai/pull/4627) | A single-string `stop_strings` in `generation_config.json` was dropped, so those models never stopped on it. |
| krkn (CNCF) | [#1657](https://github.com/krkn-chaos/krkn/pull/1657) | An `exclude_label` value like `true` or `1.0` reached the NetworkPolicy as a bool or float instead of a string. |
| krkn (CNCF) | [#1632](https://github.com/krkn-chaos/krkn/pull/1632) | Container chaos scenarios without `expected_recovery_time` crashed before injecting any fault. |

</details>

<sub>[Every merged PR](https://github.com/pulls?q=is%3Apr+author%3ASomay-kousis+is%3Amerged) · [Google ADK commits](https://github.com/google/adk-python/commits?author=Somay-kousis). Google lands outside PRs through Copybara, so they show as closed.</sub>

## Agent safety

What does an agent do when nobody is checking, and how would you know? Pocket Change limits what it can take. Apocalypse checks whether it stays contained after it breaks out. Perceived Oversight asks whether it behaves differently when it thinks it is being watched. Every number here comes with the command that produced it.

### [Pocket Change](https://github.com/Somay-kousis/Pocket-Change)

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

### [Apocalypse](https://github.com/Somay-kousis/Apocalypse)

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

### [Perceived Oversight](https://github.com/Somay-kousis/Perceived-Oversight)

The paper. Does an untrusted agent reveal more of a hidden objective to an overseer it thinks is a collaborator than to one it knows is a monitor? The real monitoring never changes, only what the agent believes about its partner. Built on SHADE-Arena through ControlArena, and scoped to detection, so the real monitor can act on a flagged attack. No results yet, so none claimed.

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

[LinkedIn](https://linkedin.com/in/somay-kousis-630ab1313) · [Insta](https://www.instagram.com/somay.ipynb/) · somaykousis@gmail.com

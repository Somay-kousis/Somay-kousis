<div align="center">
  <img src="assets/header.png" width="100%" alt="Somay Kousis" />
</div>

<br />

<div align="center">

![Profile Views](https://komarev.com/ghpvc/?username=Somay-kousis&style=for-the-badge&color=111111&label=VISITORS)&nbsp;&nbsp;
![Stars](https://img.shields.io/github/stars/Somay-kousis?style=for-the-badge&color=111111&label=STARS)&nbsp;&nbsp;
![Followers](https://img.shields.io/github/followers/Somay-kousis?style=for-the-badge&color=111111&label=FOLLOWERS)

</div>

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=1200&color=111111&center=true&vCenter=true&width=680&lines=I+build+the+version+that+survives+contact.;Memory+that+stays+correct+after+it+is+contradicted.;25+of+25+writes+held.+A+flat+file+kept+1.;Every+number+here+ships+with+the+command+that+proves+it.)](https://git.io/typing-svg)

</div>

---

## I build memory systems, agentic workflows, and interfaces that feel a little alive.

<img align="left" src="assets/knight.png" width="180" alt="profile art" />

Hi, I am **Somay Kousis**. I also go by **Blink**.

CS student at **ABV-IIITM Gwalior**. Currently **AI Systems Engineer Intern at RYSE Technologies**, where I built the orchestrator routing tasks across a registry of 3,000+ specialized subagents. Also **co-founder and CEO of Something**, a founder and investor matching layer built on verified proof of work rather than network access.

The thing I keep coming back to: most systems are built to work once, in the demo, on the happy path. I am more interested in the version that holds up afterwards. Under contention. Under a rate limit. After the fact it recorded last month turns out to be wrong.

That preference shows up in the code before it shows up in anything I say about it. Two of my projects independently converged on the same write path, and I did not plan that.

<br clear="left" />

---

<div align="center">
  <img src="assets/ledger.svg" width="100%" alt="Consolidation log: what I added, updated, invalidated, and left alone" />
</div>

---

## Proof Of Work

Ordered by how much of it survives inspection, not by how recent it is.

### [PaperPlanes](https://github.com/Somay-kousis/PaperPlanes)

A research companion on a **CockroachDB memory substrate** with bi-temporal fact versioning, so a superseded claim is closed with `valid_to` and stays auditable instead of being overwritten. Not a vector store bolted to a chatbot.

Every claim ships a reproduction command:

| Claim | Result | Baseline |
|---|---|---|
| 25 concurrent writers, one counter | **25 / 25 held**, 58 SERIALIZABLE conflicts auto-retried | flat file kept **1**, silently lost 24 |
| ANN over ~10,000 notes | **~15ms** C-SPANN vector search | O(n) full scan |
| Live DB restart mid-conversation | next turn returns **200** | history gone |

There is a test in there asserting the decision model is real Nova and not stubbed, because mocks agree with you and a real cluster does not.

![LangGraph](https://img.shields.io/badge/LangGraph-111111?style=flat-square)
![CockroachDB](https://img.shields.io/badge/CockroachDB-111111?style=flat-square&logo=cockroachlabs&logoColor=white)
![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-111111?style=flat-square&logo=amazonaws&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-111111?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-111111?style=flat-square&logo=fastapi&logoColor=white)

### [podman-flake-agent](https://github.com/Somay-kousis/podman-flake-agent)

Prototype for the **LFX Mentorship on agentic CI flake categorization**. Podman's migration off Cirrus orphaned `logformatter`, the 38KB Perl script that used to classify every subtest, so triage fell back to a human reading a bar graph.

The hard parts were not calling a model on a log:

- **Ground truth had to be mined.** The project never auto-reruns failing tests, so "failed then passed" is not handed to you. Three weighted proxy signals stand in.
- **Cost is an architecture decision.** 30+ jobs per PR, each with a full journal. Extracting only the failing block cuts payload **76% to 93%** before inference.
- **A confident wrong answer is worse than no tool.** Call a real race condition an infra blip and you have told a maintainer to press re-run on a genuine bug. `unknown` is a first-class verdict.

Standard library only. Clone it and run the whole eval with no token and no API budget.

![Python](https://img.shields.io/badge/Python-111111?style=flat-square&logo=python&logoColor=white)
![LLM Evals](https://img.shields.io/badge/LLM_Evals-111111?style=flat-square)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-111111?style=flat-square&logo=githubactions&logoColor=white)
![Zero Deps](https://img.shields.io/badge/Zero_Dependencies-111111?style=flat-square)

### [RabbitHole](https://github.com/Somay-kousis/RabbitHole)

A LangGraph courtroom over a real legal corpus. Asked politely for 2 perspectives, it generated 6 to 8, a 3 to 4x overrun that burned Groq's token-per-minute ceiling before the debate resolved. No amount of prompt rewording fixed it.

Moving perspective count into a **state schema the moderator schedules against** fixed it completely. Mean time to verdict went from **19.8s to 9.8s**. Retrieval is Pinecone dense plus a BM25 sparse encoder, Jina reranking on top, and a three-way CRAG route: good chunks synthesize locally, bad chunks fall back to web search, ambiguous chunks run both in parallel.

![Python](https://img.shields.io/badge/Python-111111?style=flat-square&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-111111?style=flat-square)
![Pinecone](https://img.shields.io/badge/Pinecone_+_BM25-111111?style=flat-square)
![Jina](https://img.shields.io/badge/Jina_Rerank-111111?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-111111?style=flat-square)

### [Something](https://github.com/Somay-kousis/Something)

Co-founded. Team formation and capital discovery are the same failure wearing two costumes, and nobody had built one system closing both. Existing platforms either gate on post-traction signals a pre-seed founder cannot produce, or apply no verification at all and drown both sides in noise.

Something gates on proof that exists **before** revenue: prototype, pilot, patent, press. **573-person waitlist in the first month, zero paid distribution.** I own frontend, AI architecture, and go-to-market.

![Next.js](https://img.shields.io/badge/Next.js-111111?style=flat-square&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React_19-111111?style=flat-square&logo=react&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-111111?style=flat-square&logo=mongodb&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-111111?style=flat-square)

### [Co-op Purchase Coordinator](https://github.com/Somay-kousis/Co-op-Purchase-Coordinator)

When autonomous agents buy from shared sellers they collide, bid against each other, and waste rounds under a seller's hidden floor. This resolves each collision with the mechanism that actually fits it instead of one generic rule.

Second-price auction flooring the winning bid at the seller's reservation price. Shapley-inspired coalition discounts scaling 5% at two buyers to 20% at four. Binary search converges on a seller's price in about **7 rounds**. 46 tests, including concurrency and 3 regression bugs.

![FastAPI](https://img.shields.io/badge/FastAPI-111111?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-111111?style=flat-square&logo=python&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-111111?style=flat-square&logo=googlecloud&logoColor=white)

### [Co-Founder Memory](https://github.com/Somay-kousis/Co-Founder-Memory)

A **19-node stateful LangGraph** separating live conversational memory extraction, critique-driven planning loops, and an automated nightly dossier pipeline. Backed by Supabase pgvector with HNSW indexing. A daily catch-up scheduler reconstructs project momentum by correlating engineering logs, GitHub activity, and targeted search, looping an auto-reviewer back to search until the dossier passes.

![Python](https://img.shields.io/badge/Python-111111?style=flat-square&logo=python&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase_pgvector-111111?style=flat-square&logo=supabase&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-111111?style=flat-square)

### [Portfolio](https://github.com/Somay-kousis/Portfolio)

Part website, part environment. Every number on it links to the repository that proves it, which is the only design constraint that actually mattered.

![Next.js](https://img.shields.io/badge/Next.js-111111?style=flat-square&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-111111?style=flat-square&logo=typescript&logoColor=white)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-111111?style=flat-square&logo=framer&logoColor=white)

---

<details>
<summary><strong>Smaller Experiments</strong> (click to expand)</summary>
<br />

- [Oeuvre](https://github.com/Somay-kousis/Oeuvre): a portfolio RAG system over personal memory, including the contradictions.
- [The Last Library](https://github.com/Somay-kousis/The-Last-Library): small RAG mystery project built while learning retrieval.
- [SteelCareer](https://github.com/Somay-kousis/SteelCareer): multi-role hiring platform shipped to a real client. Human introductions, not algorithmic matching.
- [Customer Churn Prediction](https://github.com/Somay-kousis/Customer-Churn): churn risk and classification.
- [House Price Prediction System](https://github.com/Somay-kousis/House-Price-Prediction-System): my first ML project, kept here on purpose.

</details>

---

## Stack I Am Actually Using

**AI / Backend**

![Python](https://img.shields.io/badge/Python-111111?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-111111?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-111111?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-111111?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-111111?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-111111?style=for-the-badge&logo=ollama&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-111111?style=for-the-badge)
![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-111111?style=for-the-badge&logo=amazonaws&logoColor=white)

**Data / Memory**

![CockroachDB](https://img.shields.io/badge/CockroachDB-111111?style=for-the-badge&logo=cockroachlabs&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-111111?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-111111?style=for-the-badge&logo=supabase&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-111111?style=for-the-badge)
![MongoDB](https://img.shields.io/badge/MongoDB-111111?style=for-the-badge&logo=mongodb&logoColor=white)

**Frontend / Product**

![Next.js](https://img.shields.io/badge/Next.js-111111?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-111111?style=for-the-badge&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-111111?style=for-the-badge&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-111111?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-111111?style=for-the-badge&logo=framer&logoColor=white)

**Tools / Infra**

![Git](https://img.shields.io/badge/Git-111111?style=for-the-badge&logo=git&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-111111?style=for-the-badge&logo=linux&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-111111?style=for-the-badge&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-111111?style=for-the-badge&logo=vercel&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-111111?style=for-the-badge&logo=nodedotjs&logoColor=white)

---

## Elsewhere On The Record

<!-- Hornet faces LEFT, so she sits on the RIGHT, looking back toward the text -->
<img align="right" src="assets/hornet.png" width="180" alt="Hornet" />

- **Smart India Hackathon 2025**, 6th nationally, leading a team of 6.
- **Hacksagon 2024**, 2nd place, Hardware Track.
- **MCP: Build Rich-Context AI Apps**, Anthropic.
- **Published writer**, CAMA Magazine (Canada). Poetry, performed to audiences of 350+.

Teaching math, English, and life skills to underprivileged children most weeks with the SGM social initiative. Ran logistics for a 1000+ attendee fest. The writing and the systems work are the same skill: breaking a complex thing down until nothing is left vague.

### Still Getting Wrong

- Finishing one strong project instead of starting five interesting ones. The list above is evidence both ways.
- DSA consistency, mostly so it stops being the thing that trips me up in interviews.
- Writing the limitations section before someone else finds it for me.

<br clear="right" />

---

## Links

<div align="center">

<a href="https://portfolio-sable-psi-56.vercel.app">
  <img src="https://img.shields.io/badge/portfolio-111111?style=for-the-badge&logo=vercel&logoColor=white" />
</a>
<a href="https://github.com/Somay-kousis">
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>
<a href="https://linkedin.com/in/somay-kousis-630ab1313">
  <img src="https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>
<a href="https://x.com/somaykousis">
  <img src="https://img.shields.io/badge/x-000000?style=for-the-badge&logo=x&logoColor=white" />
</a>

</div>

---

<div align="center">

<!-- demolab is the maintained domain for streak-stats; the old herokuapp host is
     unmaintained. github-readme-stats.vercel.app is DEPLOYMENT_PAUSED, so the
     stats and top-langs cards are replaced by the activity graph until it is
     either self-hosted or comes back. -->
<img height="160" src="https://streak-stats.demolab.com?user=Somay-kousis&theme=github-dark-blue&hide_border=true&background=0d1117&stroke=30363d&ring=ffffff&fire=ffffff&currStreakNum=ffffff&sideNums=8b949e&currStreakLabel=8b949e&sideLabels=8b949e&dates=30363d" />

<img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=Somay-kousis&custom_title=Contribution%20history&bg_color=0d1117&color=ffffff&line=8b949e&point=ffffff&area=true&area_color=30363d&hide_border=true" />

</div>

<div align="center">
<br />
<sub><code>valid_from 2024. no row here has been overwritten, only closed.</code></sub>
</div>

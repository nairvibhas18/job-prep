# Voice few-shots (mandatory)

Match this cadence. Concrete verb, specific tech, real problem, one number. Plain English. Do not sound like a keyword cloud or a systems-design doc.

Do **not** copy Amazon's density unless the target team is low-level systems/runtimes. Default voice = NeurIPS + Beautiful Together.

## NeurIPS / Algoverse (research voice)

- **Co-first author** of a paper accepted to **NeurIPS 2025** Mechanistic Interpretability (**MechInterp**) and New Perspectives in Graph ML (**NPGML**) Workshops.
- Designed a novel Hybrid Attribution and Pruning (HAP) framework that combines attribution patching with edge pruning to discover faithful LLM circuits **46% faster** than state-of-the-art methods.
- Implemented attribution scoring, pruning optimization, and evaluation pipelines in **PyTorch/TensorFlow**; used GPT-2 Small as a baseline model, with experiments run on NVIDIA H100 clusters (hosted on **Runpod**).

## Beautiful Together (product / systems voice)

- Facilitated adoption outcomes for **2,400+** animals by engineering a weighted preference matching algorithm that dynamically ranks candidates using real-time data scraped via **BeautifulSoup**.
- Built the full-stack application with a 10-member team using **React** (**Next.js**), holding code reviews and managing the end-to-end development lifecycle from database design to deployment.
- Automated production deployment on **Vercel** via **GitHub Actions**, and optimized database queries (**SQL**) for scalability and real-time reliability.

## Bolding (JSON `**span**` → LaTeX `\textbf`)

Copy this density from the base resumes. In `result.json` mark spans with `**double asterisks**`. Never write `\textbf{}` and never leave `**` in the PDF (the renderer converts them).

Bold:

- Metrics and counts: **78%**, **~50%**, **277**, **146**, **40%**, **under 3 seconds**, **10,000+**, **2,400+**, **46% faster**, **75,000+**, **68%**, **12,600+**
- Key technologies and named methods in that bullet: **Kotlin**, **AWS Lambda**, **Pydantic AI**, **Retrieval Augmented Generation**, **BeautifulSoup**, **React** (**Next.js**)
- Signature research phrases when they appear: **Co-first author**, **NeurIPS 2025**, **MechInterp**, **NPGML**

Do not bold whole clauses, verbs, or company names (headings are already bold). Typical bullet: 3–6 spans. A bullet may have none (LoSeR's forecasting bullet). When you keep a base bullet, keep its `**` marks. When you rewrite, re-mark the same classes of spans. New-project bullets follow the same pattern (**PyTorch**, **Docker**, a conservative metric such as **epsilon = 8**).

## Shape (XYZ / STAR) — structure only, not voice

Use the **XYZ formula**: accomplished **[X]** as measured by **[Y]**, by doing **[Z]**.

That is the resume form of **STAR** (Situation/Task compressed into the problem, Action = Z, Result = Y). Start with a strong action verb. Put tech in Z. Put numbers in Y. Do not write a four-sentence STAR story.

Same idea as: [Action verb] + [technical implementation] + [specific problem] + [measured impact]

Bad: "Built a chatbot using Python"

Good: "Engineered a FastAPI-based chatbot using **Retrieval-Augmented Generation (RAG)** over **10K+** documents, reducing internal search time by **40%**"

Shape references (do **not** copy these facts or add Hugging Face/React onto jobs that did not use them):

- Led front-end development of a core user onboarding feature using React and TypeScript, boosting daily active user engagement by 25% and reducing page load time by 15%.
- Fine-tuned a transformer-based LLM using PyTorch and Hugging Face, improving domain-specific response accuracy by 18% while cutting token inference latency by 35%.

Prefer **one or two metrics**, not a list. If two metrics, they must both be true (existing jobs: only metrics already on the base resume).

## Banned phrasing

leverage, utilize, cutting-edge, robust, synergistic, ground-breaking, passionate, excited to, proven track record, results-driven, "played a key role"

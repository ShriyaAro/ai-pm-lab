# AI PM Lab

Hands-on AI product work by [Shriya Arora](https://github.com/ShriyaAro), a product manager
in web analytics and measurement.

Each lab will take public data, label it by hand, run the same task on more than one model,
and end with a product decision: ship, don't ship, or ship with guardrails.

## How every lab works
1. **Data.** Public or synthetic, with its source and license.
2. **Labels.** A written rubric and my own pass/fail labels.
3. **Models.** The same task on at least two models: quality, cost per task, latency.
4. **Evals.** Error analysis first (failures grouped by cause), then automated checks or an
   LLM judge measured against my labels.
5. **Decision.** Ship, don't ship, or ship with guardrails, and what I would cut. Memos will live
   in [`decisions/`](decisions/).

## Labs
| # | Lab | Question | Status |
|---|---|---|---|
| 01 | Model playground | Which model and setting would I ship for a release-notes summary? | Planned |
| 02 | Docs assistant | Is a retrieval assistant over public analytics docs good enough for a beta? | Planned |
| 03 | Labeling and error analysis | Can an LLM judge replace my labels? | Planned |
| 04 | Cross-model ship decision | Which model ships, and with which guardrails? | Planned |
| Flagship | Site-search evals | An eval harness for site search on two models, with instrumentation and consent built in | Planned |
| 05 | Agent traces | Which agent failures block launch? | Planned |
| 06 | Privacy in traces | What can be logged, for how long, under what consent? | Planned |
| 07 | AI telemetry | When would I roll back? | Planned |
| 08 | Eval data pipeline | Can the pipeline give one trusted definition of "pass rate"? | Planned |
| 09 | Prompt experiment | Ship prompt A or B? | Planned |
| 10 | Agent traffic | How much of a site's traffic is AI agents, and what do they do? | Planned |

## Run a lab
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your own API keys; .env is never committed
```
Each lab folder will have its own README with rerun steps.

## Data and privacy
Public or synthetic data only. No employer data, internal names or customer information.
I redact traces that could hold personal data before committing them.

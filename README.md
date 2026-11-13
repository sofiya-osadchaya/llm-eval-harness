# LLM Evaluation Harness

демо-реконструкция подхода на синтетических данных

Provider-neutral evaluation contract with a five-criterion judge rubric and a separate deterministic
field-accuracy calculation. Only fictional towers and deliberately corrupted candidates are included.

```bash
pip install -r requirements.txt
python eval.py --dataset data/synthetic.jsonl
# Optional local server; model must already be installed:
python eval.py --dataset data/synthetic.jsonl --backend live --model qwen2.5:7b
```

See [measured mock report](reports/results.md) and [methodology](methodology.md).
Live LLM-as-a-judge code is provided but has not been executed in this package. Mock results do not
establish LLM quality. No employer benchmark is included. MIT.

# Dataset and rubric

Each JSONL record contains a unique ID, source_text, gold object and candidate object. Gold is
held separately from the live judge prompt to avoid leaking the answer. The mock baseline uses it.
Rubric: completeness, groundedness, schema compliance, numeric consistency, relevance; 0/1/2 each.

Exact field accuracy = matching required fields / all required fields. Unsupported claim rate =
unsupported atomic claims / all checked atomic claims. Extra claims must be counted by a live judge;
mock evaluation counts only required fields and therefore cannot measure arbitrary candidate additions.
The included fixtures have exactly two required fields. Do not compare field accuracy to span NER precision.

Keep dataset, prompt and model revisions with source hashes. For a real release, freeze a held-out set,
deduplicate before splitting, include prompt-injection and ambiguous examples, adjudicate all uncertain
cases and a random stratified sample with two human reviewers. Publish judgment coverage and disagreement.
Source-quote substring checks are necessary but do not prove entailment. No threshold is a measured result.
Live outputs need independent human audit; model scores are not ground truth.

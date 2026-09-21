# Industrial Equipment Troubleshooting Agent

Offline LangGraph agent for investigating compressor Air Production Unit failures using the MetroPT-3 dataset.

## Phase 1

Phase 1 builds the trustworthy data foundation:

1. Prepare the original MetroPT-3 CSV into Parquet.
2. Measure actual timestamp coverage and sampling gaps.
3. Query telemetry through DuckDB.
4. Keep the four company-reported failure windows as structured incident metadata.

The raw dataset is **not** committed to Git.

## Expected raw file

Place the official UCI file here:

```text
data/raw/MetroPT3(AirCompressor).csv
```

The UCI dataset page identifies that file as the MetroPT-3 data file. See the dataset documentation for attribution and license.

## Setup

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Prepare

```bash
python scripts/prepare_dataset.py \\
  --input "data/raw/MetroPT3(AirCompressor).csv" \\
  --output-dir "data/processed/metropt3"
```

## Inspect

```bash
python scripts/inspect_dataset.py
```

## Next phases

- deterministic troubleshooting tools
- LangGraph investigation loop
- hypothesis and critic nodes
- local technical RAG
- checkpointing / human approval
- FastAPI
- evaluation and UI

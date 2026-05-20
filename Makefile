generate:
	python scripts/generate_events.py

warehouse:
	python scripts/build_warehouse.py

quality:
	python scripts/run_quality_checks.py

pipeline:
	python orchestration/pipeline_flow.py

run-all:
	python run_pipeline.py
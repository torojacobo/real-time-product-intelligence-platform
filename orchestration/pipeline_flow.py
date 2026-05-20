from prefect import flow, task
import subprocess


@task
def generate_events():
    subprocess.run(
        ["python", "scripts/generate_events.py"],
        check=True
    )


@task
def build_warehouse():
    subprocess.run(
        ["python", "scripts/build_warehouse.py"],
        check=True
    )

@task
def build_retention_mart():
    subprocess.run(
        ["python", "scripts/build_retention_mart.py"],
        check=True
    )

@task
def build_anomaly_detection():

    subprocess.run(
        ["python", "scripts/build_anomaly_detection.py"],
        check=True
    )

@task
def run_quality_checks():
    subprocess.run(
        ["python", "scripts/run_quality_checks.py"],
        check=True
    )


@flow(name="product-intelligence-pipeline")
def product_intelligence_pipeline():

    generate_events()

    build_warehouse()

    build_retention_mart()

    build_anomaly_detection()

    run_quality_checks()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    product_intelligence_pipeline()
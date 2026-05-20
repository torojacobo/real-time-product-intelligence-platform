import subprocess
import sys


def run_step(step_name, command):

    print(f"\n=== Running: {step_name} ===")

    result = subprocess.run(
        command,
        shell=True
    )

    if result.returncode != 0:

        print(
            f"\nPipeline failed at step: {step_name}"
        )

        sys.exit(result.returncode)

    print(f"Completed: {step_name}")


def main():

    run_step(
        "Generate product events",
        "python scripts/generate_events.py"
    )

    run_step(
        "Build analytics warehouse",
        "python scripts/build_warehouse.py"
    )

    run_step(
        "Run quality checks",
        "python scripts/run_quality_checks.py"
    )

    run_step(
        "Run orchestration flow",
        "python orchestration/pipeline_flow.py"
    )

    print(
        "\nReal-Time Product Intelligence Pipeline completed successfully."
    )


if __name__ == "__main__":
    main()
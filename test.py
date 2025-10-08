import os
import subprocess
from pathlib import Path

os.environ.update(
    {
        "PGHOST": "localhost",
        "PGUSER": "postgres",
        "PGPASSWORD": "password",
        "PGDATABASE": "postgres",
    }
)

for problem_dir in sorted(Path("problems").iterdir()):
    print(f"{'👇' * 10} {problem_dir.name} {'👇' * 10}")

    for test_file in sorted(problem_dir.glob("test-*.sql")):
        print(f"📝 {test_file.stem}")

        # >>> clean up and migrate >>>
        subprocess.run(
            ["psql", "-qc", "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"],
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(["psql", "-qf", str(problem_dir / "schema.sql")])
        subprocess.run(["psql", "-qf", str(test_file)])
        # <<< clean up and migrate <<<

        for query_file in sorted(problem_dir.glob("query-*.sql")):
            # >>> run query >>>
            query_result = subprocess.run(
                ["psql", "-At", "-f", str(query_file)],
                capture_output=True,
                text=True,
            )
            # <<< run query <<<

            actual = query_result.stdout.strip()
            expected = test_file.with_suffix(".out").read_text().strip()

            if query_result.stderr.strip():
                error_msg = (
                    query_result.stderr.split("\n")[0].split("ERROR:")[1].strip()
                )
                print(f"{query_file.stem}: RE ({error_msg})")
            elif actual == expected:
                print(f"{query_file.stem}: AC")
            else:
                print(f"{query_file.stem}: WA (expected={expected}, actual={actual})")

    print()

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
    readme_file = problem_dir / "README.md"

    with open(readme_file, "w") as f:
        f.write(f"# {problem_dir.name}\n\n")

        schema_file = problem_dir / "schema.sql"
        f.write("## schema\n\n")
        f.write("```sql\n")
        f.write(schema_file.read_text())
        f.write("```\n\n")

        for test_file in sorted(problem_dir.glob("test-*.sql")):
            # >>> clean up and migrate >>>
            subprocess.run(
                ["psql", "-qc", "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"],
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(["psql", "-qf", str(problem_dir / "schema.sql")])
            subprocess.run(["psql", "-qf", str(test_file)])
            # <<< clean up and migrate <<<

            f.write(f"## {test_file.stem}\n\n")

            f.write("### data\n\n")
            f.write("```sql\n")
            f.write(test_file.read_text())
            f.write("```\n\n")

            expected_file = test_file.with_suffix(".out")

            f.write("### expected\n\n")
            f.write("```txt\n")
            f.write(expected_file.read_text())
            f.write("```\n\n")

            for query_file in sorted(problem_dir.glob("query-*.sql")):
                # >>> run query >>>
                query_result = subprocess.run(
                    ["psql", "-At", "-f", str(query_file)],
                    capture_output=True,
                    text=True,
                )
                # <<< run query <<<

                actual = query_result.stdout.strip()
                expected = expected_file.read_text().strip()

                f.write(f"### {query_file.stem}\n\n")
                f.write("```sql\n")
                f.write(query_file.read_text())
                f.write("```\n\n")

                f.write("<details>\n")
                f.write("<summary>result</summary>\n")
                if query_result.stderr.strip():
                    error_msg = (
                        query_result.stderr.split("\n")[0].split("ERROR:")[1].strip()
                    )
                    f.write(f"❌ RE: `{error_msg}`\n")
                elif actual == expected:
                    f.write("✅ AC\n")
                else:
                    f.write(f"❌ WA: expected `{expected}` but got `{actual}`\n")
                f.write("</details>\n\n")

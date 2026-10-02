"""
Script to test compilation and execution of all 23 C11 implementations using GCC.
"""
import os
import subprocess
import tempfile
from app.algorithms.c_sources import C_SOURCES

def test_all_c_implementations():
    print(f"Total C implementations to test: {len(C_SOURCES)}")
    assert len(C_SOURCES) == 23, f"Expected 23, got {len(C_SOURCES)}"

    results = []
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        for idx, (slug, c_code) in enumerate(C_SOURCES.items(), 1):
            c_file = os.path.join(tmpdir, f"{slug}.c")
            exe_file = os.path.join(tmpdir, f"{slug}.exe")

            with open(c_file, "w", encoding="utf-8") as f:
                f.write(c_code)

            # Compile with gcc -std=c11 -Wall -Wextra -pedantic
            cmd = ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic", c_file, "-o", exe_file, "-lm"]
            res = subprocess.run(cmd, capture_output=True, text=True)

            status = "PASS" if res.returncode == 0 else "FAIL"
            warnings = res.stderr.strip() if res.returncode == 0 and res.stderr else ""
            errors = res.stderr.strip() if res.returncode != 0 else ""

            # Try running the compiled executable
            runtime_output = ""
            if res.returncode == 0:
                try:
                    run_res = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                    runtime_output = run_res.stdout.splitlines()[0] if run_res.stdout else "Executed (no stdout)"
                except Exception as e:
                    runtime_output = f"Execution error: {e}"

            results.append({
                "num": idx,
                "slug": slug,
                "compile_status": status,
                "warnings": warnings,
                "errors": errors,
                "runtime_sample": runtime_output
            })

            print(f"[{idx:02d}/23] {slug:35s} -> Compile: {status} | Run: {runtime_output[:40]}")
            if warnings:
                print(f"       Warning: {warnings}")
            if errors:
                print(f"       Error: {errors}")

    all_passed = all(r["compile_status"] == "PASS" for r in results)
    print("\nSummary:")
    print(f"Total: {len(results)}, Passed: {sum(1 for r in results if r['compile_status'] == 'PASS')}, Failed: {sum(1 for r in results if r['compile_status'] != 'PASS')}")
    if all_passed:
        print("[SUCCESS] All 23 C11 implementations compiled and executed successfully!")
    else:
        print("[FAILURE] Some C implementations failed compilation.")

if __name__ == "__main__":
    test_all_c_implementations()

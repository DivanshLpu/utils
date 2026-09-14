from pathlib import Path
from datetime import datetime
import time


def reverse_changes(root_folder):

    start_time = time.perf_counter()
    start_datetime = datetime.now()

    root = Path(root_folder).resolve()
    result_file = root / "reverse_result.txt"

    scanned_files = 0
    scanned_folders = 0

    gitignore_restored = []
    gitkeep_restored = []

    skipped_files = []
    problems = []

    # ---------------------------------------------------------
    # Validate root
    # ---------------------------------------------------------

    if not root.exists():
        print(f"[ERROR] Folder does not exist: {root}")
        return

    if not root.is_dir():
        print(f"[ERROR] Not a directory: {root}")
        return

    print("=" * 70)
    print("             CODEBASE REVERSE TOOL")
    print("=" * 70)
    print(f"ROOT: {root}")
    print()

    # ---------------------------------------------------------
    # Recursive scan
    # ---------------------------------------------------------

    try:

        for path in root.rglob("*"):

            # Never touch .git
            if ".git" in path.parts:
                continue

            if path.is_dir():
                scanned_folders += 1
                continue

            if not path.is_file():
                continue

            scanned_files += 1

            relative_path = path.relative_to(root)

            print(f"[SCAN] {relative_path}")

            # =================================================
            # the-gitignore.txt -> .gitignore
            # =================================================

            if path.name == "the-gitignore.txt":

                new_path = path.parent / ".gitignore"

                # Don't overwrite an existing .gitignore
                if new_path.exists():

                    message = (
                        f"SKIPPED: {path}\n"
                        f"Reason: {new_path} already exists."
                    )

                    skipped_files.append(message)

                    print("[SKIP] Existing .gitignore")
                    continue

                try:

                    # Rename only.
                    # Content stays unchanged.
                    path.rename(new_path)

                    gitignore_restored.append({
                        "old": str(path),
                        "new": str(new_path)
                    })

                    print(
                        "[RESTORED] the-gitignore.txt\n"
                        f"         -> {new_path}"
                    )

                except Exception as e:

                    message = (
                        f"Could not restore {path}: {e}"
                    )

                    problems.append(message)

                    print(f"[ERROR] {message}")

            # =================================================
            # keepme.txt -> .gitkeep
            # =================================================

            elif path.name == "keepme.txt":

                new_path = path.parent / ".gitkeep"

                # Don't overwrite an existing .gitkeep
                if new_path.exists():

                    message = (
                        f"SKIPPED: {path}\n"
                        f"Reason: {new_path} already exists."
                    )

                    skipped_files.append(message)

                    print("[SKIP] Existing .gitkeep")
                    continue

                try:

                    # Delete the renamed file by renaming it first
                    # and then make its contents empty.
                    path.rename(new_path)

                    # Empty the file
                    new_path.write_text(
                        "",
                        encoding="utf-8"
                    )

                    gitkeep_restored.append({
                        "old": str(path),
                        "new": str(new_path)
                    })

                    print(
                        "[RESTORED] keepme.txt\n"
                        f"         -> {new_path}\n"
                        "         Content: EMPTY"
                    )

                except Exception as e:

                    message = (
                        f"Could not restore {path}: {e}"
                    )

                    problems.append(message)

                    print(f"[ERROR] {message}")

    except Exception as e:

        problems.append(
            f"Fatal scanning error: {e}"
        )

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    end_datetime = datetime.now()
    elapsed = time.perf_counter() - start_time

    minutes = int(elapsed // 60)
    seconds = elapsed % 60

    if minutes:
        time_taken = (
            f"{minutes} minute(s) "
            f"{seconds:.3f} second(s)"
        )
    else:
        time_taken = f"{seconds:.3f} second(s)"

    # ---------------------------------------------------------
    # Counts
    # ---------------------------------------------------------

    total_restored = (
        len(gitignore_restored)
        + len(gitkeep_restored)
    )

    # ---------------------------------------------------------
    # Final status
    # ---------------------------------------------------------

    if problems:
        final_status = "COMPLETED WITH PROBLEMS"

    elif skipped_files:
        final_status = "COMPLETED WITH SKIPPED FILES"

    else:
        final_status = "COMPLETED SUCCESSFULLY"

    # ---------------------------------------------------------
    # Build report
    # ---------------------------------------------------------

    report = []

    report.append("=" * 80)
    report.append("                 REVERSE PROCESSING REPORT")
    report.append("=" * 80)
    report.append("")

    report.append(f"Root folder      : {root}")
    report.append(f"Started          : {start_datetime}")
    report.append(f"Finished         : {end_datetime}")
    report.append(f"Time taken       : {time_taken}")
    report.append("")

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    report.append("-" * 80)
    report.append("FINAL STATUS")
    report.append("-" * 80)

    report.append(f"Status             : {final_status}")
    report.append(f"Files scanned      : {scanned_files}")
    report.append(f"Folders scanned    : {scanned_folders}")
    report.append(f"Total restored     : {total_restored}")
    report.append(
        f".gitignore restored: {len(gitignore_restored)}"
    )
    report.append(
        f".gitkeep restored  : {len(gitkeep_restored)}"
    )
    report.append(
        f"Skipped files      : {len(skipped_files)}"
    )
    report.append(
        f"Problems           : {len(problems)}"
    )
    report.append("")

    # ---------------------------------------------------------
    # Gitignore report
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append("GITIGNORE FILES RESTORED")
    report.append("=" * 80)

    if gitignore_restored:

        for item in gitignore_restored:

            report.append("")
            report.append("OLD PATH:")
            report.append(item["old"])

            report.append("")
            report.append("RESTORED PATH:")
            report.append(item["new"])

            report.append("")
            report.append(
                "CONTENT: PRESERVED"
            )

    else:

        report.append(
            "No the-gitignore.txt files were restored."
        )

    report.append("")

    # ---------------------------------------------------------
    # Gitkeep report
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append("GITKEEP FILES RESTORED")
    report.append("=" * 80)

    if gitkeep_restored:

        for item in gitkeep_restored:

            report.append("")
            report.append("OLD PATH:")
            report.append(item["old"])

            report.append("")
            report.append("RESTORED PATH:")
            report.append(item["new"])

            report.append("")
            report.append(
                "CONTENT: EMPTY"
            )

    else:

        report.append(
            "No keepme.txt files were restored."
        )

    report.append("")

    # ---------------------------------------------------------
    # Skipped
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append("SKIPPED FILES")
    report.append("=" * 80)

    if skipped_files:

        for item in skipped_files:

            report.append("")
            report.append(item)

    else:

        report.append("No files were skipped.")

    report.append("")

    # ---------------------------------------------------------
    # Problems
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append("PROBLEMS / ERRORS")
    report.append("=" * 80)

    if problems:

        for problem in problems:

            report.append("")
            report.append(problem)

    else:

        report.append(
            "No problems or errors occurred."
        )

    report.append("")

    # ---------------------------------------------------------
    # Final verification
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append("FINAL VERIFICATION")
    report.append("=" * 80)

    remaining_the_gitignore = []
    remaining_keepme = []

    try:

        for path in root.rglob("*"):

            if ".git" in path.parts:
                continue

            if not path.is_file():
                continue

            if path.name == "the-gitignore.txt":
                remaining_the_gitignore.append(str(path))

            elif path.name == "keepme.txt":
                remaining_keepme.append(str(path))

    except Exception as e:

        problems.append(
            f"Verification error: {e}"
        )

    report.append("")
    report.append(
        f"Remaining the-gitignore.txt: "
        f"{len(remaining_the_gitignore)}"
    )

    for path in remaining_the_gitignore:
        report.append(f"  {path}")

    report.append("")
    report.append(
        f"Remaining keepme.txt: "
        f"{len(remaining_keepme)}"
    )

    for path in remaining_keepme:
        report.append(f"  {path}")

    report.append("")

    if (
        not remaining_the_gitignore
        and not remaining_keepme
    ):

        report.append(
            "VERIFICATION: All renamed files were restored."
        )

    else:

        report.append(
            "VERIFICATION: Some renamed files remain."
        )

    report.append("")

    # ---------------------------------------------------------
    # Save report
    # ---------------------------------------------------------

    try:

        result_file.write_text(
            "\n".join(report),
            encoding="utf-8"
        )

    except Exception as e:

        print(
            f"[ERROR] Could not save "
            f"reverse_result.txt: {e}"
        )

        return

    # ---------------------------------------------------------
    # Console summary
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("                  REVERSE COMPLETE")
    print("=" * 70)

    print(f"Status            : {final_status}")
    print(f"Files scanned     : {scanned_files}")
    print(f"Folders scanned   : {scanned_folders}")
    print(f"Total restored    : {total_restored}")
    print(f".gitignore        : {len(gitignore_restored)}")
    print(f".gitkeep          : {len(gitkeep_restored)}")
    print(f"Skipped           : {len(skipped_files)}")
    print(f"Problems          : {len(problems)}")
    print(f"Time taken        : {time_taken}")
    print()
    print("Report:")
    print(result_file)
    print("=" * 70)


# =============================================================
# PROGRAM START
# =============================================================

if __name__ == "__main__":

    print()

    root_folder = input(
        "Enter ROOT folder of the codebase: "
    ).strip()

    if not root_folder:

        print("[ERROR] No folder entered.")

    else:

        process_codebase(root_folder)

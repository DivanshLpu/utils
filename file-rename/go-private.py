"""
this is python programme which rename evry .gitignore and .gitkeep text in root folder where ever this place 
this is usefull for saving all development files in github private repo 
running this fle before pushing to private repo 
"""


from pathlib import Path
from datetime import datetime
import time


def process_codebase(root_folder):
    start_time = time.perf_counter()
    start_datetime = datetime.now()

    root = Path(root_folder).resolve()
    result_file = root / "result.txt"

    scanned_files = 0
    scanned_folders = 0

    gitignore_changed = []
    gitkeep_changed = []

    skipped_files = []
    problems = []

    # ---------------------------------------------------------
    # Basic validation
    # ---------------------------------------------------------

    if not root.exists():
        print(f"[ERROR] Folder does not exist: {root}")
        return

    if not root.is_dir():
        print(f"[ERROR] Not a directory: {root}")
        return

    print("=" * 70)
    print("        CODEBASE COMPLETE ANALYSER")
    print("=" * 70)
    print(f"ROOT: {root}")
    print()

    # ---------------------------------------------------------
    # Start recursive scan
    # ---------------------------------------------------------

    try:

        for path in root.rglob("*"):

            # Never touch Git's internal directory
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

            # -------------------------------------------------
            # .gitignore
            # -------------------------------------------------

            if path.name == ".gitignore":

                new_path = path.parent / "the-gitignore.txt"

                if new_path.exists():
                    message = (
                        f".gitignore NOT changed: {path}\n"
                        f"Reason: {new_path} already exists"
                    )

                    print(f"[SKIP] {message}")

                    skipped_files.append(message)
                    continue

                try:

                    path.rename(new_path)

                    gitignore_changed.append({
                        "old": str(path),
                        "new": str(new_path)
                    })

                    print(
                        f"[CHANGED] {path}\n"
                        f"       -> {new_path}"
                    )

                except Exception as e:

                    message = f"Could not rename {path}: {e}"

                    problems.append(message)

                    print(f"[ERROR] {message}")

            # -------------------------------------------------
            # .gitkeep
            # -------------------------------------------------

            elif path.name == ".gitkeep":

                new_path = path.parent / "keepme.txt"

                if new_path.exists():
                    message = (
                        f".gitkeep NOT changed: {path}\n"
                        f"Reason: {new_path} already exists"
                    )

                    print(f"[SKIP] {message}")

                    skipped_files.append(message)
                    continue

                try:

                    # Rename
                    path.rename(new_path)

                    # Replace contents
                    new_path.write_text(
                        "hey please keep me",
                        encoding="utf-8"
                    )

                    gitkeep_changed.append({
                        "old": str(path),
                        "new": str(new_path)
                    })

                    print(
                        f"[CHANGED] {path}\n"
                        f"       -> {new_path}\n"
                        f"       Content: hey please keep me"
                    )

                except Exception as e:

                    message = f"Could not process {path}: {e}"

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
        time_taken = f"{minutes} minute(s) {seconds:.3f} second(s)"
    else:
        time_taken = f"{seconds:.3f} second(s)"

    # ---------------------------------------------------------
    # Final status
    # ---------------------------------------------------------

    total_changes = (
        len(gitignore_changed)
        + len(gitkeep_changed)
    )

    if problems:
        final_status = "COMPLETED WITH PROBLEMS"

    elif skipped_files:
        final_status = "COMPLETED WITH SKIPPED FILES"

    else:
        final_status = "COMPLETED SUCCESSFULLY"

    # ---------------------------------------------------------
    # Build result report
    # ---------------------------------------------------------

    report = []

    report.append("=" * 80)
    report.append("                 CODEBASE PROCESSING REPORT")
    report.append("=" * 80)
    report.append("")

    report.append(f"Root folder      : {root}")
    report.append(f"Started          : {start_datetime}")
    report.append(f"Finished         : {end_datetime}")
    report.append(f"Time taken       : {time_taken}")
    report.append("")

    report.append("-" * 80)
    report.append("FINAL STATUS")
    report.append("-" * 80)

    report.append(f"Status            : {final_status}")
    report.append(f"Files scanned     : {scanned_files}")
    report.append(f"Folders scanned   : {scanned_folders}")
    report.append(f"Total changes     : {total_changes}")
    report.append(f".gitignore changed: {len(gitignore_changed)}")
    report.append(f".gitkeep changed  : {len(gitkeep_changed)}")
    report.append(f"Skipped files     : {len(skipped_files)}")
    report.append(f"Problems          : {len(problems)}")
    report.append("")

    # ---------------------------------------------------------
    # .gitignore changes
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append(".GITIGNORE FILES CHANGED")
    report.append("=" * 80)

    if gitignore_changed:

        for item in gitignore_changed:

            report.append("")
            report.append(f"OLD PATH:")
            report.append(item["old"])
            report.append("")
            report.append(f"NEW PATH:")
            report.append(item["new"])

    else:
        report.append("No .gitignore files were changed.")

    report.append("")

    # ---------------------------------------------------------
    # .gitkeep changes
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append(".GITKEEP FILES CHANGED")
    report.append("=" * 80)

    if gitkeep_changed:

        for item in gitkeep_changed:

            report.append("")
            report.append("OLD PATH:")
            report.append(item["old"])
            report.append("")
            report.append("NEW PATH:")
            report.append(item["new"])
            report.append("")
            report.append("NEW CONTENT:")
            report.append("hey please keep me")

    else:
        report.append("No .gitkeep files were changed.")

    report.append("")

    # ---------------------------------------------------------
    # Skipped files
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
        report.append("No problems or errors occurred.")

    report.append("")

    # ---------------------------------------------------------
    # Verification
    # ---------------------------------------------------------

    report.append("=" * 80)
    report.append("FINAL VERIFICATION")
    report.append("=" * 80)

    remaining_gitignore = []
    remaining_gitkeep = []

    try:

        for path in root.rglob("*"):

            if ".git" in path.parts:
                continue

            if not path.is_file():
                continue

            if path.name == ".gitignore":
                remaining_gitignore.append(str(path))

            elif path.name == ".gitkeep":
                remaining_gitkeep.append(str(path))

    except Exception as e:

        problems.append(
            f"Verification error: {e}"
        )

    report.append("")

    report.append(
        f"Remaining .gitignore files: "
        f"{len(remaining_gitignore)}"
    )

    for path in remaining_gitignore:
        report.append(f"  {path}")

    report.append("")

    report.append(
        f"Remaining .gitkeep files: "
        f"{len(remaining_gitkeep)}"
    )

    for path in remaining_gitkeep:
        report.append(f"  {path}")

    report.append("")

    if not remaining_gitignore and not remaining_gitkeep:
        report.append(
            "VERIFICATION: No .gitignore or .gitkeep files remain."
        )
    else:
        report.append(
            "VERIFICATION: Some target files remain."
        )

    report.append("")

    # ---------------------------------------------------------
    # Save result.txt
    # ---------------------------------------------------------

    try:

        result_file.write_text(
            "\n".join(report),
            encoding="utf-8"
        )

    except Exception as e:

        print(f"[ERROR] Could not save result.txt: {e}")
        return

    # ---------------------------------------------------------
    # Final console output
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("                    COMPLETE")
    print("=" * 70)

    print(f"Status          : {final_status}")
    print(f"Files scanned   : {scanned_files}")
    print(f"Folders scanned : {scanned_folders}")
    print(f"Changes         : {total_changes}")
    print(f"Skipped         : {len(skipped_files)}")
    print(f"Problems        : {len(problems)}")
    print(f"Time taken      : {time_taken}")
    print()
    print(f"Report saved to:")
    print(result_file)
    print("=" * 70)


# =============================================================
# PROGRAM START
# =============================================================

if __name__ == "__main__":

    print()
    root_folder = input(
        "Enter ROOT folder of your codebase: "
    ).strip()

    if not root_folder:
        print("ERROR: No folder entered.")
    else:
        process_codebase(root_folder)

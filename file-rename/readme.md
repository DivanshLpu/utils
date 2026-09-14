# Codebase Git File Tools

A small Python utility collection for recursively processing `.gitignore` and `.gitkeep` files across an entire codebase.

The tools are designed to work from a **project root** and recursively search every folder and subfolder.

## Files

```text
.
├── go-public.py
├── go-private.py
└── README.md
```

### `go-public.py`

Recursively scans the complete project and:

```text
.gitignore  →  the-gitignore.txt
.gitkeep    →  keepme.txt
```

For every `.gitkeep` file that is renamed, its contents are replaced with:

```text
hey please keep me
```

It also generates a detailed:

```text
result.txt
```

The report contains:

* Root directory scanned
* Start and finish time
* Total execution time
* Number of folders scanned
* Number of files scanned
* Every `.gitignore` changed
* Every `.gitkeep` changed
* Exact old and new paths
* Skipped files
* Errors and problems
* Final verification
* Remaining `.gitignore` / `.gitkeep` files

The `.git` directory is skipped to avoid modifying Git's internal files.

---

### `go-private.py`

Reverses the changes made by `go-public.py`.

It recursively searches the complete project and:

```text
the-gitignore.txt  →  .gitignore
keepme.txt         →  .gitkeep
```

For `.gitignore` files, the existing content is preserved.

For `.gitkeep` files, the restored file is intentionally created as an **empty file**.

It generates:

```text
reverse_result.txt
```

containing:

* Execution time
* Files and folders scanned
* `.gitignore` files restored
* `.gitkeep` files restored
* Exact old and new paths
* Skipped files
* Errors
* Final verification
* Any renamed files that remain

---

## Basic Usage

Open a terminal in the directory containing the Python scripts.

### Make the codebase public

Run:

```bash
python go-public.py
```

Enter the root directory of your project:

```text
Enter ROOT folder of your codebase: D:\Projects\MyProject
```

The program recursively processes the entire project.

Example:

```text
MyProject/
├── .gitignore
├── backend/
│   ├── .gitkeep
│   └── src/
│       └── database/
│           └── .gitkeep
└── frontend/
    ├── .gitignore
    └── src/
        └── components/
            └── .gitkeep
```

After running `go-public.py`:

```text
MyProject/
├── the-gitignore.txt
├── backend/
│   ├── keepme.txt
│   └── src/
│       └── database/
│           └── keepme.txt
└── frontend/
    ├── the-gitignore.txt
    └── src/
        └── components/
            └── keepme.txt
```

---

## Restore the Codebase

Run:

```bash
python go-private.py
```

Enter the same project root.

The files are restored:

```text
the-gitignore.txt  →  .gitignore
keepme.txt         →  .gitkeep
```

The restored `.gitkeep` files are empty.

---

## Why Rename These Files?

`.gitignore` has a special meaning to Git.

If a project is uploaded somewhere where you don't want Git's ignore rules to be interpreted normally, renaming:

```text
.gitignore
```

to:

```text
the-gitignore.txt
```

turns it into an ordinary text file.

Similarly:

```text
.gitkeep
```

becomes:

```text
keepme.txt
```

This is useful for certain code-sharing, packaging, archival, or automated processing workflows.

---

## Important Warning

This tool **does not make a repository truly public or private**.

`go-public.py` only changes the filenames described above.

It does **not**:

* Change GitHub repository visibility
* Change GitLab repository visibility
* Remove Git history
* Remove secrets from Git history
* Remove passwords or API keys
* Remove `.env` files
* Remove private source code
* Change repository permissions
* Push or pull anything from Git
* Modify the `.git` directory

Renaming `.gitignore` also means Git will no longer automatically use that file as an ignore file.

Therefore, check your project carefully before committing or publishing it.

---

## Safety

The scripts intentionally skip:

```text
.git/
```

This is important because `.git` contains Git's internal repository data.

The scripts also avoid overwriting an existing target file.

For example, if:

```text
the-gitignore.txt
```

exists and:

```text
.gitignore
```

also exists, the reverse script will skip the operation rather than overwrite `.gitignore`.

Likewise, an existing:

```text
.gitkeep
```

will not be overwritten by `go-private.py`.

---

## Recursive Processing

The scripts don't only check the root directory.

They recursively search:

```text
root/
├── folder/
│   ├── folder/
│   │   ├── folder/
│   │   │   └── target file
│   │   └── target file
│   └── target file
└── target file
```

There is no fixed folder depth.

Every accessible subdirectory is scanned.

---

## Reports

### Public operation

```text
result.txt
```

### Reverse operation

```text
reverse_result.txt
```

These reports are intended to make the operation auditable.

They record what happened instead of simply saying:

```text
Done.
```

For example:

```text
Files scanned     : 842
Folders scanned   : 126
Total changes     : 7
.gitignore        : 3
.gitkeep          : 4
Skipped           : 0
Problems          : 0
Time taken        : 1.359 seconds
```

---

## Requirements

Python 3.8+ is recommended.

No external Python packages are required.

The scripts use Python's standard library:

```python
pathlib
datetime
time
```

---

## Typical Workflow

```text
                 PROJECT
                    │
                    ▼
             go-public.py
                    │
                    ▼
       Rename special Git files
                    │
                    ▼
              result.txt
                    │
                    ▼
           Share / Package / Archive
                    │
                    ▼
             go-private.py
                    │
                    ▼
          Restore Git filenames
                    │
                    ▼
        reverse_result.txt
```

---

## Limitations

`go-private.py` can restore the **contents of `.gitignore`** because `go-public.py` only renamed those files.

However, `.gitkeep` contents cannot be recovered.

`go-public.py` intentionally replaces the original `.gitkeep` contents with:

```text
hey please keep me
```

Therefore, `go-private.py` restores `.gitkeep` as an empty file.

If the original `.gitkeep` contained important information, that information is not recoverable by `go-private.py`.

---

## License

Use, modify, and learn from these scripts as you wish.

This is a simple utility project intended primarily for experimentation, learning, and practical codebase management.

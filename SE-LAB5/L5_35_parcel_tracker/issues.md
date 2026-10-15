# Lab 5: Static Code Analysis — Issues and Fixes

| Issue | Type | Original Location | Description | Fix Applied |
|---|---|---|---|---|
| Mutable default argument | Code quality / Bug | `bookParcel()` | Using `history=[]` could share the same list across function calls. | Changed the default to `None` and initialized a new list inside the function. |
| Inconsistent naming conventions | Code style | Multiple functions | CamelCase function names and variable names reduced consistency with Python conventions. | Changed names to snake_case. |
| Broad exception handling | Code quality | `trackParcel()` | Catching `Exception` could hide unexpected errors. | Changed to catch `KeyError` specifically. |
| Unsafe temporary-file creation | Security | `labelPath()` | `tempfile.mktemp()` can introduce a race condition. | Replaced it with `tempfile.NamedTemporaryFile()`. |
| Shell command execution | Security | `pingHub()` | Using `shell=True` with constructed input could allow command injection. | Removed the unused `ping_hub()` helper and its subprocess dependency. |
| Insecure OTP generation | Security | OTP generation in `main()` | `random.randint()` is not intended for security-sensitive random values. | Replaced it with `secrets.randbelow()`. |
| Missing documentation | Code quality | Module and functions | Missing docstrings made the code harder to understand. | Added module and function docstrings. |
| Formatting violations | Code style | Multiple lines | Missing whitespace, inline-comment spacing and blank lines violated style guidelines. | Corrected formatting and verified using Flake8. |

## Verification

- Pylint final score: 10.00/10
- Flake8 final result: No reported issues
- Bandit final result: No issues identified
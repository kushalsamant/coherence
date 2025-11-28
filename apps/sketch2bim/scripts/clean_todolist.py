import os
import re
from typing import List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INPUT_FILE = os.path.join(REPO_ROOT, "todolist.txt")
OUTPUT_FILE = os.path.join(REPO_ROOT, "todolist.cleaned.txt")


def compile_patterns() -> Tuple[re.Pattern, re.Pattern, List[re.Pattern]]:
    # Allowlist: anything clearly related to the project or tech stack
    allow_keywords = [
        r"\bfrontend\/", r"\bbackend\/", r"\bcomponents\/", r"\bapp\/",
        r"\.(ts|tsx|py|json|md)\b", r"\bIFC\b", r"\bIfc[A-Za-z]*\b", r"\bBIM\b",
        r"\bSketch2BIM\b", r"\bviewer\b", r"\bexporter\b", r"\bfilter\b",
        r"\bmesh\b", r"\bgeometry\b", r"\bThree\.js\b", r"\bweb-ifc\b",
        r"\bifcjs\b", r"\bOpenBIM\b", r"\bRevit\b", r"\bIfc(Property|Spatial|GUID)\b",
        r"\bTypeScript\b", r"\bReact\b", r"\bNext\.js\b", r"\bFastAPI\b",
        r"\bPydantic\b", r"\buvicorn\b", r"\bmiddleware\b", r"\bOpenAPI\b",
        r"\bCORS\b", r"\bpytest\b",
        # Common code-like tokens
        r"`[^`]+`", r"\bclass\s+\w+", r"\bdef\s+\w+", r"\bfunction\s+\w+",
        r"import\s+\w+", r"from\s+[\w\.]+", r"\bconst\b", r"\blet\b", r"\binterface\b",
    ]
    allow_re = re.compile("|".join(allow_keywords), re.IGNORECASE)

    # Exclude patterns (heuristics)
    exclude_keywords = [
        r"https?://", r"\bwww\.",  # URLs
        r"\bMeeting\b", r"\bAgenda\b", r"\bZoom\b", r"\bCalendar\b",
        r"\bCall\b", r"\bSchedule\b",
        r"\bSEO\b", r"\bWordPress\b", r"\bPhotoshop\b",
        # Long noise without code-like tokens will be handled separately
    ]
    exclude_re = re.compile("|".join(exclude_keywords), re.IGNORECASE)

    # Special-case patterns checked individually
    special_excludes = [
        re.compile(r"^- \[ \]\s*(?!.*(IFC|Ifc|BIM|Sketch2BIM|frontend|backend|\.ts|\.tsx|\.py)).*$", re.IGNORECASE),
        re.compile(r"[A-Za-z0-9+\/]{80,}={0,2}"),  # base64-ish long tokens
        re.compile(r"(?:[\U0001F300-\U0001FAFF\U00002700-\U000027BF]){3,}"),  # many emojis
    ]

    return allow_re, exclude_re, special_excludes


def looks_noisy_long_line(line: str) -> bool:
    if len(line) < 150:
        return False
    # Consider it noisy if no code-like tokens are present
    code_tokens = re.search(r"[\{\}\[\]\(\);]|`[^`]+`|\b(if|for|while|class|def|const|let|function)\b", line)
    return code_tokens is None


def high_non_ascii_ratio(line: str, threshold: float = 0.7) -> bool:
    if not line:
        return False
    non_ascii = sum(1 for ch in line if ord(ch) > 127)
    return (non_ascii / max(1, len(line))) > threshold


def should_keep_line(line: str, allow_re: re.Pattern, exclude_re: re.Pattern, special_excludes: List[re.Pattern]) -> bool:
    # Always keep if clearly allowed
    if allow_re.search(line):
        return True

    # Exclude if matches exclude and not allowed
    if exclude_re.search(line):
        return False

    for pat in special_excludes:
        if pat.search(line):
            return False

    if looks_noisy_long_line(line):
        return False

    if high_non_ascii_ratio(line):
        return False

    # Keep lines that have alphanumerics to avoid stripping too aggressively
    if re.search(r"[A-Za-z0-9]", line):
        return True

    # Otherwise, keep as is (blank lines will be collapsed later)
    return True


def collapse_blank_runs(lines: List[str]) -> List[str]:
    result: List[str] = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 1:
                result.append("")
        else:
            blank_run = 0
            result.append(line.rstrip())
    # Ensure trailing newline at file end
    if result and result[-1] != "":
        result.append("")
    return result


def main() -> None:
    allow_re, exclude_re, special_excludes = compile_patterns()

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    kept: List[str] = []
    removed_samples: List[str] = []
    total = 0
    removed = 0

    with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            total += 1
            keep = should_keep_line(line, allow_re, exclude_re, special_excludes)
            if keep:
                kept.append(line)
            else:
                removed += 1
                if len(removed_samples) < 10:
                    removed_samples.append(line)

    kept = collapse_blank_runs(kept)

    with open(OUTPUT_FILE, "w", encoding="utf-8", errors="replace") as f:
        f.write("\n".join(kept))

    print(f"[todolist cleaner] Total lines: {total}")
    print(f"[todolist cleaner] Kept lines:  {total - removed}")
    print(f"[todolist cleaner] Removed:     {removed}")
    if removed_samples:
        print("[todolist cleaner] Sample removed lines:")
        for i, s in enumerate(removed_samples, 1):
            # Safely display up to 200 chars for readability
            display = s if len(s) <= 200 else s[:197] + "..."
            print(f"  {i:2d}. {display}")


if __name__ == "__main__":
    main()



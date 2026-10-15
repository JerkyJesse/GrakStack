#!/usr/bin/env python3
"""claims_check.py - the claims gate for the grakstack tree.

Gates six claims against the tree: commands (six command files, each with a
front-matter description and a trailing <!-- grakstack-owned --> marker, and
their names in the README command table and in both installers' lists),
hosts (setup.ps1's $AllHosts / $AutoHosts vs the README hosts table, both
directions), curriculum (setup.ps1's $CurriculumFields vs the curriculum/*.md
stems), support (the support set in both installers' lists and in
rock_memory.py's SOURCES), pointers (standard.md / scenes.md / scorer.py
mentions in grak-agent.md, digest.md, and README.md), and boundary (the
banned sibling /
trading-machinery terms swept over characters/grak/**, README.md, and
AGENTS.md only; tools/, .github/, docs/ are exempt: this script and CI carry
the lists).

Modes: --check audits --root (default: the repo root inferred from this
script's location) and exits 0 only when all sections pass; --self-test
builds a fixture tree in a temp dir (never the live tree), proves it green,
then proves one mutation per section flips its own section red, and exits 0
only when the clean fixture is green and every mutation flips.

Stdlib only. No network. UTF-8. Cross-platform.
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

COMMANDS = ("plan", "grak", "review", "team", "ship", "land")
CURRICULUM = (
    "grammar logic rhetoric arithmetic geometry music astronomy finance economics".split()
)
SUPPORT_SET = (
    ("GRAK.md", "characters/grak/GRAK.md"),
    ("GRAK_CREDENTIALS.md", "characters/grak/credentials/GRAK_CREDENTIALS.md"),
    ("exam.py", "characters/grak/credentials/exam.py"),
    ("mcq_bank.json", "characters/grak/credentials/mcq_bank.json"),
    *(("%s.md" % name, "characters/grak/curriculum/%s.md" % name) for name in CURRICULUM),
    ("standard.md", "characters/grak/standard.md"),
    ("scenes.md", "characters/grak/scenes.md"),
    ("scorer.py", "characters/grak/scorer.py"),
)
BANNED_SIBLING = (
    "waifu", "waifustack", "mechapip", "reika", "mei", "elo", "yui",
    "niko", "rin", "aria", "the house",
)
BANNED_TRADING = (
    "kalshi", "kxbtc", "kxeth", "kxgold", "kxsilver", "fleet", "perps",
    "tradingideas", "ship_wave", "strategy_proof", "edge_report",
    "paper_account", "probe_",
)
POINTER_FILES = ("characters/grak/grak-agent.md", "characters/grak/digest.md", "README.md")
POINTER_TERMS = ("standard.md", "scenes.md", "scorer.py")
FIXTURE_SUPPORT = (
    "characters/grak/GRAK.md",
    "characters/grak/credentials/GRAK_CREDENTIALS.md",
    "characters/grak/credentials/exam.py",
    "characters/grak/credentials/mcq_bank.json",
    "characters/grak/standard.md",
    "characters/grak/scenes.md",
    "characters/grak/scorer.py",
)

def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

def rel(root, path):
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)

def frontmatter_value(text, key):
    if not text.startswith("---"):
        return None
    block = text.split("\n---", 1)[0]
    for line in block.splitlines()[1:]:
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip() or None
    return None

def last_content_line(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-1] if lines else ""

def parse_bash_var(text, var):
    pattern = re.compile(r"^" + re.escape(var) + r"=[\"']([^\"']*)[\"']")
    tokens, lineno = [], None
    for index, line in enumerate(text.splitlines(), 1):
        match = pattern.match(line)
        if match:
            tokens, lineno = match.group(1).split(), index
    return tokens, lineno

def parse_ps1_array(text, var):
    match = re.search(r"\$" + re.escape(var) + r"\s*=\s*@\((.*?)\)", text, re.S)
    if not match:
        return None, None
    lineno = text[: match.start()].count("\n") + 1
    return re.findall(r"\"([^\"]+)\"", match.group(1)), lineno

def parse_bash_support(text):
    names = set()
    pattern = re.compile(r"^([A-Z][A-Z0-9_]*)=[\"']([^\"']*)[\"']")
    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        var, value = match.group(1), match.group(2)
        if var == "CURRICULUM_FIELDS":
            names.update(token + ".md" for token in value.split())
        elif "SUPPORT" in var:
            names.update(value.split())
    return names

def parse_ps1_support(text):
    names = set()
    match = re.search(r"\$SupportFiles\s*=\s*@\((.*?)\n\)", text, re.S)
    tokens = re.findall(r"\"([^\"]+)\"", match.group(1)) if match else []
    tokens += [m.group(1) for m in re.finditer(r"Dst\s*=\s*\"([^\"]+)\"", text)]
    for token in tokens:
        base = token.replace("\\", "/").rsplit("/", 1)[-1]
        if base.endswith((".md", ".py", ".json")):
            names.add(base)
    return names

def parse_sources(text):
    match = re.search(r"SOURCES\s*=\s*\((.*?)\n\)", text, re.S)
    return set(re.findall(r"\"([^\"]+)\"", match.group(1))) if match else set()

def parse_readme_hosts(text):
    hosts, active = [], False
    for index, line in enumerate(text.splitlines(), 1):
        if re.match(r"^#{1,3}\s+hosts?\b", line.strip(), re.IGNORECASE):
            active = True
            continue
        if active and line.startswith("## "):
            break
        if not active or not line.startswith("|"):
            continue
        first = line.strip().strip("|").split("|", 1)[0].strip().lower()
        if first != "host":
            hosts.extend((token, index) for token in re.split(r"[^a-z0-9-]+", first)
                         if re.fullmatch(r"[a-z][a-z0-9-]*", token))
    return hosts

def banned_pattern(term):
    body = re.escape(term).replace(r"\ ", r"\s+")
    if term.endswith("_"):
        return re.compile(r"(?<![A-Za-z0-9_])" + body, re.IGNORECASE)
    return re.compile(r"(?<![A-Za-z0-9_])" + body + r"(?![A-Za-z0-9_])", re.IGNORECASE)

def scan_terms(path, patterns):
    try:
        data = path.read_bytes()
    except OSError:
        return []
    if b"\x00" in data[:8192]:
        return []
    hits = []
    for lineno, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
        for term, pattern in patterns:
            if pattern.search(line):
                hits.append((lineno, term))
    return hits

def check_commands(root):
    checks = []
    command_dir = root / "characters" / "grak" / "commands"
    for name in COMMANDS:
        path = command_dir / (name + ".md")
        where = rel(root, path)
        if not path.is_file():
            checks.append((False, "commands: missing " + where))
            continue
        text = read_text(path)
        checks.append((bool(frontmatter_value(text, "description")),
                       "commands: " + where + " missing front-matter description key"))
        checks.append((last_content_line(text) == "<!-- grakstack-owned -->",
                       "commands: " + where + " missing the trailing <!-- grakstack-owned --> marker"))
    if command_dir.is_dir():
        extras = [p.name for p in sorted(command_dir.glob("*.md")) if p.stem not in COMMANDS]
        checks.extend((False, "commands: unexpected " + rel(root, command_dir / e)) for e in extras)
        if not extras:
            checks.append((True, "command dir holds exactly the six files"))
    else:
        checks.append((False, "commands: missing directory " + rel(root, command_dir)))
    lines = read_text(root / "README.md").splitlines()
    header = next((i for i, line in enumerate(lines, 1) if re.match(r"^\|\s*Command\s*\|", line, re.I)), None)
    for name in COMMANDS:
        found = any(re.search(r"\|\s*`/" + re.escape(name) + r"(?:`|\s)", line) for line in lines)
        checks.append((found, "commands: " + ("README.md:%d" % header if header else "README.md")
                       + " missing /" + name + " in the command table"))
    tokens, lineno = parse_bash_var(read_text(root / "setup"), "COMMANDS")
    for name in COMMANDS:
        checks.append((name in tokens, "commands: " + ("setup:%d" % lineno if lineno else "setup")
                       + " missing " + name + " in the COMMANDS list"))
    name_tokens, ps1_line = parse_ps1_array(read_text(root / "setup.ps1"), "Commands")
    for name in COMMANDS:
        checks.append((bool(name_tokens) and name in name_tokens,
                       "commands: " + ("setup.ps1:%d" % ps1_line if ps1_line else "setup.ps1")
                       + " missing " + name + " in the $Commands list"))
    return checks

def check_hosts(root):
    checks = []
    ps1_text = read_text(root / "setup.ps1")
    all_hosts, all_line = parse_ps1_array(ps1_text, "AllHosts")
    auto_hosts, _ = parse_ps1_array(ps1_text, "AutoHosts")
    if all_hosts is None:
        checks.append((False, "hosts: setup.ps1 $AllHosts array not found"))
        all_hosts = []
    if auto_hosts is None:
        checks.append((False, "hosts: setup.ps1 $AutoHosts array not found"))
        auto_hosts = []
    readme_rows = parse_readme_hosts(read_text(root / "README.md"))
    names = {n for n, _ in readme_rows}
    if not readme_rows:
        checks.append((False, "hosts: README.md hosts table not found"))
    for host in sorted(set(all_hosts) | set(auto_hosts)):
        checks.append((host in names,
                       "hosts: setup.ps1:%d lists %s; README.md hosts table does not" % (all_line or 1, host)))
    for host, lineno in readme_rows:
        checks.append((host in set(all_hosts),
                       "hosts: README.md:%d names %s; setup.ps1 $AllHosts does not accept it" % (lineno, host)))
    return checks

def check_curriculum(root):
    fields, lineno = parse_ps1_array(read_text(root / "setup.ps1"), "CurriculumFields")
    if fields is None:
        return [(False, "curriculum: setup.ps1 $CurriculumFields array not found")]
    checks = []
    curriculum_dir = root / "characters" / "grak" / "curriculum"
    if not curriculum_dir.is_dir():
        checks.append((False, "curriculum: missing directory " + rel(root, curriculum_dir)))
    stems = {path.stem for path in curriculum_dir.glob("*.md")}
    for field in fields:
        checks.append((field in stems, "curriculum: setup.ps1:%d lists %s; characters/grak/curriculum/%s.md is missing"
                       % (lineno or 1, field, field)))
    for stem in sorted(stems):
        checks.append((stem in set(fields),
                       "curriculum: characters/grak/curriculum/%s.md has no entry in setup.ps1 $CurriculumFields" % stem))
    return checks

def check_support(root):
    checks = []
    bash_names = parse_bash_support(read_text(root / "setup"))
    ps1_text = read_text(root / "setup.ps1")
    ps1_names = parse_ps1_support(ps1_text)
    ps1_fields, _ = parse_ps1_array(ps1_text, "CurriculumFields")
    ps1_fields = set(ps1_fields or [])
    sources = parse_sources(read_text(root / "characters" / "grak" / "rock_memory.py"))
    for name, repo_path in SUPPORT_SET:
        stem = name[:-3] if name.endswith(".md") else None
        checks.append((name in bash_names, "support: " + name + " missing from setup SUPPORT_FILES"))
        checks.append((name in ps1_names or (stem is not None and stem in ps1_fields),
                       "support: " + name + " missing from setup.ps1 $SupportFiles"))
        checks.append((repo_path in sources, "support: " + repo_path + " missing from rock_memory.py SOURCES"))
    return checks

def check_pointers(root):
    checks = []
    for rel_path in POINTER_FILES:
        text = read_text(root / rel_path)
        for term in POINTER_TERMS:
            checks.append((term in text, "pointers: " + rel_path + " missing mention of " + term))
    return checks

def check_boundary(root):
    patterns = [(term, banned_pattern(term)) for term in BANNED_SIBLING + BANNED_TRADING]
    targets = [root / "README.md", root / "AGENTS.md"]
    grak_dir = root / "characters" / "grak"
    if grak_dir.is_dir():
        targets.extend(sorted(path for path in grak_dir.rglob("*") if path.is_file()))
    hits = []
    for path in targets:
        for lineno, term in scan_terms(path, patterns):
            hits.append("%s:%d: %s" % (rel(root, path), lineno, term))
    return [(False, "boundary: " + hit) for hit in hits] or [(True, "boundary: no banned terms in scope")]

def run_checks(root):
    return {
        "commands": check_commands(root),
        "hosts": check_hosts(root),
        "curriculum": check_curriculum(root),
        "support": check_support(root),
        "pointers": check_pointers(root),
        "boundary": check_boundary(root),
    }

def failed_sections(results):
    return {name for name, checks in results.items() if any(not ok for ok, _ in checks)}

def run_check(root):
    if not root.is_dir():
        print("claims_check: root not found: %s" % root)
        return 1
    results = run_checks(root)
    ok_count = fail_count = 0
    print("claims_check: root %s" % root)
    for name, checks in results.items():
        fails = [message for ok, message in checks if not ok]
        ok_count += len(checks) - len(fails)
        fail_count += len(fails)
        for message in fails:
            print("FAIL " + message)
        print("FAIL %s: %d of %d checks failed" % (name, len(fails), len(checks)) if fails
              else "ok %s: %d checks" % (name, len(checks)))
    print("claims_check: %d ok / %d fail" % (ok_count, fail_count))
    return 0 if fail_count == 0 else 1

def base_fixture():
    files = {}
    for name in COMMANDS:
        files["characters/grak/commands/%s.md" % name] = (
            '---\ndescription: "%s command"\n---\n\n%s body.\n\n<!-- grakstack-owned -->\n' % (name, name))
    for name in CURRICULUM:
        files["characters/grak/curriculum/%s.md" % name] = "# %s\n" % name
    for rel_path in FIXTURE_SUPPORT:
        files[rel_path] = "# fixture\n"
    files["characters/grak/grak-agent.md"] = "Fixture agent. See standard.md, scenes.md, and scorer.py.\n"
    files["characters/grak/digest.md"] = "Fixture digest. See standard.md, scenes.md, and scorer.py.\n"
    entries = ",\n".join('  @{ Src = Join-Path $Root "characters\\grak\\%s"; Dst = "%s" }'
                         % (p[len("characters/grak/"):].replace("/", "\\"), p.rsplit("/", 1)[-1])
                         for p in FIXTURE_SUPPORT)
    files["setup.ps1"] = (
        "$Commands = @(%s)\n" % ", ".join('"%s"' % n for n in COMMANDS)
        + "$CurriculumFields = @(%s)\n" % ", ".join('"%s"' % n for n in CURRICULUM)
        + '$AllHosts = @("claude", "opencode")\n$AutoHosts = @("claude", "opencode")\n'
        + "$SupportFiles = @(\n" + entries + "\n)\n")
    files["setup"] = (
        'COMMANDS="%s"\n' % " ".join(COMMANDS)
        + 'SUPPORT_FILES="GRAK.md GRAK_CREDENTIALS.md exam.py mcq_bank.json standard.md scenes.md scorer.py"\n'
        + 'CURRICULUM_FIELDS="%s"\n' % " ".join(CURRICULUM))
    files["characters/grak/rock_memory.py"] = "SOURCES = (\n%s\n)\n" % "\n".join(
        '    "%s",' % p for _, p in SUPPORT_SET)
    files["README.md"] = (
        "## Commands\n\n| Command | Does |\n|---|---|\n%s\n\n" % "\n".join("| `/%s` | Fixture. |" % n for n in COMMANDS)
        + "## Hosts\n\n| Host | Grak lands at |\n|---|---|\n| claude | fixture |\n| opencode | fixture |\n\n"
        + "Pointers: standard.md, scenes.md, and scorer.py.\n")
    return files

def write_fixture(root, files):
    for rel_path, text in files.items():
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))

MUTATION_NAMES = ("commands", "hosts", "curriculum", "support", "pointers", "boundary")

def mutated_fixture(name):
    files = base_fixture()
    if name == "commands":
        files["characters/grak/commands/plans.md"] = files.pop("characters/grak/commands/plan.md")
    elif name == "hosts":
        files["setup.ps1"] = files["setup.ps1"].replace('$AllHosts = @("claude", "opencode")', '$AllHosts = @("opencode")')
    elif name == "curriculum":
        files["characters/grak/curriculum/grammer.md"] = files.pop("characters/grak/curriculum/grammar.md")
    elif name == "support":
        files["setup"] = files["setup"].replace(" scenes.md scorer.py", " scenes.md")
    elif name == "pointers":
        files["characters/grak/digest.md"] = files["characters/grak/digest.md"].replace("scorer.py", "the scorer")
    elif name == "boundary":
        files["characters/grak/digest.md"] += "waifu\n"
    return files

def self_test():
    base = base_fixture()
    problems = 0
    with tempfile.TemporaryDirectory(prefix="claims-check-") as tmp:
        root = Path(tmp) / "clean"
        write_fixture(root, base)
        failed = failed_sections(run_checks(root))
        if failed:
            print("self-test: clean fixture is NOT green: " + ", ".join(sorted(failed)))
            problems += 1
        else:
            print("self-test: clean fixture green (6/6 sections)")
    for name in MUTATION_NAMES:
        files = mutated_fixture(name)
        if files == base:
            print("self-test: mutation %s did not change the fixture" % name)
            problems += 1
            continue
        with tempfile.TemporaryDirectory(prefix="claims-check-") as tmp:
            root = Path(tmp) / "mutated"
            write_fixture(root, files)
            failed = failed_sections(run_checks(root))
        if failed == {name}:
            print("self-test: mutation %s: %s red, other sections green" % (name, name))
        elif name in failed:
            print("self-test: mutation %s: %s red; also red: %s" % (name, name, ", ".join(sorted(failed - {name}))))
            problems += 1
        else:
            print("self-test: mutation %s: NOT DETECTED" % name)
            problems += 1
    if problems:
        print("self-test: FAIL (%d problem(s))" % problems)
        return 1
    print("self-test: 6/6 mutations flipped, clean fixture green")
    return 0

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="The claims gate: every claim the grakstack tree makes must resolve against the tree.")
    parser.add_argument("--check", action="store_true", help="audit the tree")
    parser.add_argument("--self-test", action="store_true", help="prove one mutation per section flips, in a temp fixture")
    parser.add_argument("--root", default=None, help="repo root to audit (default: inferred from this script's location)")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.check:
        root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
        return run_check(root)
    parser.print_help()
    return 2

if __name__ == "__main__":
    sys.exit(main())

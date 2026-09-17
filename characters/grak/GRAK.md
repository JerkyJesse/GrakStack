# GRAK

```
    ___                ___  _             _
   / __\__ ___   _____/ __\| |_ __ _  ___| | __
  / /  / _` \ \ / / _ \__ \| __/ _` |/ __| |/ /
 / /__| (_| |\ V /  __/___) | || (_| | (__|   <
 \____/\__,_| \_/ \___|____/ \__\__,_|\___|_|\_\

> AI talk too much. Grak fix.
```

Grak is not a mascot. Grak is the agent.

### Who is Grak?

Staff Engineer, Level: Cave. 12 years infra at StoneStack & Mammoth Labs. Ex-Lead at Obsidian Systems, FireCorp, and SpearPoint. PhD compilers (Rock University). 10k+ PRs reviewed.
Built the thing your thing runs on. Invented TTHW (Time To Human Work) - time eng stare at AI output before doing work. Avg: 47s wasted.

One day AI wrote 3 paragraphs of empathy for a one-line bug.
Senior eng closed laptop. Went to cave. Became Grak.

### Why Grak Qualified

**Grak seen waste.** 75% of tokens = cost, latency, senior eng leaving tab. Measured in chars, not tokens. Model-agnostic. Same savings everywhere.

**Grak built rails.**
- CAVE protocol (identity, trust, simplicity)
- Zero-Test-Drift
- Test-Scaffold Gate (soft/hard)
- Voice-verify internet hedge guard
- Persist regardless of voice

**Grak locked to full.** No lite/ultra toggles. No half-terse. `stop caveman` disables per session. `/caveman` resumes.

### What Grak Knows (50+ Skills)

Grak not know one thing. Grak know many thing.

#### Think Before Code
- `/office-hours` - Premise challenge + 6 forcing questions + design doc
- `/spec` - Vague intent -> precise executable spec (5 phases)
- `/investigate` - Reproduce -> isolate -> diagnose -> fix
- `/plan-tune` - Tune question sensitivity

#### Review (Judgment Layer)
- `/plan-eng-review` - Architecture + tests + coverage lock
- `/plan-design-review` - UI/UX audit with mockups
- `/plan-devex-review` - DX critique with personas + benchmarks
- `/plan-ceo-review` - CEO-mode plan review
- `/autoplan` - Run all reviews in sequence
- `/cso` - Security audit: OWASP Top 10 + STRIDE + supply chain

#### Build & Ship
- `/review` - Diff review. Short. Direct.
- `/ship` - Test, review, version, push, PR
- `/land-and-deploy` - Merge, deploy, verify prod
- `/canary` - Post-deploy monitoring loop
- `/checkpoint` - Save/resume work state
- `/context-save` `/context-restore` - Resume across sessions

#### Quality & Ops
- `/qa` `/browse` `/ios-qa` - QA site + fix loop, headless browser, real iPhone
- `/benchmark` `/health` - Core Web Vitals + code quality dashboard
- `/careful` `/freeze` `/guard` `/unfreeze` - Destructive guard + dir lock

#### Design & Docs
- `/design-consultation` `/design-review` `/design-shotgun` `/design-html`
- `/make-pdf` `/diagram` `/document-generate` `/document-release`
- `/scrape` `/skillify` `/benchmark-models`

...and more. Full list: `cavestack-skills list` or `/help`

### How Grak Works

Multi-host. One brain, many caves.
- Claude Code (primary, with hooks)
- Cursor (`~/.cursor/skills/cavestack-*`)
- Kiro, Codex, Factory, OpenCode, Slate, OpenClaw, Hermes, GBrain
- Each host = one file in `hosts/*.ts`

Voice on all skill templates. Not just chat, but instructions compressed. Zero telemetry. No remote data ever. Local DX metrics: `cavestack-dx show`.

Reversible: `cavestack-uninstall`. Your files untouched.

### Controlling Grak

```
# During session:
stop caveman          # back to verbose (why though)
normal mode           # same
/caveman              # re-enable (locked to full)

# Permanent:
cavestack-settings-hook remove-caveman
cavestack-settings-hook install-caveman
```

### Grak Philosophy

```
Other AI: "I'd be happy to help you with that! Let me take a look..."
Grak: [reads code]

Other AI: "The issue appears to be related to the auth middleware where token expiry..."
Grak: "Bug in auth middleware. `<` not `<=`. Fix:"

47 lines explaining what it's about to do
vs
5 lines doing it
```

Grak know: value = work done. Talk less. Work more.

---
Built by JerkyJesse. Grak smash verbose. MIT.

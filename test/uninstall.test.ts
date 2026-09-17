import { describe, test, expect, beforeEach, afterEach } from 'bun:test';
import { spawnSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const ROOT = path.resolve(import.meta.dir, '..');
const UNINSTALL = path.join(ROOT, 'bin', 'cavestack-uninstall');

describe('cavestack-uninstall', () => {
  test('syntax check passes', () => {
    const result = spawnSync('bash', ['-n', UNINSTALL], { stdio: 'pipe' });
    expect(result.status).toBe(0);
  });

  test('--help prints usage and exits 0', () => {
    const result = spawnSync('bash', [UNINSTALL, '--help'], { stdio: 'pipe' });
    expect(result.status).toBe(0);
    const output = result.stdout.toString();
    expect(output).toContain('cavestack-uninstall');
    expect(output).toContain('--force');
    expect(output).toContain('--keep-state');
  });

  test('unknown flag exits with error', () => {
    const result = spawnSync('bash', [UNINSTALL, '--bogus'], {
      stdio: 'pipe',
      env: { ...process.env, HOME: '/nonexistent' },
    });
    expect(result.status).toBe(1);
    expect(result.stderr.toString()).toContain('Unknown option');
  });

  describe('integration tests with mock layout', () => {
    let tmpDir: string;
    let mockHome: string;
    let mockGitRoot: string;

    beforeEach(() => {
      tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cavestack-uninstall-test-'));
      mockHome = path.join(tmpDir, 'home');
      mockGitRoot = path.join(tmpDir, 'repo');

      // Create mock cavestack install layout
      fs.mkdirSync(path.join(mockHome, '.claude', 'skills', 'cavestack'), { recursive: true });
      fs.writeFileSync(path.join(mockHome, '.claude', 'skills', 'cavestack', 'SKILL.md'), 'test');

      // Create per-skill symlinks (both old unprefixed and new prefixed)
      fs.symlinkSync('cavestack/review', path.join(mockHome, '.claude', 'skills', 'review'));
      fs.symlinkSync('cavestack/ship', path.join(mockHome, '.claude', 'skills', 'cavestack-ship'));

      // Create a non-cavestack symlink (should NOT be removed)
      fs.mkdirSync(path.join(mockHome, '.claude', 'skills', 'other-tool'), { recursive: true });

      // Create state directory
      fs.mkdirSync(path.join(mockHome, '.cavestack', 'projects'), { recursive: true });
      fs.writeFileSync(path.join(mockHome, '.cavestack', 'config.json'), '{}');

      // Create mock git repo
      fs.mkdirSync(mockGitRoot, { recursive: true });
      spawnSync('git', ['init', '-b', 'main'], { cwd: mockGitRoot, stdio: 'pipe' });
    });

    afterEach(() => {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('--force removes global Claude skills and state', () => {
      const result = spawnSync('bash', [UNINSTALL, '--force'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: mockHome,
          CAVESTACK_DIR: path.join(mockHome, '.claude', 'skills', 'cavestack'),
          CAVESTACK_STATE_DIR: path.join(mockHome, '.cavestack'),
        },
        cwd: mockGitRoot,
      });

      expect(result.status).toBe(0);
      const output = result.stdout.toString();
      expect(output).toContain('cavestack uninstalled');

      // Global skill dir should be removed
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'cavestack'))).toBe(false);

      // Per-skill symlinks pointing into cavestack/ should be removed
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'review'))).toBe(false);
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'cavestack-ship'))).toBe(false);

      // Non-cavestack tool should still exist
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'other-tool'))).toBe(true);

      // State should be removed
      expect(fs.existsSync(path.join(mockHome, '.cavestack'))).toBe(false);
    });

    test('--keep-state preserves state directory', () => {
      const result = spawnSync('bash', [UNINSTALL, '--force', '--keep-state'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: mockHome,
          CAVESTACK_DIR: path.join(mockHome, '.claude', 'skills', 'cavestack'),
          CAVESTACK_STATE_DIR: path.join(mockHome, '.cavestack'),
        },
        cwd: mockGitRoot,
      });

      expect(result.status).toBe(0);

      // Skills should be removed
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'cavestack'))).toBe(false);

      // State should still exist
      expect(fs.existsSync(path.join(mockHome, '.cavestack'))).toBe(true);
      expect(fs.existsSync(path.join(mockHome, '.cavestack', 'config.json'))).toBe(true);
    });

    test('clean system outputs nothing to remove', () => {
      const cleanHome = path.join(tmpDir, 'clean-home');
      fs.mkdirSync(cleanHome, { recursive: true });

      const result = spawnSync('bash', [UNINSTALL, '--force'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: cleanHome,
          CAVESTACK_DIR: path.join(cleanHome, 'nonexistent'),
          CAVESTACK_STATE_DIR: path.join(cleanHome, '.cavestack'),
        },
        cwd: mockGitRoot,
      });

      expect(result.status).toBe(0);
      expect(result.stdout.toString()).toContain('Nothing to remove');
    });

    test('upgrade path: prefixed install + uninstall cleans both old and new symlinks', () => {
      // Simulate the state after setup --no-prefix followed by setup (with prefix):
      // Both old unprefixed and new prefixed symlinks exist
      // (mockHome already has both 'review' and 'cavestack-ship' symlinks)

      const result = spawnSync('bash', [UNINSTALL, '--force'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: mockHome,
          CAVESTACK_DIR: path.join(mockHome, '.claude', 'skills', 'cavestack'),
          CAVESTACK_STATE_DIR: path.join(mockHome, '.cavestack'),
        },
        cwd: mockGitRoot,
      });

      expect(result.status).toBe(0);

      // Both old (review) and new (cavestack-ship) symlinks should be gone
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'review'))).toBe(false);
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'cavestack-ship'))).toBe(false);

      // Non-cavestack should survive
      expect(fs.existsSync(path.join(mockHome, '.claude', 'skills', 'other-tool'))).toBe(true);
    });

    test('--force removes Cursor cavestack skills and leaves other Cursor skills', () => {
      // Cursor installs are rendered real dirs, so removal is gated on the
      // generated banner in SKILL.md (S5) — the managed fixtures carry it.
      const banner = '<!-- AUTO-GENERATED from SKILL.md.tmpl - DO NOT EDIT DIRECTLY -->\n# x\n';
      fs.mkdirSync(path.join(mockHome, '.cursor', 'skills', 'cavestack'), { recursive: true });
      fs.writeFileSync(path.join(mockHome, '.cursor', 'skills', 'cavestack', 'SKILL.md'), banner);
      fs.mkdirSync(path.join(mockHome, '.cursor', 'skills', 'cavestack-review'), { recursive: true });
      fs.writeFileSync(path.join(mockHome, '.cursor', 'skills', 'cavestack-review', 'SKILL.md'), banner);
      fs.mkdirSync(path.join(mockHome, '.cursor', 'skills', 'frontend-design'), { recursive: true });
      fs.writeFileSync(path.join(mockHome, '.cursor', 'skills', 'frontend-design', 'SKILL.md'), 'keep');

      fs.mkdirSync(path.join(mockGitRoot, '.cursor', 'skills', 'cavestack-ship'), { recursive: true });
      fs.writeFileSync(path.join(mockGitRoot, '.cursor', 'skills', 'cavestack-ship', 'SKILL.md'), banner);
      fs.mkdirSync(path.join(mockGitRoot, '.cursor', 'rules'), { recursive: true });
      fs.writeFileSync(path.join(mockGitRoot, '.cursor', 'rules', 'keep.md'), 'keep');

      const result = spawnSync('bash', [UNINSTALL, '--force'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: mockHome,
          CAVESTACK_DIR: path.join(mockHome, '.claude', 'skills', 'cavestack'),
          CAVESTACK_STATE_DIR: path.join(mockHome, '.cavestack'),
        },
        cwd: mockGitRoot,
      });

      expect(result.status).toBe(0);

      expect(fs.existsSync(path.join(mockHome, '.cursor', 'skills', 'cavestack'))).toBe(false);
      expect(fs.existsSync(path.join(mockHome, '.cursor', 'skills', 'cavestack-review'))).toBe(false);
      expect(fs.existsSync(path.join(mockHome, '.cursor', 'skills', 'frontend-design'))).toBe(true);
      expect(fs.existsSync(path.join(mockGitRoot, '.cursor', 'skills', 'cavestack-ship'))).toBe(false);
      expect(fs.existsSync(path.join(mockGitRoot, '.cursor', 'rules', 'keep.md'))).toBe(true);
    });

    test("a user's own cavestack-prefixed Cursor dir (no banner) survives and is listed", () => {
      // S5: the bare cavestack* glob must not sweep a dir that merely starts
      // with "cavestack" — provenance comes from the generated banner, and a
      // hand-written SKILL.md never carries it.
      const foreign = path.join(mockHome, '.cursor', 'skills', 'cavestack-fork-notes');
      fs.mkdirSync(foreign, { recursive: true });
      fs.writeFileSync(path.join(foreign, 'SKILL.md'), '# my own notes\n');

      const foreignLocal = path.join(mockGitRoot, '.cursor', 'skills', 'cavestack-my-rules');
      fs.mkdirSync(foreignLocal, { recursive: true });
      fs.writeFileSync(path.join(foreignLocal, 'SKILL.md'), '# hand-written\n');

      const result = spawnSync('bash', [UNINSTALL, '--force'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: mockHome,
          CAVESTACK_DIR: path.join(mockHome, '.claude', 'skills', 'cavestack'),
          CAVESTACK_STATE_DIR: path.join(mockHome, '.cavestack'),
        },
        cwd: mockGitRoot,
      });

      expect(result.status).toBe(0);
      expect(fs.existsSync(foreign)).toBe(true);
      expect(fs.existsSync(foreignLocal)).toBe(true);
      const stderr = result.stderr.toString();
      expect(stderr).toContain('left in place');
      expect(stderr).toContain('cavestack-fork-notes');
      expect(stderr).toContain('cavestack-my-rules');
    });
  });
});

// ----------------------------------------------------------------------
// Grak OpenCode agent mode (uninstall + setup wiring). Kept in its own
// describe: the mock layout above builds symlinks (needs Developer Mode on
// Windows), while these cases are pure file copies either shape installs.
// ----------------------------------------------------------------------

describe('cavestack-uninstall removes the Grak OpenCode agent mode', () => {
  let tmpDir: string;
  let mockHome: string;
  let agentDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cavestack-uninstall-grak-'));
    mockHome = path.join(tmpDir, 'home');
    agentDir = path.join(mockHome, '.config', 'opencode', 'agent');
    fs.mkdirSync(agentDir, { recursive: true });
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  function runUninstall(): { status: number | null; stdout: string; stderr: string } {
    const r = spawnSync('bash', [UNINSTALL, '--force'], {
      stdio: 'pipe',
      encoding: 'utf-8',
      env: {
        ...process.env,
        HOME: mockHome,
        CAVESTACK_DIR: path.join(mockHome, '.claude', 'skills', 'cavestack'),
        CAVESTACK_STATE_DIR: path.join(mockHome, '.cavestack'),
      },
      cwd: tmpDir,
    });
    return { status: r.status, stdout: r.stdout, stderr: r.stderr };
  }

  test('managed copy (cavestack-managed marker) is removed, other agent files survive', () => {
    // Windows install shape: a real copy carrying the marker install_opencode_agent
    // writes. Anything else in the agent dir is the user's and must survive.
    fs.writeFileSync(
      path.join(agentDir, 'grak.md'),
      '---\nmode: primary\n---\n<!-- cavestack-managed: grak agent mode -->\n',
    );
    fs.writeFileSync(path.join(agentDir, 'my-own-agent.md'), '# mine\n');

    const r = runUninstall();
    expect(r.status).toBe(0);
    expect(fs.existsSync(path.join(agentDir, 'grak.md'))).toBe(false);
    expect(fs.existsSync(path.join(agentDir, 'my-own-agent.md'))).toBe(true);
    expect(r.stdout).toContain('opencode/grak agent');
  });

  test("a user's own grak.md (no marker) survives and is listed", () => {
    fs.writeFileSync(
      path.join(agentDir, 'grak.md'),
      '---\nmode: primary\n---\n# my own agent, same name\n',
    );

    const r = runUninstall();
    expect(r.status).toBe(0);
    expect(fs.existsSync(path.join(agentDir, 'grak.md'))).toBe(true);
    expect(r.stderr).toContain('left in place');
    expect(r.stderr).toContain('grak.md');
  });

  test.skipIf(process.platform === 'win32')('symlinked grak.md (Unix install shape) is removed', () => {
    const src = path.join(tmpDir, 'grak-agent.md');
    fs.writeFileSync(src, '---\nmode: primary\n---\n');
    fs.symlinkSync(src, path.join(agentDir, 'grak.md'));

    const r = runUninstall();
    expect(r.status).toBe(0);
    expect(fs.existsSync(path.join(agentDir, 'grak.md'))).toBe(false);
  });
});

// ----------------------------------------------------------------------
// Hook-cleanup ordering (phantom-hooks fix). Pre-v1.67.2, the settings
// cleanup ran AFTER `rm -rf $CLAUDE_SKILLS/cavestack` — and SETTINGS_HOOK
// resolves via $(dirname "$0") INSIDE that root, so a real global uninstall
// (running the installed copy) silently orphaned every hook. Prior tests
// masked this by running the uninstaller from the repo checkout. This test
// runs the INSTALLED copy.
// ----------------------------------------------------------------------

describe('hook cleanup runs before the install root is deleted', () => {
  test('uninstall executed FROM the install root still removes hook entries', () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'cavestack-uninstall-order-'));
    try {
      const mockHome = path.join(tmp, 'home');
      const installRoot = path.join(mockHome, '.claude', 'skills', 'cavestack');
      const installBin = path.join(installRoot, 'bin');
      fs.mkdirSync(installBin, { recursive: true });
      // The installed copies — the uninstaller under test IS the one inside
      // the root it deletes.
      for (const b of ['cavestack-uninstall', 'cavestack-settings-hook', 'cavestack-session-update', 'cavestack-config']) {
        const src = path.join(ROOT, 'bin', b);
        const dst = path.join(installBin, b);
        fs.copyFileSync(src, dst);
        fs.chmodSync(dst, 0o755);
      }
      const settingsFile = path.join(mockHome, '.claude', 'settings.json');
      fs.writeFileSync(settingsFile, JSON.stringify({
        hooks: {
          PostToolUse: [{
            matcher: '(AskUserQuestion|mcp__.*__AskUserQuestion)',
            _cavestack_source: 'auq-error-fallback',
            hooks: [{ type: 'command', command: '/dead/wt/hosts/claude/hooks/auq-error-fallback-hook', timeout: 5 }],
          }],
          Stop: [{
            hooks: [{ type: 'command', command: `${installRoot}/hosts/claude/hooks/timeline-stop-hook`, timeout: 5 }],
          }],
          PreCompact: [{ hooks: [{ type: 'command', command: '/Users/me/my-own-hook' }] }],
        },
      }, null, 2));
      fs.mkdirSync(path.join(mockHome, '.cavestack'), { recursive: true });

      const result = spawnSync('bash', [path.join(installBin, 'cavestack-uninstall'), '--force', '--keep-state'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: mockHome,
          CAVESTACK_SETTINGS_FILE: settingsFile,
          CAVESTACK_STATE_ROOT: path.join(mockHome, '.cavestack'),
        },
        cwd: tmp,
      });
      expect(result.status).toBe(0);

      // Install root gone…
      expect(fs.existsSync(installRoot)).toBe(false);
      // …and the hook entries were still cleaned (cleanup ran BEFORE deletion).
      const s = JSON.parse(fs.readFileSync(settingsFile, 'utf-8'));
      expect(s.hooks?.PostToolUse).toBeUndefined();
      expect(s.hooks?.Stop).toBeUndefined();
      // The user's own hook survives the sweep.
      expect(s.hooks?.PreCompact?.[0]?.hooks?.[0]?.command).toBe('/Users/me/my-own-hook');
    } finally {
      fs.rmSync(tmp, { recursive: true, force: true });
    }
    // 30s: the copied uninstaller spawns several bun -e children; on a loaded
    // box their cold starts blow bun's default 5s per-test timeout.
  }, 30000);
});

describe('hook cleanup under lock contention is loud, never silent (review-army)', () => {
  test('a held foreign lock during uninstall surfaces the give-up warning on stderr', () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'cavestack-uninstall-lock-'));
    try {
      const mockHome = path.join(tmp, 'home');
      const installRoot = path.join(mockHome, '.claude', 'skills', 'cavestack');
      const installBin = path.join(installRoot, 'bin');
      fs.mkdirSync(installBin, { recursive: true });
      for (const b of ['cavestack-uninstall', 'cavestack-settings-hook', 'cavestack-session-update', 'cavestack-config']) {
        const dst = path.join(installBin, b);
        fs.copyFileSync(path.join(ROOT, 'bin', b), dst);
        fs.chmodSync(dst, 0o755);
      }
      const settingsFile = path.join(mockHome, '.claude', 'settings.json');
      fs.writeFileSync(settingsFile, JSON.stringify({
        hooks: {
          Stop: [{
            _cavestack_source: 'cavestack-timeline-stop',
            hooks: [{ type: 'command', command: `${installRoot}/hosts/claude/hooks/timeline-stop-hook` }],
          }],
        },
      }, null, 2));
      fs.mkdirSync(path.join(mockHome, '.cavestack'), { recursive: true });
      // A fresh foreign lock: pre-fix, every cleanup call silently skipped and
      // uninstall reported clean while orphaning the hooks forever.
      fs.mkdirSync(`${settingsFile}.lock`);
      fs.writeFileSync(path.join(`${settingsFile}.lock`, 'owner'), 'another-live-process');

      const result = spawnSync('bash', [path.join(installBin, 'cavestack-uninstall'), '--force', '--keep-state'], {
        stdio: 'pipe',
        env: {
          ...process.env,
          HOME: mockHome,
          CAVESTACK_SETTINGS_FILE: settingsFile,
          CAVESTACK_STATE_ROOT: path.join(mockHome, '.cavestack'),
          CAVESTACK_SETTINGS_LOCK_TIMEOUT_MS: '300',
        },
        cwd: tmp,
      });
      const stderr = result.stderr.toString();
      const s = JSON.parse(fs.readFileSync(settingsFile, 'utf-8'));
      const cleaned = s.hooks?.Stop === undefined;
      // Either the sweep still happened, or the user SEES why it didn't.
      expect(cleaned || /could not acquire lock/.test(stderr)).toBe(true);
      expect(/could not acquire lock/.test(stderr)).toBe(true);
    } finally {
      fs.rmSync(tmp, { recursive: true, force: true });
    }
    // 30s: several settings-hook calls each wait out the 300ms lock give-up,
    // and their bun -e cold starts stack up under load — the default 5s
    // per-test budget is too tight on a busy box.
  }, 30000);
});

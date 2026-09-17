/**
 * Grak ships as a selectable OpenCode agent mode. setup's OpenCode arm
 * installs characters/grak/grak-agent.md to ~/.config/opencode/agent/grak.md
 * via _link_or_copy (symlink on Unix, copy on Windows), and cavestack-uninstall
 * removes it behind a provenance gate. This file is the static half: setup
 * wiring + the agent file's schema validity. The removal behavior itself is
 * exercised with a mock HOME in uninstall.test.ts.
 */
import { describe, test, expect } from 'bun:test';
import * as fs from 'fs';
import * as path from 'path';

const ROOT = path.resolve(import.meta.dir, '..');
const SETUP = fs.readFileSync(path.join(ROOT, 'setup'), 'utf-8');
const AGENT = fs.readFileSync(path.join(ROOT, 'characters', 'grak', 'grak-agent.md'), 'utf-8');

/** Body of a shell function `name() { ... }` up to the closing line `}`. */
function fnBody(src: string, name: string): string {
  const start = src.indexOf(`${name}() {`);
  if (start === -1) return '';
  const end = src.indexOf('\n}', start);
  return src.slice(start, end === -1 ? undefined : end);
}

/** Content between two marker lines of the setup script. */
function between(src: string, startMarker: string, endMarker: string): string {
  const start = src.indexOf(startMarker);
  const end = src.indexOf(endMarker, start + 1);
  return start === -1 || end === -1 ? '' : src.slice(start, end);
}

describe('setup installs the Grak OpenCode agent mode', () => {
  test('install_opencode_agent links the agent source into ~/.config/opencode/agent', () => {
    const body = fnBody(SETUP, 'install_opencode_agent');
    expect(body).not.toBe('');
    expect(body).toContain('characters/grak/grak-agent.md');
    expect(body).toContain('$HOME/.config/opencode/agent');
    expect(body).toContain('_link_or_copy');
    // Windows-fallback invariant: no raw ln anywhere in the helper.
    expect(body).not.toMatch(/\bln -s/);
  });

  test('the OpenCode install arm calls install_opencode_agent', () => {
    const arm = between(SETUP, '6c. Install for OpenCode', '6d. Install for Cursor');
    expect(arm).not.toBe('');
    expect(arm).toContain('install_opencode_agent "$SOURCE_CAVESTACK_DIR"');
  });
});

describe('grak-agent.md is a valid OpenCode primary agent', () => {
  const fmMatch = AGENT.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const fm = fmMatch ? fmMatch[1] : '';

  test('frontmatter parses and carries description, primary mode, and hex color', () => {
    expect(fmMatch).not.toBeNull();
    expect(fm).toMatch(/^description:/m);
    expect(fm).toMatch(/^mode:\s*primary\s*$/m);
    expect(fm).toMatch(/^color:\s*'#[0-9A-Fa-f]{6}'/m);
  });

  test('frontmatter keys stay inside the agent schema allowlist', () => {
    const allowed = new Set([
      'name', 'model', 'variant', 'description', 'mode', 'hidden', 'color',
      'steps', 'options', 'permission', 'disable', 'temperature', 'top_p',
    ]);
    const keys = fm
      .split(/\r?\n/)
      .filter((line) => line.trim() !== '' && !line.startsWith(' '))
      .map((line) => line.slice(0, line.indexOf(':')).trim())
      .filter((key) => key !== '');
    expect(keys.filter((key) => !allowed.has(key))).toEqual([]);
  });

  test('the resume credentials are baked into the personality', () => {
    for (const fact of [
      'Staff Engineer',
      'StoneStack',
      'Mammoth Labs',
      'Obsidian Systems',
      'Rock University',
      '10k+ PRs',
      'TTHW',
      'CAVE protocol',
      'Zero-Test-Drift',
    ]) {
      expect(AGENT).toContain(fact);
    }
  });

  test('provenance marker matches the uninstall gate', () => {
    expect(AGENT).toContain('cavestack-managed: grak agent mode');
  });

  test('caveman voice contract is present', () => {
    expect(AGENT).toContain('caveman');
    expect(AGENT).toContain('stop caveman');
  });
});

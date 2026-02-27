#!/usr/bin/env node
const fs = require('fs');
const { execSync } = require('child_process');

function redact(text) {
  const patterns = [/apikey[a-z0-9_\-]+/gi, /sk-[a-z0-9]{20,}/gi];
  let out = text;
  for (const p of patterns) out = out.replace(p, '[REDACTED]');
  return out;
}

function run(cmd) {
  return execSync(cmd, { encoding: 'utf8' }).trim();
}

(async () => {
  const date = new Date().toISOString().slice(0, 10);
  const file = `memory/${date}-chat.md`;
  if (!fs.existsSync('memory')) fs.mkdirSync('memory');

  let sessions;
  try {
    sessions = JSON.parse(run('openclaw sessions list --json'));
  } catch (e) {
    process.exit(0);
  }

  let log = `# Chat Log for ${date}\n\n`;

  for (const s of sessions.sessions) {
    let hist;
    try {
      hist = JSON.parse(run(`openclaw sessions history ${s.key} --limit 500 --json`));
    } catch (e) { continue; }
    for (const m of hist.messages) {
      const speaker = m.sender === 'user' ? 'User' : 'Kevin';
      log += `**${speaker}:** ${redact(m.text)}\n\n`;
    }
  }

  fs.writeFileSync(file, log);
  run('git add .');
  run(`git commit -m "Daily chat log – ${date}" || true`);
})();
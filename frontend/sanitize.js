/** Sanitize package.json (remove BOM / null bytes) before start. */
const fs = require('fs');
const path = require('path');
const pkgPath = path.join(process.cwd(), 'package.json');
try {
  let raw = fs.readFileSync(pkgPath);
  if (raw[0] === 0xEF && raw[1] === 0xBB && raw[2] === 0xBF) {
    raw = raw.slice(3);
  } else if ((raw[0] === 0xFF && raw[1] === 0xFE) || (raw[0] === 0xFE && raw[1] === 0xFF)) {
    const utf16 = raw.toString('utf16le');
    raw = Buffer.from(utf16, 'utf8');
  }
  if (raw.includes(0)) {
    raw = Buffer.from([...raw].filter(b => b !== 0));
  }
  const txt = raw.toString('utf8');
  const parsed = JSON.parse(txt);
  fs.writeFileSync(pkgPath, JSON.stringify(parsed, null, 2));
  console.log('package.json sanitized');
} catch (e) {
  console.warn('package.json sanitation skipped:', e.message);
}

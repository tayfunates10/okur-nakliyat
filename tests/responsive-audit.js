/*
 * Okur Nakliyat — responsive / UI denetim koşucusu
 *
 * Kurulum (yalnızca ilk kullanımda):
 *   npm install                          # playwright devDependency olarak kurulur
 *   npx playwright install chromium      # tarayıcı ikilisini indirir
 *
 * Kullanım:
 *   npm run serve                        # ayrı bir terminalde, proje kökünde
 *   npm run test:responsive              # veya: npm run test:responsive:shot
 *
 * Ortam değişkenleri:
 *   BASE        test edilecek adres (varsayılan http://localhost:8099/index.html)
 *   SHOT=1      her viewport için tam sayfa ekran görüntüsü al
 *   OUT         ekran görüntüsü klasörü
 *   CHROME_PATH sistemde kurulu Chromium yolu
 *
 * Kontrol ettikleri: yatay taşma, taşan öğeler, metin kesilmesi,
 * 44px altı dokunma hedefleri, görsel oran bozulması, header/içerik
 * çakışması, konsol hataları, kırık asset, landscape görünüm.
 */
const { chromium } = require('playwright');
const fs = require('fs');

// Sistemde kurulu bir Chromium kullanmak için CHROME_PATH tanımlayın.
const CHROME = process.env.CHROME_PATH || undefined;
const BASE = process.env.BASE || 'http://localhost:8099/index.html';
const OUT = process.env.OUT || './audit-shots';
const SHOT = process.env.SHOT === '1';

const VIEWPORTS = [
  [320, 568], [360, 640], [375, 667], [390, 844], [412, 915], [430, 932],
  [540, 720], [768, 1024], [820, 1180], [1024, 768], [1280, 720],
  [1366, 768], [1440, 900], [1536, 864], [1920, 1080], [2560, 1440],
];
// ara genişlik taraması
const SWEEP = [];
for (let w = 320; w <= 2560; w += 80) SWEEP.push(w);

function analyse() {
  return page => page.evaluate(() => {
    const docW = document.documentElement.clientWidth;
    const out = {
      scrollW: document.documentElement.scrollWidth,
      bodyScrollW: document.body.scrollWidth,
      clientW: docW,
      overflowing: [],
      clipped: [],
      smallTargets: [],
      distorted: [],
      overlaps: [],
    };

    const label = el =>
      `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${
        typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).join('.') : ''
      }`.slice(0, 90);

    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) continue;

      // yatay taşma
      if (r.right > docW + 1 || r.left < -1) {
        out.overflowing.push({ el: label(el), left: Math.round(r.left), right: Math.round(r.right), pos: cs.position });
      }

      // metin kesilmesi (gizli taşma + gerçek içerik taşması)
      const hidesX = cs.overflowX === 'hidden' || cs.overflowX === 'clip';
      const hidesY = cs.overflowY === 'hidden' || cs.overflowY === 'clip';
      if ((hidesX && el.scrollWidth > el.clientWidth + 1) || (hidesY && el.scrollHeight > el.clientHeight + 1)) {
        if (el.textContent && el.textContent.trim().length > 0) {
          out.clipped.push({
            el: label(el),
            sw: el.scrollWidth, cw: el.clientWidth,
            sh: el.scrollHeight, ch: el.clientHeight,
          });
        }
      }

      // dokunma hedefi
      if (el.matches('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])')) {
        if (r.width > 0 && (r.width < 44 || r.height < 44)) {
          out.smallTargets.push({ el: label(el), w: Math.round(r.width), h: Math.round(r.height) });
        }
      }

      // görsel oranı bozulmuş mu
      if (el.tagName === 'IMG' && el.naturalWidth > 0) {
        const fit = cs.objectFit;
        if (fit === 'fill' || fit === 'none') {
          const natR = el.naturalWidth / el.naturalHeight;
          const boxR = r.width / r.height;
          if (Math.abs(natR - boxR) / natR > 0.02) {
            out.distorted.push({ el: label(el), natR: +natR.toFixed(3), boxR: +boxR.toFixed(3), fit });
          }
        }
      }
    }

    // header ile ana içerik çakışması
    const header = document.querySelector('.site-header');
    const hero = document.querySelector('.hero-content');
    if (header && hero) {
      const hr = header.getBoundingClientRect();
      const cr = hero.getBoundingClientRect();
      if (cr.top < hr.bottom - 1) {
        out.overlaps.push({ a: 'site-header', b: 'hero-content', headerBottom: Math.round(hr.bottom), contentTop: Math.round(cr.top) });
      }
    }
    return out;
  });
}

(async () => {
  const browser = await chromium.launch(CHROME ? { executablePath: CHROME } : {});
  const report = { viewports: [], sweep: [], console: [], network: [], landscape: [] };
  if (SHOT) fs.mkdirSync(OUT, { recursive: true });

  for (const [w, h] of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    page.on('requestfailed', r => {
      const u = r.url();
      const kind = u.includes('fonts.googleapis') || u.includes('fonts.gstatic') ? 'font-external' : 'asset';
      report.network.push({ vp: `${w}x${h}`, url: u.slice(0, 110), kind, err: r.failure()?.errorText });
    });
    page.on('response', r => {
      if (r.status() >= 400) report.network.push({ vp: `${w}x${h}`, url: r.url().slice(0, 110), kind: 'http', status: r.status() });
    });

    await page.goto(BASE, { waitUntil: 'load' });
    await page.waitForTimeout(2200);
    const res = await analyse()(page);
    res.vp = `${w}x${h}`;
    res.hScroll = res.scrollW > res.clientW;
    report.viewports.push(res);
    if (errs.length) report.console.push({ vp: `${w}x${h}`, errs });
    if (SHOT) await page.screenshot({ path: `${OUT}/${w}x${h}.png`, fullPage: true });
    await page.close();
  }

  // ara genişlik taraması (yalnızca yatay taşma)
  const sp = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await sp.goto(BASE, { waitUntil: 'load' });
  for (const w of SWEEP) {
    await sp.setViewportSize({ width: w, height: 800 });
    await sp.waitForTimeout(90);
    const r = await sp.evaluate(() => ({
      sw: document.documentElement.scrollWidth,
      cw: document.documentElement.clientWidth,
    }));
    if (r.sw > r.cw) report.sweep.push({ w, sw: r.sw, cw: r.cw });
  }
  await sp.close();

  // landscape (mobil yatay)
  for (const [w, h] of [[844, 390], [932, 430], [667, 375]]) {
    const p = await browser.newPage({ viewport: { width: w, height: h } });
    await p.goto(BASE, { waitUntil: 'load' });
    await p.waitForTimeout(1200);
    const res = await analyse()(p);
    res.vp = `${w}x${h} (landscape)`;
    res.hScroll = res.scrollW > res.clientW;
    report.landscape.push(res);
    if (SHOT) await p.screenshot({ path: `${OUT}/ls-${w}x${h}.png`, fullPage: false });
    await p.close();
  }

  await browser.close();

  // özet
  const sum = v => ({
    vp: v.vp, hScroll: v.hScroll,
    overflow: v.overflowing.length, clipped: v.clipped.length,
    smallTap: v.smallTargets.length, distorted: v.distorted.length, overlap: v.overlaps.length,
  });
  console.log('=== VIEWPORT OZETI ===');
  console.table([...report.viewports, ...report.landscape].map(sum));

  const firstIssues = [...report.viewports, ...report.landscape].filter(
    v => v.hScroll || v.overflowing.length || v.clipped.length || v.smallTargets.length || v.distorted.length || v.overlaps.length
  );
  console.log('\n=== AYRINTI (sorunlu viewportlar) ===');
  for (const v of firstIssues) {
    console.log(`\n--- ${v.vp} (scrollW=${v.scrollW} clientW=${v.clientW}) ---`);
    if (v.overflowing.length) console.log('  TASAN:', JSON.stringify(v.overflowing.slice(0, 8)));
    if (v.clipped.length) console.log('  KESIK:', JSON.stringify(v.clipped.slice(0, 8)));
    if (v.smallTargets.length) console.log('  KUCUK HEDEF:', JSON.stringify(v.smallTargets.slice(0, 8)));
    if (v.distorted.length) console.log('  ORAN BOZUK:', JSON.stringify(v.distorted));
    if (v.overlaps.length) console.log('  CAKISMA:', JSON.stringify(v.overlaps));
  }

  console.log('\n=== ARA GENISLIK TARAMASI (taşma) ===');
  console.log(report.sweep.length ? JSON.stringify(report.sweep) : 'temiz (320-2560)');

  console.log('\n=== CONSOLE ===');
  console.log(report.console.length ? JSON.stringify(report.console.slice(0, 5), null, 1) : 'hata yok');

  console.log('\n=== AG ===');
  const grouped = {};
  for (const n of report.network) {
    const k = `${n.kind} ${n.status || n.err || ''} ${n.url}`;
    grouped[k] = (grouped[k] || 0) + 1;
  }
  console.log(Object.keys(grouped).length ? JSON.stringify(grouped, null, 1) : 'sorun yok');

  fs.writeFileSync(
    process.env.JSON || './audit.json',
    JSON.stringify(report, null, 1)
  );
})();

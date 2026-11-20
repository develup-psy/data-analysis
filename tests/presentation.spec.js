const { test, expect } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { chromium } = require('playwright-core');

const url = `file://${path.resolve(__dirname, '..', 'index.html')}`;
const chrome = process.env.PLAYWRIGHT_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

async function withPage(fn) {
  const browser = await chromium.launch({ headless: true, executablePath: chrome });
  const context = await browser.newContext({ viewport: { width: 1600, height: 900 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await context.newPage();
  try {
    await page.goto(url);
    await fn(page);
  } finally {
    await browser.close();
  }
}

test('deck follows the supplied teaching order and excludes deleted data', async () => {
  await withPage(async page => {
    const slides = page.locator('#stage > section.slide');
    assert.ok((await slides.count()) >= 35);
    const titles = await slides.evaluateAll(elements => elements.map(element => element.dataset.title));
    const text = await page.locator('#stage').textContent();
    assert.ok(titles.indexOf('프로젝트 결과 시연') < titles.indexOf('데이터 분석의 여섯 단계'));
    assert.ok(titles.indexOf('데이터 분석의 여섯 단계') < titles.indexOf('텍스트 마이닝'));
    assert.ok(titles.indexOf('텍스트 마이닝') < titles.indexOf('프로젝트 실습'));
    assert.equal(text.includes('따릉이'), false);
    assert.ok(text.includes('뷰티 결과물 추가 예정'));
  });
});

test('slide navigation, hash and speaker notes work', async () => {
  await withPage(async page => {
    assert.equal(await page.locator('#counter').innerText(), `1 / ${await page.locator('#stage > section.slide').count()}`);
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.evaluate(() => location.hash), '#slide-2');
    await page.keyboard.press('n');
    assert.ok((await page.locator('#notes').getAttribute('class')).includes('open'));
    assert.ok((await page.locator('#noteText').inputValue()).length > 20);
  });
});

test('lab prompts copy complete plain text', async () => {
  await withPage(async page => {
    await page.goto(`${url}#slide-17`);
    await page.locator('#stage > section.slide.active .copy-prompt').first().click();
    const copied = await page.evaluate(() => navigator.clipboard.readText());
    assert.ok(copied.includes('Spotify.csv'));
    assert.equal(copied.includes('```'), false);
    assert.ok((await page.locator('#copyStatus').innerText()).includes('복사'));
  });
});

test('prompt buttons remain inside the slide and telecom demo opens', async () => {
  await withPage(async page => {
    const overflow = await page.evaluate(() => {
      const slides = [...document.querySelectorAll('#stage > .slide')];
      return slides.flatMap((slide, index) => {
        slide.style.display = 'flex';
        const bounds = slide.getBoundingClientRect();
        const clipped = [...slide.querySelectorAll('.prompt-item button')].filter(button => {
          const rect = button.getBoundingClientRect();
          return rect.left < bounds.left || rect.right > bounds.right;
        }).map(button => `${index + 1}: ${button.textContent}`);
        slide.style.display = '';
        return clipped;
      });
    });
    assert.deepEqual(overflow, []);
    await page.goto(`${url}#slide-5`);
    const demo = page.locator('.slide.active .primary-link');
    const href = await demo.getAttribute('href');
    assert.ok(href.startsWith('./결과물/'));
    assert.ok(path.resolve(__dirname, '..', decodeURI(href)).endsWith('.html'));
    const [report] = await Promise.all([page.waitForEvent('popup'), demo.click()]);
    await report.waitForLoadState('domcontentloaded');
    assert.ok((await report.title()).length > 0);
  });
});

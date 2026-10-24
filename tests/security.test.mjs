import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const elements = new Map();
const context = vm.createContext({
  HTMLElement: class {
    attachShadow() {
      this.shadowRoot = { innerHTML: "", querySelector: () => null, querySelectorAll: () => [] };
    }
  },
  customElements: { get: (name) => elements.get(name), define: (name, cls) => elements.set(name, cls) },
  window: {}, navigator: { userAgent: "test" }, location: { origin: "https://ha.example" },
  URL, console: { info() {} },
});
vm.runInContext(readFileSync(new URL("../touchkio-card.js", import.meta.url), "utf8"), context);
const Card = elements.get("touchkio-card");
const attack = '<img src=x onerror="alert(document.domain)">';

test("entity states, titles, update versions and image attributes are escaped", () => {
  const card = new Card();
  card.hass = { states: {
    "sensor.temp": { state: attack, attributes: {} },
    "update.app": { state: "on", attributes: { installed_version: attack, latest_version: attack + "2" } },
  } };
  card.setConfig({ title: attack, subtitle: attack, update_title: attack, temperature_entity: "sensor.temp",
    update_entity: "update.app", image_url: 'x" onerror="alert(1)' });
  const html = card.shadowRoot.innerHTML;
  assert.ok(!html.includes(attack));
  assert.ok(!html.includes('src="x" onerror='));
  assert.match(html, /&lt;img/);
});

test("package names and versions are escaped when expanded", () => {
  const card = new Card();
  card.hass = { states: { "sensor.packages": { state: "1", attributes: { packages: [{ [attack]: attack }] } } } };
  card.setConfig({ packages_entity: "sensor.packages" });
  card._pkgOpen = true;
  card._render();
  assert.ok(!card.shadowRoot.innerHTML.includes(attack));
  assert.match(card.shadowRoot.innerHTML, /&lt;img src=x onerror=&quot;/);
});

test("selection values and dashboard API titles and paths cannot escape attributes", () => {
  const card = new Card();
  card.hass = { states: { "select.theme": { state: attack, attributes: { options: [attack] } } } };
  card.setConfig({ theme_entity: "select.theme" });
  card._pages = [{ title: attack, url_path: 'dash" onfocus="alert(1)', views: [{ title: attack, path: attack }] }];
  card._render();
  const html = card.shadowRoot.innerHTML;
  assert.ok(!html.includes(attack));
  assert.ok(!html.includes('" onfocus="alert(1)'));
  assert.match(html, /&quot; onfocus=&quot;/);
  assert.match(html, /&lt;img/);
});

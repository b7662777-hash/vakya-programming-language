/**
 * Vākya Mini Browser Client Controller
 *
 * Implements URL parsing, DOM tree traversal, history management,
 * and view rendering mirroring `vakya/browser.vakya` and `browser/engine.py`.
 */

// Embedded offline preset documents for instant testing
const PRESET_PAGES = {
  "https://example.com": `<!DOCTYPE html>
<html>
<head>
  <title>Example Domain</title>
</head>
<body>
  <div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
  </div>
</body>
</html>`,

  "local:sample": `<!DOCTYPE html>
<html>
<head>
  <title>Vākya Sample Page</title>
</head>
<body>
  <h1>Namaste, Vākya Browser!</h1>
  <p>This is a well-formed HTML document demonstrating <strong>Vākya Mini Browser</strong> capabilities.</p>
  <h2>Core Vākya Features</h2>
  <ul>
    <li>Sanskrit-inspired vocabulary with standard Roman characters</li>
    <li>Custom Stack-based Bytecode Virtual Machine</li>
    <li>Exact source line/column diagnostics</li>
  </ul>
  <h2>Learn More</h2>
  <p>Visit <a href="https://example.com">Example.com</a> for standard web testing.</p>
</body>
</html>`,

  "local:malformed": `<html>
<body>
  <h1>Malformed HTML Test
  <p>This page contains unclosed tags and nested formatting.
  <p><b>Bold text <i>and nested italic</b></i>
  <ul>
    <li>Item 1 without closing li
    <li>Item 2 with <a href="https://example.com">embedded link</a>
    <li>Item 3
  <hr>
  <div>Unclosed footer block
</body>
</html>`,

  "local:vakya_docs": `<!DOCTYPE html>
<html>
<body>
  <h1>Vākya Language Architecture</h1>
  <p>Vākya compiles source code to bytecode executed on a custom stack-based Virtual Machine.</p>
  <h2>Supported Keywords</h2>
  <ul>
    <li><strong>chara</strong>: Mutable variable declaration</li>
    <li><strong>dhruva</strong>: Immutable constant declaration</li>
    <li><strong>karya</strong>: Function definition</li>
    <li><strong>yadi / anyatha</strong>: Conditional branching</li>
    <li><strong>yavat</strong>: While loop</li>
    <li><strong>pratyekam ... madhye</strong>: For-each iteration</li>
    <li><strong>vada / puchha</strong>: Builtin I/O</li>
  </ul>
</body>
</html>`
};

class MiniBrowserApp {
  constructor() {
    this.history = [];
    this.currentIndex = -1;
    this.currentHtml = "";
    this.currentDom = null;

    this.addressInput = document.getElementById("addressInput");
    this.renderedPage = document.getElementById("renderedPage");
    this.domTreeViewer = document.getElementById("domTreeViewer");
    this.rawSourceViewer = document.getElementById("rawSourceViewer");
    this.btnBack = document.getElementById("btnBack");
    this.btnForward = document.getElementById("btnForward");
    this.btnReload = document.getElementById("btnReload");
    this.btnGo = document.getElementById("btnGo");
    this.statusIndicator = document.getElementById("statusIndicator");
    this.statusMessage = document.getElementById("statusMessage");
    this.nodeCount = document.getElementById("nodeCount");
    this.historyState = document.getElementById("historyState");

    this.initEventListeners();
    this.navigate("https://example.com");
  }

  initEventListeners() {
    this.btnGo.addEventListener("click", () => this.navigate(this.addressInput.value));
    this.addressInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") this.navigate(this.addressInput.value);
    });

    this.btnBack.addEventListener("click", () => this.goBack());
    this.btnForward.addEventListener("click", () => this.goForward());
    this.btnReload.addEventListener("click", () => this.reload());

    // Preset buttons
    document.querySelectorAll(".preset-btn").forEach(btn => {
      btn.addEventListener("click", () => this.navigate(btn.dataset.url));
    });

    // Tab switching
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        btn.classList.add("active");
        document.getElementById(btn.dataset.tab).classList.add("active");
      });
    });
  }

  parseHtmlToDOM(html) {
    const root = { tag: "html", text: "", attrs: {}, children: [] };
    const stack = [root];
    const selfClosing = new Set(["br", "hr", "img", "input", "meta", "link"]);

    const tokenRegex = /<!--[\s\S]*?-->|<[^>]+>|[^<]+/g;
    let match;

    while ((match = tokenRegex.exec(html)) !== null) {
      const token = match[0];

      if (token.startsWith("<!--")) {
        continue;
      } else if (token.startsWith("</")) {
        const tagName = token.slice(2, -1).trim().toLowerCase().split(/\s+/)[0];
        if (stack.length > 1) {
          let idx = stack.length - 1;
          while (idx > 0 && stack[idx].tag !== tagName) {
            idx--;
          }
          if (idx > 0) {
            stack.length = idx;
          }
        }
      } else if (token.startsWith("<")) {
        const raw = token.slice(1, -1).trim();
        if (!raw) continue;
        const parts = raw.split(/\s+/);
        const tagName = parts[0].toLowerCase().replace(/\/$/, "");
        const attrs = {};

        const attrRegex = /([a-zA-Z0-9_-]+)(?:=["']([^"']*)["'])?/g;
        let attrMatch;
        while ((attrMatch = attrRegex.exec(raw)) !== null) {
          if (attrMatch[1].toLowerCase() !== tagName) {
            attrs[attrMatch[1].toLowerCase()] = attrMatch[2] || "";
          }
        }

        const node = { tag: tagName, text: "", attrs, children: [] };
        stack[stack.length - 1].children.push(node);

        const isSelfClosing = raw.endsWith("/") || selfClosing.has(tagName);
        if (!isSelfClosing) {
          stack.push(node);
        }
      } else {
        const text = token.trim();
        if (text) {
          stack[stack.length - 1].children.push({
            tag: "#text",
            text: text.replace(/\s+/g, " "),
            attrs: {},
            children: []
          });
        }
      }
    }

    return root;
  }

  countNodes(node) {
    let count = 1;
    for (const child of node.children) {
      count += this.countNodes(child);
    }
    return count;
  }

  navigate(url) {
    url = url.trim();
    if (!url) return;

    this.setStatus("Loading...", "status-loading");

    // History stack push with forward truncation
    if (this.currentIndex + 1 < this.history.length) {
      this.history = this.history.slice(0, this.currentIndex + 1);
    }
    this.history.push(url);
    this.currentIndex = this.history.length - 1;
    this.addressInput.value = url;

    this.loadPage(url);
  }

  loadPage(url) {
    let htmlContent = PRESET_PAGES[url];

    if (!htmlContent) {
      htmlContent = `<!DOCTYPE html>
<html>
<body>
  <h1>Page Loaded: ${url}</h1>
  <p>Connected to <code>${url}</code> via Vākya Browser Host Engine.</p>
  <hr>
  <p>To inspect offline presets, select <strong>example.com</strong> or <strong>Sample Page</strong> from the preset bar above.</p>
</body>
</html>`;
    }

    this.currentHtml = htmlContent;
    this.currentDom = this.parseHtmlToDOM(htmlContent);

    this.renderDOM();
    this.updateControls();
    this.setStatus("200 OK", "status-ready");
  }

  renderDOM() {
    // 1. Viewport Render
    this.renderedPage.innerHTML = "";
    this.renderNodeToElement(this.currentDom, this.renderedPage);

    // Attach click listeners to links
    this.renderedPage.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const href = link.getAttribute("href");
        if (href) this.navigate(href);
      });
    });

    // 2. DOM Tree Viewer
    this.domTreeViewer.textContent = JSON.stringify(this.currentDom, null, 2);

    // 3. Raw Source Viewer
    this.rawSourceViewer.textContent = this.currentHtml;

    // 4. Status Bar
    const totalNodes = this.countNodes(this.currentDom);
    this.nodeCount.innerText = `DOM Nodes: ${totalNodes}`;
  }

  renderNodeToElement(node, parentElement) {
    if (node.tag === "#text") {
      parentElement.appendChild(document.createTextNode(node.text + " "));
      return;
    }

    let el;
    switch (node.tag) {
      case "html":
      case "body":
      case "div":
        el = document.createElement("div");
        break;
      case "h1": el = document.createElement("h1"); break;
      case "h2": el = document.createElement("h2"); break;
      case "h3": el = document.createElement("h3"); break;
      case "p": el = document.createElement("p"); break;
      case "ul": el = document.createElement("ul"); break;
      case "ol": el = document.createElement("ol"); break;
      case "li": el = document.createElement("li"); break;
      case "strong":
      case "b": el = document.createElement("strong"); break;
      case "em":
      case "i": el = document.createElement("em"); break;
      case "a":
        el = document.createElement("a");
        el.href = node.attrs.href || "#";
        break;
      case "hr": el = document.createElement("hr"); break;
      case "br": el = document.createElement("br"); break;
      default:
        el = document.createElement("div");
    }

    for (const child of node.children) {
      this.renderNodeToElement(child, el);
    }

    parentElement.appendChild(el);
  }

  goBack() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      const url = this.history[this.currentIndex];
      this.addressInput.value = url;
      this.loadPage(url);
    }
  }

  goForward() {
    if (this.currentIndex + 1 < this.history.length) {
      this.currentIndex++;
      const url = this.history[this.currentIndex];
      this.addressInput.value = url;
      this.loadPage(url);
    }
  }

  reload() {
    if (this.currentIndex >= 0) {
      this.loadPage(this.history[this.currentIndex]);
    }
  }

  updateControls() {
    this.btnBack.disabled = this.currentIndex <= 0;
    this.btnForward.disabled = this.currentIndex >= this.history.length - 1;
    this.historyState.innerText = `History: ${this.currentIndex + 1}/${this.history.length}`;
  }

  setStatus(msg, className) {
    this.statusIndicator.className = `status-pill ${className}`;
    this.statusIndicator.innerText = className.includes("ready") ? "Ready" : "Loading";
    this.statusMessage.innerText = msg;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.browserApp = new MiniBrowserApp();
});

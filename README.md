<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Caught In 4K — System Documentation</title>
  <style>
    :root {
      --bg-teal: #008080;
      --win-gray: #c0c0c0;
      --win-light: #ffffff;
      --win-dark: #808080;
      --win-black: #000000;
      --title-navy: linear-gradient(90deg, #000080 0%, #1084d0 100%);
      --term-bg: #0a0e14;
      --accent-green: #00ff66;
      --accent-cyan: #00e5ff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      border-radius: 0px !important;
    }

    body {
      background-color: var(--bg-teal);
      background-image: radial-gradient(#006666 18%, transparent 19%);
      background-size: 4px 4px;
      font-family: "MS Sans Serif", Tahoma, "Segoe UI", sans-serif;
      font-size: 12px;
      color: var(--win-black);
      padding: 24px 12px;
      display: flex;
      justify-content: center;
      line-height: 1.4;
    }

    .window {
      width: 100%;
      maxWidth: 960px;
      background: var(--win-gray);
      border-top: 2px solid var(--win-light);
      border-left: 2px solid var(--win-light);
      border-right: 2px solid var(--win-black);
      border-bottom: 2px solid var(--win-black);
      box-shadow: 3px 3px 0px rgba(0, 0, 0, 0.65);
    }

    .titlebar {
      height: 24px;
      background: var(--title-navy);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 2px 4px;
      user-select: none;
    }

    .titlebar-text {
      color: var(--win-light);
      font-weight: bold;
      font-size: 11px;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .titlebar-controls {
      display: flex;
      gap: 2px;
    }

    .win-btn {
      width: 16px;
      height: 14px;
      background: var(--win-gray);
      border-top: 1px solid var(--win-light);
      border-left: 1px solid var(--win-light);
      border-right: 1px solid var(--win-black);
      border-bottom: 1px solid var(--win-black);
      font-size: 9px;
      font-weight: bold;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }

    .menubar {
      display: flex;
      gap: 16px;
      padding: 3px 8px;
      border-bottom: 1px solid var(--win-dark);
      background: var(--win-gray);
      font-size: 11px;
    }

    .menubar span u {
      text-decoration: underline;
    }

    .container {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .sunken-panel {
      background: var(--win-light);
      border-top: 2px solid var(--win-dark);
      border-left: 2px solid var(--win-dark);
      border-right: 2px solid var(--win-light);
      border-bottom: 2px solid var(--win-light);
      padding: 14px;
    }

    .banner {
      background: #e8e8e8;
      border-top: 2px solid var(--win-dark);
      border-left: 2px solid var(--win-dark);
      border-right: 2px solid var(--win-light);
      border-bottom: 2px solid var(--win-light);
      padding: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .banner h1 {
      font-size: 18px;
      color: #000080;
      margin-bottom: 4px;
    }

    .banner-badge {
      background: #000080;
      color: #ffffff;
      padding: 4px 8px;
      font-family: "Courier New", monospace;
      font-size: 10px;
      font-weight: bold;
      border-top: 1px solid var(--win-light);
      border-left: 1px solid var(--win-light);
      border-right: 1px solid var(--win-black);
      border-bottom: 1px solid var(--win-black);
    }

    .groupbox {
      border-top: 1px solid var(--win-light);
      border-left: 1px solid var(--win-light);
      border-right: 1px solid var(--win-dark);
      border-bottom: 1px solid var(--win-dark);
      box-shadow: -1px -1px 0px var(--win-dark) inset, 1px 1px 0px var(--win-light) inset;
      padding: 12px 14px;
      margin-top: 6px;
    }

    .groupbox legend {
      font-weight: bold;
      padding: 0 4px;
      color: #000080;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    @media (max-width: 768px) {
      .grid-2 {
        grid-template-columns: 1fr;
      }
    }

    .terminal {
      background: var(--term-bg);
      color: var(--accent-green);
      font-family: "Lucida Console", "Courier New", monospace;
      font-size: 11px;
      line-height: 1.5;
      padding: 12px;
      border-top: 2px solid var(--win-dark);
      border-left: 2px solid var(--win-dark);
      border-right: 2px solid var(--win-light);
      border-bottom: 2px solid var(--win-light);
      overflow-x: auto;
      white-space: pre;
    }

    .terminal-cyan {
      color: var(--accent-cyan);
    }

    .terminal-dim {
      color: #718096;
    }

    ul.features-list {
      list-style-type: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    ul.features-list li {
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }

    ul.features-list li::before {
      content: "■";
      color: #000080;
      font-size: 8px;
      margin-top: 2px;
    }

    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      text-align: left;
    }

    table.data-table th {
      background: var(--win-gray);
      border: 1px solid var(--win-dark);
      padding: 4px 6px;
      font-weight: bold;
    }

    table.data-table td {
      border: 1px solid #e0e0e0;
      padding: 4px 6px;
      vertical-align: top;
    }

    .btn-action {
      background: var(--win-gray);
      border-top: 2px solid var(--win-light);
      border-left: 2px solid var(--win-light);
      border-right: 2px solid var(--win-black);
      border-bottom: 2px solid var(--win-black);
      padding: 4px 14px;
      font-size: 11px;
      font-weight: bold;
      font-family: inherit;
      cursor: pointer;
      display: inline-block;
      text-decoration: none;
      color: var(--win-black);
    }

    .btn-action:active {
      border-top: 2px solid var(--win-black);
      border-left: 2px solid var(--win-black);
      border-right: 2px solid var(--win-light);
      border-bottom: 2px solid var(--win-light);
      padding: 5px 13px 3px 15px;
    }

    .statusbar {
      height: 22px;
      background: var(--win-gray);
      border-top: 1px solid var(--win-dark);
      display: flex;
      gap: 4px;
      padding: 2px 4px;
      font-size: 11px;
    }

    .statusbar-panel {
      border-top: 1px solid var(--win-dark);
      border-left: 1px solid var(--win-dark);
      border-right: 1px solid var(--win-light);
      border-bottom: 1px solid var(--win-light);
      padding: 1px 6px;
      display: flex;
      align-items: center;
    }

    .flex-1 { flex: 1; }
    .w-120 { width: 120px; text-align: center; }
  </style>
</head>
<body>

  <div class="window">
    <div class="titlebar">
      <div class="titlebar-text">
        <span>📷</span>
        <span>CAUGHT_IN_4K.DOC — Technical Specification & Run Guide</span>
      </div>
      <div class="titlebar-controls">
        <div class="win-btn">_</div>
        <div class="win-btn">□</div>
        <div class="win-btn">✕</div>
      </div>
    </div>

    <div class="menubar">
      <span><u>F</u>ile</span>
      <span><u>E</u>dit</span>
      <span><u>S</u>earch</span>
      <span><u>H</u>elp</span>
    </div>

    <div class="container">
      <div class="banner">
        <div>
          <h1>CAUGHT IN 4K</h1>
          <p>Autonomous Optical Reaction Parody Generator & Telemetry Microservice</p>
        </div>
        <div class="banner-badge">RTX 4050 ACCELERATED</div>
      </div>

      <fieldset class="groupbox">
        <legend>System Abstract</legend>
        <p>
          A standalone computer vision and generative parody appliance engineered for integration into the 
          <strong>RAGEWARE 98</strong> operating system. The subsystem samples incoming optical buffers, extracts 
          micro-expressions via local vision-language inference, routes features across 1,800+ indexed meme contexts, 
          and burns dynamic, non-cropped captions into output rasters in real-time.
        </p>
      </fieldset>

      <fieldset class="groupbox">
        <legend>Subsystem Architecture Pipeline</legend>
        <div class="terminal">                 +----------------------------------------+
                 |              RAGEWARE 98               |
                 |  (Desktop Icon / External Link Target) |
                 +-------------------+--------------------+
                                     |
                         <span class="terminal-cyan">http://localhost:8000</span>
                                     |
                                     v
  +-----------------------------------------------------------------------+
  |                       <span class="terminal-cyan">CAUGHT IN 4K APPLIANCE</span>                          |
  |                                                                       |
  |  +-----------------------------------------------------------------+  |
  |  |           <span class="terminal-cyan">React 19 Frontend (Vite / Win95 3D UI)</span>                |  |
  |  | - Single-view video capture buffer                              |  |
  |  | - Vertical comparison stack (Live Suspect -> Burned Meme)       |  |
  |  | - Bottom-anchored optical telemetry diagnostics                 |  |
  |  +--------------------------------+--------------------------------+  |
  |                                   | <span class="terminal-cyan">POST /generate-caught-meme</span>        |
  |                                   v                                   |
  |  +-----------------------------------------------------------------+  |
  |  |              <span class="terminal-cyan">FastAPI Backend (CUDA / FP16)</span>                      |  |
  |  |                                                                 |  |
  |  |  1. Vision Parsing:       Moondream2 (Image -> Vibe text)       |  |
  |  |  2. Semantic Search:      Sentence-Transformers (1,800+ Anchors)|  |
  |  |  3. Softmax Variety:      Top-15 Pool with 10-Item History Lock |  |
  |  |  4. Roast Synthesis:      Qwen2.5-0.5B-Instruct                 |  |
  |  |  5. Buffer Rendering:     Pillow (Dynamic Auto-Wrap & Stroke)   |  |
  |  |  6. Static Web Serving:   FastAPI FileResponse (/client/dist)   |  |
  |  +-----------------------------------------------------------------+  |
  +-----------------------------------------------------------------------+</div>
      </fieldset>

      <div class="grid-2">
        <fieldset class="groupbox">
          <legend>Core Engineering Features</legend>
          <ul class="features-list">
            <li><strong>Authentic Windows 95/98 UI:</strong> Beveled panels, sunken viewports, and zero border radius.</li>
            <li><strong>Vertical Display Hierarchy:</strong> Input feed stacked directly above the parody output raster.</li>
            <li><strong>1,800+ Semantic Anchors:</strong> Vectorized matrix across multi-scene emotional templates.</li>
            <li><strong>Anti-Repetition Lockout:</strong> Top-15 sampling pool with a 10-item historical duplicate block.</li>
            <li><strong>Dynamic Text Wrapper:</strong> Auto-scaling Impact text bounded to an 88% width threshold.</li>
            <li><strong>Edge-Ready Execution:</strong> 100% offline inference on host GPU without cloud roundtrips.</li>
          </ul>
        </fieldset>

        <fieldset class="groupbox">
          <legend>Component Specifications</legend>
          <table class="data-table">
            <thead>
              <tr>
                <th>Layer</th>
                <th>Technology</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Vision Core</td>
                <td>Moondream2</td>
                <td>Frame expression extraction</td>
              </tr>
              <tr>
                <td>Embedding</td>
                <td>all-MiniLM-L6-v2</td>
                <td>Semantic vector distance</td>
              </tr>
              <tr>
                <td>LLM Engine</td>
                <td>Qwen2.5-0.5B</td>
                <td>Two-line contextual burns</td>
              </tr>
              <tr>
                <td>HTTP / OS</td>
                <td>FastAPI / Uvicorn</td>
                <td>Static asset & API routing</td>
              </tr>
              <tr>
                <td>Frontend</td>
                <td>React 19 / Vite</td>
                <td>Webcam capture & Win98 UI</td>
              </tr>
            </tbody>
          </table>
        </fieldset>
      </div>

      <fieldset class="groupbox">
        <legend>Source File Index</legend>
        <div class="terminal"><span class="terminal-dim">caught-in-4k/</span>
├── <span class="terminal-cyan">client/</span>                     <span class="terminal-dim"># React frontend workspace</span>
│   ├── <span class="terminal-cyan">dist/</span>                   <span class="terminal-dim"># Static assets served by FastAPI</span>
│   ├── <span class="terminal-cyan">src/App.jsx</span>             <span class="terminal-dim"># Win98 UI components & capture state</span>
│   └── <span class="terminal-cyan">package.json</span>
├── <span class="terminal-cyan">hf_cache/</span>                   <span class="terminal-dim"># Offline model weights store</span>
├── <span class="terminal-cyan">launch.bat</span>                  <span class="terminal-dim"># Runtime initialization batch routine</span>
├── <span class="terminal-cyan">CaughtIn4K.exe</span>              <span class="terminal-dim"># Native compiled launcher binary</span>
├── <span class="terminal-cyan">server.py</span>                   <span class="terminal-dim"># FastAPI inference pipeline & static host</span>
└── <span class="terminal-cyan">.gitignore</span></div>
      </fieldset>

      <fieldset class="groupbox">
        <legend>Deployment Execution Routines</legend>
        <p style="margin-bottom: 8px;"><strong>1. Production Asset Compilation</strong></p>
        <div class="terminal">cd D:\caught-in-4k\client
npm install
npm run build</div>

        <p style="margin: 8px 0;"><strong>2. Build Native Binary Launcher (PowerShell)</strong></p>
        <div class="terminal">cd D:\caught-in-4k
$source = @"
using System;
using System.Diagnostics;
using System.IO;
class Program {
    static void Main() {
        string baseDir = AppDomain.CurrentDomain.BaseDirectory;
        ProcessStartInfo psi = new ProcessStartInfo();
        psi.FileName = Path.Combine(baseDir, "launch.bat");
        psi.WorkingDirectory = baseDir;
        psi.UseShellExecute = true;
        Process.Start(psi);
    }
}
"@
Add-Type -TypeDefinition $source -Language CSharp -OutputAssembly "D:\caught-in-4k\CaughtIn4K.exe" -OutputType ConsoleApplication</div>

        <p style="margin: 8px 0;"><strong>3. RAGEWARE 98 Integration Trigger</strong> (<code>src/components/os/Desktop.jsx</code>)</p>
        <div class="terminal"><span class="terminal-cyan">const</span> CAUGHT_IN_4K_URL = <span class="terminal-green">'http://localhost:8000'</span>;

<span class="terminal-cyan">const</span> handleOpenApp = (appId) => {
  <span class="terminal-cyan">if</span> (appId === <span class="terminal-green">'caught_in_4k'</span>) {
    window.open(CAUGHT_IN_4K_URL, <span class="terminal-green">'_blank'</span>, <span class="terminal-green">'noopener,noreferrer'</span>);
    <span class="terminal-cyan">return</span>;
  }
  openApp(appId);
};</div>
      </fieldset>

      <div style="display: flex; justify-content: flex-end; gap: 8px;">
        <button class="btn-action" onclick="window.print()">Print Document</button>
        <a class="btn-action" href="http://localhost:8000" target="_blank">Launch Subsystem</a>
      </div>
    </div>

    <div class="statusbar">
      <div class="statusbar-panel flex-1">Documentation Status: OK</div>
      <div class="statusbar-panel w-120">VFW32 DRIVER</div>
      <div class="statusbar-panel w-120">PORT: 8000</div>
    </div>
  </div>

</body>
</html>

# Keelwater solution prototype

A clickable prototype of the claim lifecycle: a claimant submits a claim, then it's sorted by hand, in bulk, by rules in a workflow, and finally with an AI agent proposing improvements. Plan and progress: [PLAN.md](PLAN.md).

**To open it:** download [`keelwater-prototype.html`](keelwater-prototype.html) and double-click it. It's one self-contained file: no server or internet needed.

Deep links: `#consumer`, `#handler/inbox`, `#handler/bulk`, `#handler/workflow`, `#handler/agent`.

All claims, insurers and numbers in the prototype are **[INVENTED]**.

## Working on it

```bash
npm install
npm run dev     # local dev server with hot reload
npm run build   # type-check, build, and write keelwater-prototype.html
```

Built with React, [Radix Themes](https://www.radix-ui.com/themes) (styled with Xelix brand tokens in `src/theme.css`) and [React Flow](https://reactflow.dev) for the workflow canvas, bundled into one file by Vite and `vite-plugin-singlefile`.

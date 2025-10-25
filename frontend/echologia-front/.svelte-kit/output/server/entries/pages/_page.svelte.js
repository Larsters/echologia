import "clsx";
import { y as sanitize_props, z as rest_props, F as attributes, G as ensure_array_like, J as element, K as slot, N as bind_props, O as spread_props, x as attr, P as attr_class, Q as attr_style, T as clsx, V as stringify } from "../../chunks/index.js";
import { l as fallback, k as escape_html } from "../../chunks/context.js";
/**
 * @license lucide-svelte v0.374.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const defaultAttributes = {
  xmlns: "http://www.w3.org/2000/svg",
  width: 24,
  height: 24,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  "stroke-width": 2,
  "stroke-linecap": "round",
  "stroke-linejoin": "round"
};
function Icon($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const $$restProps = rest_props($$sanitized_props, [
    "name",
    "color",
    "size",
    "strokeWidth",
    "absoluteStrokeWidth",
    "iconNode"
  ]);
  $$renderer.component(($$renderer2) => {
    let name = $$props["name"];
    let color = fallback($$props["color"], "currentColor");
    let size = fallback($$props["size"], 24);
    let strokeWidth = fallback($$props["strokeWidth"], 2);
    let absoluteStrokeWidth = fallback($$props["absoluteStrokeWidth"], false);
    let iconNode = $$props["iconNode"];
    $$renderer2.push(`<svg${attributes(
      {
        ...defaultAttributes,
        ...$$restProps,
        width: size,
        height: size,
        stroke: color,
        "stroke-width": absoluteStrokeWidth ? Number(strokeWidth) * 24 / Number(size) : strokeWidth,
        class: `lucide-icon lucide lucide-${name} ${$$sanitized_props.class ?? ""}`
      },
      void 0,
      void 0,
      void 0,
      3
    )}><!--[-->`);
    const each_array = ensure_array_like(iconNode);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let [tag, attrs] = each_array[$$index];
      element($$renderer2, tag, () => {
        $$renderer2.push(`${attributes({ ...attrs }, void 0, void 0, void 0, 3)}`);
      });
    }
    $$renderer2.push(`<!--]--><!--[-->`);
    slot($$renderer2, $$props, "default", {});
    $$renderer2.push(`<!--]--></svg>`);
    bind_props($$props, {
      name,
      color,
      size,
      strokeWidth,
      absoluteStrokeWidth,
      iconNode
    });
  });
}
function Pause($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  /**
   * @license lucide-svelte v0.374.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   */
  const iconNode = [
    [
      "rect",
      { "x": "14", "y": "4", "width": "4", "height": "16", "rx": "1" }
    ],
    [
      "rect",
      { "x": "6", "y": "4", "width": "4", "height": "16", "rx": "1" }
    ]
  ];
  Icon($$renderer, spread_props([
    { name: "pause" },
    $$sanitized_props,
    {
      /**
       * @component @name Pause
       * @description Lucide SVG icon component, renders SVG Element with children.
       *
       * @preview ![img](data:image/svg+xml;base64,PHN2ZyAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogIHdpZHRoPSIyNCIKICBoZWlnaHQ9IjI0IgogIHZpZXdCb3g9IjAgMCAyNCAyNCIKICBmaWxsPSJub25lIgogIHN0cm9rZT0iIzAwMCIgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6ICNmZmY7IGJvcmRlci1yYWRpdXM6IDJweCIKICBzdHJva2Utd2lkdGg9IjIiCiAgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIgogIHN0cm9rZS1saW5lam9pbj0icm91bmQiCj4KICA8cmVjdCB4PSIxNCIgeT0iNCIgd2lkdGg9IjQiIGhlaWdodD0iMTYiIHJ4PSIxIiAvPgogIDxyZWN0IHg9IjYiIHk9IjQiIHdpZHRoPSI0IiBoZWlnaHQ9IjE2IiByeD0iMSIgLz4KPC9zdmc+Cg==) - https://lucide.dev/icons/pause
       * @see https://lucide.dev/guide/packages/lucide-svelte - Documentation
       *
       * @param {Object} props - Lucide icons props and any valid SVG attribute
       * @returns {FunctionalComponent} Svelte component
       *
       */
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
function Play($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  /**
   * @license lucide-svelte v0.374.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   */
  const iconNode = [["polygon", { "points": "6 3 20 12 6 21 6 3" }]];
  Icon($$renderer, spread_props([
    { name: "play" },
    $$sanitized_props,
    {
      /**
       * @component @name Play
       * @description Lucide SVG icon component, renders SVG Element with children.
       *
       * @preview ![img](data:image/svg+xml;base64,PHN2ZyAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogIHdpZHRoPSIyNCIKICBoZWlnaHQ9IjI0IgogIHZpZXdCb3g9IjAgMCAyNCAyNCIKICBmaWxsPSJub25lIgogIHN0cm9rZT0iIzAwMCIgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6ICNmZmY7IGJvcmRlci1yYWRpdXM6IDJweCIKICBzdHJva2Utd2lkdGg9IjIiCiAgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIgogIHN0cm9rZS1saW5lam9pbj0icm91bmQiCj4KICA8cG9seWdvbiBwb2ludHM9IjYgMyAyMCAxMiA2IDIxIDYgMyIgLz4KPC9zdmc+Cg==) - https://lucide.dev/icons/play
       * @see https://lucide.dev/guide/packages/lucide-svelte - Documentation
       *
       * @param {Object} props - Lucide icons props and any valid SVG attribute
       * @returns {FunctionalComponent} Svelte component
       *
       */
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
function Search($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  /**
   * @license lucide-svelte v0.374.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   */
  const iconNode = [
    ["circle", { "cx": "11", "cy": "11", "r": "8" }],
    ["path", { "d": "m21 21-4.3-4.3" }]
  ];
  Icon($$renderer, spread_props([
    { name: "search" },
    $$sanitized_props,
    {
      /**
       * @component @name Search
       * @description Lucide SVG icon component, renders SVG Element with children.
       *
       * @preview ![img](data:image/svg+xml;base64,PHN2ZyAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogIHdpZHRoPSIyNCIKICBoZWlnaHQ9IjI0IgogIHZpZXdCb3g9IjAgMCAyNCAyNCIKICBmaWxsPSJub25lIgogIHN0cm9rZT0iIzAwMCIgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6ICNmZmY7IGJvcmRlci1yYWRpdXM6IDJweCIKICBzdHJva2Utd2lkdGg9IjIiCiAgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIgogIHN0cm9rZS1saW5lam9pbj0icm91bmQiCj4KICA8Y2lyY2xlIGN4PSIxMSIgY3k9IjExIiByPSI4IiAvPgogIDxwYXRoIGQ9Im0yMSAyMS00LjMtNC4zIiAvPgo8L3N2Zz4K) - https://lucide.dev/icons/search
       * @see https://lucide.dev/guide/packages/lucide-svelte - Documentation
       *
       * @param {Object} props - Lucide icons props and any valid SVG attribute
       * @returns {FunctionalComponent} Svelte component
       *
       */
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
function AudioManager($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let searchQuery = "";
    let playingId = null;
    let hoveredRow = null;
    let filteredFiles = [];
    function getRowClass(fileId) {
      const baseClass = "grid grid-cols-12 gap-4 px-6 py-5 transition-all duration-300 cursor-pointer";
      const hoverClass = hoveredRow === fileId ? "bg-slate-700/30 scale-[1.01]" : "hover:bg-slate-700/20";
      return `${baseClass} ${hoverClass}`;
    }
    function getIndicatorClass(fileId) {
      const baseClass = "w-2 h-2 rounded-full transition-all duration-300";
      const statusClass = playingId === fileId ? "bg-cyan-400 animate-pulse" : "bg-slate-600";
      return `${baseClass} ${statusClass}`;
    }
    $$renderer2.push(`<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8"><div class="max-w-6xl mx-auto"><div class="mb-12 animate-fadeIn"><div class="flex items-center gap-3 mb-8"><div class="relative"><div class="w-12 h-12 rounded-full bg-cyan-500 flex items-center justify-center animate-pulse"><div class="w-8 h-8 rounded-full border-4 border-white"></div></div> <div class="absolute inset-0 w-12 h-12 rounded-full bg-cyan-400 animate-ping opacity-20"></div></div> <h1 class="text-4xl font-bold text-white">Echologia</h1></div> <div class="relative group">`);
    Search($$renderer2, {
      class: "absolute left-4 top-1/2 transform -translate-y-1/2 text-cyan-400 w-5 h-5 transition-all group-hover:scale-110"
    });
    $$renderer2.push(`<!----> <input type="text" placeholder="Search anything..."${attr("value", searchQuery)} class="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-4 pl-12 pr-4 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:bg-slate-800/80 transition-all duration-300 backdrop-blur-sm"/></div></div> <div class="bg-slate-800/30 backdrop-blur-md rounded-2xl border border-slate-700/50 overflow-hidden shadow-2xl"><div class="grid grid-cols-12 gap-4 px-6 py-4 bg-slate-800/50 border-b border-slate-700/50"><div class="col-span-3 text-slate-400 text-sm font-semibold tracking-wider uppercase">File Name</div> <div class="col-span-2 text-slate-400 text-sm font-semibold tracking-wider uppercase">Date</div> <div class="col-span-6 text-slate-400 text-sm font-semibold tracking-wider uppercase">Labels</div> <div class="col-span-1 text-slate-400 text-sm font-semibold tracking-wider uppercase">Actions</div></div> <div class="divide-y divide-slate-700/30"><!--[-->`);
    const each_array = ensure_array_like(filteredFiles);
    for (let index = 0, $$length = each_array.length; index < $$length; index++) {
      let file = each_array[index];
      $$renderer2.push(`<div${attr_class(clsx(getRowClass(file.id)))}${attr_style(`animation: slideIn 0.5s ease-out ${stringify(index * 0.1)}s both`)}><div class="col-span-3 flex items-center gap-3"><div${attr_class(clsx(getIndicatorClass(file.id)))}></div> <span class="text-slate-200 font-medium">${escape_html(file.filename)}</span></div> <div class="col-span-2 flex items-center text-slate-400">${escape_html(file.date)}</div> <div class="col-span-6 flex flex-wrap gap-2 items-center"><!--[-->`);
      const each_array_1 = ensure_array_like(file.labels);
      for (let idx = 0, $$length2 = each_array_1.length; idx < $$length2; idx++) {
        let label = each_array_1[idx];
        $$renderer2.push(`<span class="px-3 py-1 bg-slate-700/50 text-cyan-300 text-sm rounded-full border border-slate-600/50 transition-all duration-300 hover:bg-slate-600/50 hover:scale-105"${attr_style(`animation: fadeIn 0.5s ease-out ${stringify(index * 0.1 + idx * 0.05)}s both`)}>${escape_html(label)}</span>`);
      }
      $$renderer2.push(`<!--]--></div> <div class="col-span-1 flex items-center gap-2"><button class="p-2 rounded-lg bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30 transition-all duration-300 hover:scale-110">`);
      if (playingId === file.id) {
        $$renderer2.push("<!--[-->");
        Pause($$renderer2, { class: "w-4 h-4" });
      } else {
        $$renderer2.push("<!--[!-->");
        Play($$renderer2, { class: "w-4 h-4" });
      }
      $$renderer2.push(`<!--]--></button></div></div>`);
    }
    $$renderer2.push(`<!--]--></div></div> <div class="mt-8 flex justify-between items-center text-slate-400 text-sm"><div class="flex gap-6"><span class="flex items-center gap-2"><div class="w-2 h-2 rounded-full bg-cyan-400"></div> ${escape_html(filteredFiles.length)} recordings</span> <span class="flex items-center gap-2"><div class="w-2 h-2 rounded-full bg-green-400"></div> All synced</span></div> <div>Last updated: Today</div></div></div></div>`);
  });
}
function _page($$renderer) {
  AudioManager($$renderer);
}
export {
  _page as default
};

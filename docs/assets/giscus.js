// giscus 评论注入 —— 客户端方案（不依赖 mkdocs-material 主题 override 机制，
// 对 instant navigation 兼容：导航时重新挂载）。
// 关闭某页评论：暂不支持 meta 开关；如需关闭在该页 front matter 或此处加 URL 过滤。
(function () {
  "use strict";

  var REPO = "zerogue11/xenium-code-atlas";
  var REPO_ID = "R_kgDOUOnIUA";
  var CATEGORY = "General";
  var CATEGORY_ID = "DIC_kwDOUOnIUM4DGf0F";

  function mountGiscus() {
    if (document.getElementById("giscus-container")) return; // 防重复
    // 只在有正文的页面挂载（404/空页跳过）
    var target = document.querySelector("article") ||
                 document.querySelector(".md-content__inner");
    if (!target) return;

    var h = document.createElement("h2");
    h.id = "__comments";
    h.textContent = "评论";
    var box = document.createElement("div");
    box.id = "giscus-container";

    var s = document.createElement("script");
    s.src = "https://giscus.app/client.js";
    s.setAttribute("data-repo", REPO);
    s.setAttribute("data-repo-id", REPO_ID);
    s.setAttribute("data-category", CATEGORY);
    s.setAttribute("data-category-id", CATEGORY_ID);
    s.setAttribute("data-mapping", "pathname");
    s.setAttribute("data-strict", "1");
    s.setAttribute("data-reactions-enabled", "1");
    s.setAttribute("data-emit-metadata", "0");
    s.setAttribute("data-input-position", "top");
    s.setAttribute("data-theme", "light");
    s.setAttribute("data-lang", "zh-CN");
    s.setAttribute("data-loading", "lazy");
    s.crossOrigin = "anonymous";
    s.async = true;

    box.appendChild(s);
    target.appendChild(h);
    target.appendChild(box);
  }

  // mkdocs-material instant navigation 暴露 document$；普通站点回退 DOMContentLoaded
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(mountGiscus);
  } else {
    document.addEventListener("DOMContentLoaded", mountGiscus);
  }
})();

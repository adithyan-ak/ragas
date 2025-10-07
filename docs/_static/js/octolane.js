document.addEventListener("DOMContentLoaded", () => {
  function loadScript(src, integrity, crossorigin) {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = src;
    if (integrity) {
      script.integrity = integrity;
    }
    if (crossorigin) {
      script.crossOrigin = crossorigin;
    }
    document.head.appendChild(script);
  }

  // Load Octolane script with Subresource Integrity and crossorigin attribute
  loadScript(
    "https://cdn.octolane.com/tag.js?pk=c7c9b2b863bf7eaf4e2a",
    "sha384-0f1q3lQF5Z0eLZ1cZ2p3Yx9fXv6Lh8PzXy7a9b8c6d5e4f3g2h1j0k9l8m7n6o5p",
    "anonymous"
  );
});

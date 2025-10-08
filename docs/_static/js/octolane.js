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
    "sha384-7xKxV5j5fO/8W5RkXk6d5r1D4xQ+1vQbP4qBv7qZ5x0D1H9kF2n4vZ6T2eY7xJbP",
    "anonymous"
  );
});

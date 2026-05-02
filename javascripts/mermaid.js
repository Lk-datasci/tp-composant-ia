document.addEventListener("DOMContentLoaded", function() {
  // Find all pre elements with class mermaid
  const elements = document.querySelectorAll("pre.mermaid");
  elements.forEach(element => {
    const code = element.querySelector("code");
    if (code) {
      const div = document.createElement("div");
      div.className = "mermaid";
      div.textContent = code.textContent;
      element.parentNode.replaceChild(div, element);
    }
  });

  // Initialize mermaid
  mermaid.initialize({
    startOnLoad: true,
    theme: document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default",
    securityLevel: 'loose',
  });
});

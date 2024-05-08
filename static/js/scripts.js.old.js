function openLuna(path) {
    fetch("/open_luna", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: "path=" + encodeURIComponent(path) })
    .then(response => response.json()).then(data => alert(data.message)).catch(error => console.error("Error:", error));
  }
  function openInFinder(path) {
    fetch("/open_in_finder", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: "path=" + encodeURIComponent(path) })
    .then(response => response.json()).then(data => alert(data.message)).catch(error => console.error("Error:", error));
  }
  function generateScript(action) {
    var selected = Array.from(document.querySelectorAll("input[name='project']:checked")).map(el => el.value);
    fetch(`/${action}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({projects: selected}) })
    .then(response => response.json()).then(data => alert(data.message)).catch(error => console.error("Error:", error));
  }
  
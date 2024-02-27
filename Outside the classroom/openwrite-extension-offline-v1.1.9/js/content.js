// Send Event To Web Page
let event = new CustomEvent("ChromeID", {detail: {id: chrome.runtime.id}});
console.log(`chrome id: ${chrome.runtime.id}`);
window.dispatchEvent(event);
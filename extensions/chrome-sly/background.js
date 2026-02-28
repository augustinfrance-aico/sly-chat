// SLY Chrome Extension — Background Service Worker

// Create context menu on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "ask-sly",
    title: "Ask SLY about this",
    contexts: ["selection"]
  });
});

// Open side panel when extension icon is clicked
chrome.action.onClicked.addListener(async (tab) => {
  await chrome.sidePanel.open({ tabId: tab.id });
});

// Handle context menu click: open side panel and send selected text
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "ask-sly" && info.selectionText) {
    await chrome.sidePanel.open({ tabId: tab.id });
    // Small delay to ensure side panel is loaded before sending message
    setTimeout(() => {
      chrome.runtime.sendMessage({
        type: "context-menu-selection",
        text: info.selectionText
      });
    }, 500);
  }
});

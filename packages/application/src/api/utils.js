export const urlJoin = (...parts) => {
  parts = parts.filter((entry) => entry !== undefined);
  parts = parts.map((part, index) => {
    if (index) {
      part = part.replace(/^\//, "");
    }
    if (index !== parts.length - 1) {
      part = part.replace(/\/$/, "");
    }
    return part;
  });
  return parts.join("/");
};

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    for (let cookie of document.cookie.split(";")) {
      if (cookie.trim().substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const ROOT = window.base_url;
export const APP_URL = urlJoin(ROOT, "e2x", "grader", "app");

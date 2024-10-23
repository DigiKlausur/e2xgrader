export const urlJoin = (...parts) => {
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

export const ROOT = window.base_url;

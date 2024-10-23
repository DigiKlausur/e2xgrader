const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    for (let cookie of document.cookie.split(";")) {
      if (cookie.trim().startsWith(`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const baseSettings = {
  credentials: "same-origin",
  headers: {
    "X-CSRFToken": getCookie("_xsrf"),
  },
};

export const requests = {
  get: async (url, params = undefined) => {
    const settings = {
      ...baseSettings,
      method: "GET",
    };
    if (params !== undefined) {
      url += "?" + new URLSearchParams(params).toString();
    }
    const response = await fetch(url, settings);
    return response.json();
  },
  post: async (url, data) => {
    const settings = {
      ...baseSettings,
      method: "POST",
      body: JSON.stringify(data),
    };
    const response = await fetch(url, settings);
    return response.json();
  },
  put: async (url, data) => {
    const settings = {
      ...baseSettings,
      method: "PUT",
      body: JSON.stringify(data),
    };
    const response = await fetch(url, settings);
    return response.json();
  },
  del: async (url, data) => {
    const settings = {
      ...baseSettings,
      method: "DELETE",
      body: JSON.stringify(data),
    };
    const response = await fetch(url, settings);
    return response.json();
  },
};

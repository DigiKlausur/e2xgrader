function getCookie(name) {
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

// https://stackoverflow.com/questions/29855098/is-there-a-built-in-javascript-function-similar-to-os-path-join
export const pathJoin = (parts, sep) => {
  const separator = sep || "/";
  parts = parts.map((part, index) => {
    if (index) {
      part = part.replace(new RegExp("^" + separator), "");
    }
    if (index !== parts.length - 1) {
      part = part.replace(new RegExp(separator + "$"), "");
    }
    return part;
  });
  return parts.join(separator);
};

export class BaseAPI {
  async get(url, params = undefined) {
    let settings = {
      method: "GET",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("_xsrf"),
      },
    };
    if (params !== undefined) {
      url += "?" + new URLSearchParams(params).toString();
    }
    const response = await fetch(url, settings);
    const json = await response.json();
    return json;
  }

  async post(url, data) {
    let settings = {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("_xsrf"),
      },
      body: JSON.stringify(data),
    };
    const response = await fetch(url, settings);
    const json = await response.json();
    return json;
  }

  async put(url, data) {
    let settings = {
      method: "PUT",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("_xsrf"),
      },
      body: JSON.stringify(data),
    };
    const response = await fetch(url, settings);
    const json = await response.json();
    return json;
  }
}

export const getCookie = (name: string): string | null => {
  let cookieValue: string | null = null;
  if (document.cookie && document.cookie !== '') {
    for (const cookie of document.cookie.split(';')) {
      if (cookie.trim().startsWith(`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

export namespace Requests {
  export const baseSettings = {
    credentials: 'same-origin' as RequestCredentials,
    headers: {
      'X-CSRFToken': getCookie('_xsrf') ?? ''
    }
  };
  export const get = async (url: string, params: any = undefined) => {
    if (params) {
      url += '?' + new URLSearchParams(params);
    }
    return fetch(url, {
      ...baseSettings,
      method: 'GET'
    });
  };

  export const post = async (url: string, data: any) => {
    return fetch(url, {
      ...baseSettings,
      method: 'POST',
      body: JSON.stringify(data)
    });
  };

  export const put = async (url: string, data: any) => {
    return fetch(url, {
      ...baseSettings,
      method: 'PUT',
      body: JSON.stringify(data)
    });
  };

  export const del = async (url: string, data: any) => {
    return fetch(url, {
      ...baseSettings,
      method: 'DELETE',
      body: JSON.stringify(data)
    });
  };
}

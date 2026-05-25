// Prefer environment-configured API URL when available to avoid localhost/127.0.0.1
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

class ApiClient {
  constructor() {
    this.baseUrl = BASE_URL;
    this.token = null;
  }

  setToken(token) {
    this.token = token;
  }

  getHeaders(isFormData = false) {
    const headers = {};
    if (!isFormData) {
      headers["Content-Type"] = "application/json";
    }
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }
    return headers;
  }

  async handleResponse(response) {
    if (!response.ok) {
      let errorMessage = `Request failed with status ${response.status}`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail
              .map(err => {
                const field = err.loc ? err.loc[err.loc.length - 1] : "";
                return field ? `${field}: ${err.msg}` : err.msg;
              })
              .join(", ");
          } else if (typeof errorData.detail === "string") {
            errorMessage = errorData.detail;
          } else {
            errorMessage = JSON.stringify(errorData.detail);
          }
        } else {
          errorMessage = errorData.message || errorMessage;
        }
      } catch {
        // Response wasn't JSON
      }
      throw new Error(errorMessage);
    }

    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      return response.json();
    }
    return response;
  }

  async get(endpoint, tokenOverride = null) {
    const headers = this.getHeaders();
    if (tokenOverride) {
      headers["Authorization"] = `Bearer ${tokenOverride}`;
    }
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: "GET",
      headers,
    });
    return this.handleResponse(response);
  }

  async post(endpoint, data, tokenOverride = null) {
    const headers = this.getHeaders();
    if (tokenOverride) {
      headers["Authorization"] = `Bearer ${tokenOverride}`;
    }
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: "POST",
      headers,
      body: JSON.stringify(data),
    });
    return this.handleResponse(response);
  }

  async postForm(endpoint, formData) {
    const headers = this.getHeaders(true);
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: "POST",
      headers,
      body: formData,
    });
    return this.handleResponse(response);
  }

  async delete(endpoint) {
    const headers = this.getHeaders();
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: "DELETE",
      headers,
    });
    return this.handleResponse(response);
  }

  async download(endpoint, filename) {
    const headers = this.getHeaders();
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: "GET",
      headers,
    });

    if (!response.ok) {
      throw new Error(`Download failed with status ${response.status}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
}

const api = new ApiClient();
export default api;

const API_BASE_URL = "http://127.0.0.1:5000"; // Change this if backend URL changes

const apiRequest = async (endpoint, method = "GET", body = null) => {
  try {
    console.log("body is:", body);
    console.log("in apiRequest");

    const is_FormData = body instanceof FormData;

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method,
      headers: is_FormData
        ? {}
        : {
            "Content-Type": "application/json",
          },
      body: body ? (is_FormData ? body : JSON.stringify(body)) : null,
    });
    console.log("response in apiRequest is:", response);

    const data = await response.json();
    console.log("in api, Data is:", data);
    return data;
  } catch (error) {
    console.error("API request failed:", error);
    return { error: "Request failed. Please try again." };
  }
};

export default apiRequest;

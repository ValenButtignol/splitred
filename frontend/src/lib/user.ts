import { API_URL } from "./constants";

let creating = false; // prevent multiple requests

export async function createUserId(): Promise<string> {
  let userId = localStorage.getItem("user_id");
  if (!userId && !creating) {
    creating = true;
    try {
      const res = await fetch(`${API_URL}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const data = await res.json();
      userId = data.id as string;
      localStorage.setItem("user_id", userId);
    } finally {
      creating = false;
    }
  }
  return userId as string;
}

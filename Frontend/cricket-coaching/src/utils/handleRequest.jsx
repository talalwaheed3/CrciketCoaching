import apiRequest from "../api.jsx";

export default async function handleRequest(endpoint, method, userData = null) {
  try {
    if (method === "UPLOAD" && userData?.file) {
      console.log("here in uploading");
      const formData = new FormData();
      formData.append("file", userData.file);
      formData.append("session_id", userData.session_id);
      formData.append("shot_name", userData.shot_name);
      console.log("userData.shot_name is:", userData.shot_name);

      // const res = await fetch(endpoint, {
      //   method: "POST",
      //   body: formData,
      // });
      const res = await apiRequest(endpoint, "POST", formData);

      // if (!res.ok) throw new Error("Failed to upload file");

      // const result = await res.json();
      return res;
    }

    // alert(`endpoint:${endpoint} method:${method} userData:${userData}`)
    const data = await apiRequest(endpoint, method, userData);
    console.log("data reciecved is:", data);
    console.log("data.key reciecved is:", data.key);
    console.log("data reciecved is:", data);
    // Find the first key in response that holds an array

    // const key = Object.keys(data).find((k) => Array.isArray(data[k]) || String.isString(data[k]));

    const key = Object.keys(data).find((k) => {
      const value = data[k];
      return (
        Array.isArray(value) ||
        typeof value === "string" ||
        (typeof value === "object" && value !== null) ||
        typeof value === "boolean"
      );
    });
    console.log("key is:", key);
    console.log("data[key] is:", data[key]);

    if (!data[key]) {
      return data[key];
    }

    if (key === "arrangedSessions") {
      const list_of_data = data[key].map((session) => ({
        id: session.id,
        name: session.name,
        player: session.player,
        date: session.date,
        from: session.session_from,
        to: session.session_to,
        venue: session.venue,
      }));

      return list_of_data;
    }

    if (key === "joinedSessions") {
      const list_of_data = data[key].map((session) => ({
        id: session.id,
        name: session.name,
        coach: session.coach,
        date: session.date,
        from: session.session_from,
        to: session.session_to,
        venue: session.venue,
      }));

      return list_of_data;
    }

    if (key === "Teams") {
      const list_of_data = data[key].map((team) => ({
        id: team.id,
        name: team.name,
        total_players: team.total_players,
        // Handling coach data properly
        coach: team.coach
          ? {
              id: team.coach.id,
              name: team.coach.name,
              date_of_birth: team.coach.date_of_birth,
              experience: team.coach.experience,
              contact_no: team.coach.contact_no,
            }
          : null, // If no a single coach is assigned

        players: Array.isArray(team.players)
          ? team.players.map((player) => ({
              id: player.id,
              name: player.name,
              date_of_birth: player.date_of_birth,
              experience: player.experience,
              contact_no: player.contact_no,
              type: player.type || "Player",
            }))
          : [],
      }));
      console.log("list_of_data is:", list_of_data);
      return list_of_data;
    }

    if (key === "coachController") {
      const list_of_data = data[key].map((team) => ({
        id: team.id,
        name: team.team_name,
        players: team.team_players.map((player) => ({
          id: player.id,
          name: player.name,
          date_of_birth: player.date_of_birth,
          experience: player.experience,
          contact_no: player.contact_no,
          type: player.type,
        })),
      }));
      console.log("list_of_data is for coach_view_team is::", list_of_data);
      return list_of_data;
    }

    const list_of_data = data[key].map((user) => ({
      id: user.id,
      name: user.name,
      username: user.username,
      password: user.password,
      date_of_birth: user.date_of_birth,
      experience: user.experience,
      contact_no: user.contact_no,
      team_name: user.team_name,
      type: user.type,
    }));
    console.log("list_of_data is:", list_of_data);

    return list_of_data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return [];
  }
}

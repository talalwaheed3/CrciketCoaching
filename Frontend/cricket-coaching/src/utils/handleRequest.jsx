import apiRequest from "../api.jsx";

export default async function handleRequest(endpoint, method, userData = null) {
  try {
    if (method === "UPLOAD" && userData?.file) {
      console.log("here in uploading");
      const formData = new FormData();
      formData.append("file", userData.file);
      formData.append("session_id", userData.session_id);
      formData.append("shot_name", userData.shot_name);
      formData.append("coach_id", userData.coach_id);
      console.log("userData.shot_name is:", userData.shot_name);

      const res = await apiRequest(endpoint, "POST", formData);

      // if (!res.ok) throw new Error("Failed to upload file");

      return res;
    }

    // alert(`endpoint:${endpoint} method:${method} userData:${userData}`)
    const data = await apiRequest(endpoint, method, userData);
    console.log("data reciecved is:", data);
    console.log("data.key reciecved is:", data.key);

    if (Object.keys(data).length > 1) {
      console.log("Keys are:", Object.keys(data));
      let keys = Object.keys(data);
      if (typeof data[keys[1]] === "string") return data[keys[1]];
      if (data[keys[1]].length <= 0) {
        return [false];
      }
      const ideal_angles = data[keys[0]];

      const list_of_data = data[keys[1]].map((result) => ({
        id: result.id,
        is_shot_correct: result.is_shot_correct,
        elbow_angle: result.elbow_angle,
        shoulder_inclination: result.shoulder_inclination,
        wrist_angle: result.wrist_angle,
        knee_angle: result.knee_angle,
        hip_angle: result.hip_angle,
        bat_hip_distance: result.bat_hip_distance,
        correct_angles: result.correct_angles,
        incorrect_angles: result.incorrect_angles,
        best_frame_path: result.best_frame_path
          .split("public")[1]
          .replace(/\\/g, "/"),

        ideal_wrist_angle_from:
          ideal_angles["wrist ideal"]["Wrist Ideal Angle From"],
        ideal_wrist_angle_to:
          ideal_angles["wrist ideal"]["Wrist Ideal Angle To"],

        ideal_elbow_angle_from:
          ideal_angles["elbow ideal"]["Elbow Ideal Angle From"],
        ideal_elbow_angle_to:
          ideal_angles["elbow ideal"]["Elbow Ideal Angle To"],

        ideal_shoulder_inclination_from:
          ideal_angles["shoulder ideal"]["Shoulder Inclination Ideal From"],
        ideal_shoulder_inclination_to:
          ideal_angles["shoulder ideal"]["Shoulder Inclination Ideal To"],

        ideal_hip_angle_from: ideal_angles["hip ideal"]["Hip Ideal Angle From"],
        ideal_hip_angle_to: ideal_angles["hip ideal"]["Hip Ideal Angle To"],

        ideal_knee_angle_from:
          ideal_angles["knee angle"]["Knee Ideal Angle From"],
        ideal_knee_angle_to: ideal_angles["knee angle"]["Knee Ideal Angle To"],

        ideal_bat_hip_distance_from:
          ideal_angles["bat-hip ideal distance"]["Bat-Hip Distance Ideal From"],
        ideal_bat_hip_distance_to:
          ideal_angles["bat-hip ideal distance"]["Bat-Hip Distance Ideal To"],
      }));
      console.log("list of data now,:", list_of_data);

      return list_of_data;
    }

    // Find the first key in response that holds an array
    // const key = Object.keys(data).find((k) => Array.isArray(data[k]) || String.isString(data[k]));

    const key = Object.keys(data).find((k) => {
      const value = data[k];
      console.log("value is :", value);
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

    if (key === "Tracking Progress") {
      const progress = data[key];
      console.log("True here");
      const unpacked_data = {
        overall_accuracy: progress.overall_accuracy,
        player_id: progress.player_id,
        recommendation: progress.recommendation,
        shot_id: progress.shot_id,
        total_sessions: progress.total_sessions,
        total_shots: progress.total_shots,
        session_summary: progress.session_summary.map((session) => ({
          session_id: session.session_id,
          total_shots: session.total_shots,
          correct_shots: session.correct_shots,
          incorrect_shots: session.incorrect_shots,
          accuracy: session.accuracy,
        })),
      };

      return unpacked_data;
    }

    if (key === "Shot Ideal Range") {
      const list_of_data = data[key].map((item) => ({
        angle_id: item.angle_id,
        angle_name: item.angle_name,
        from: item.From,
        to: item.To,
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

    if (key === "playerController") {
      const team_data = data[key];
      console.log('team_data["id"] is:', team_data["id"]);
      console.log("team_data.id is:", team_data.id);
      const list_of_data = {
        id: team_data.id,
        name: team_data.team_name,
        team_coach: { coach: team_data.team_coach },
        players: team_data.team_players.map((player) => ({
          id: player.id,
          name: player.name,
          date_of_birth: player.date_of_birth,
          experience: player.experience,
          contact_no: player.contact_no,
          type: player.type,
        })),
      };
      console.log("list_of_data is for player_view_team is::", list_of_data);
      return list_of_data;
    }
    console.log('typeof(data["Results"]) is:', typeof data[key]);

    if (typeof data[key] === "string") {
      return data[key];
    }
    if (key === "Results") {
      const list_of_data = data["Results"].map((result) => ({
        id: result.id,
        is_shot_correct: result.is_shot_correct,
        elbow_angle: result.elbow_angle,
        shoulder_inclination: result.shoulder_inclination,
        wrist_angle: result.wrist_angle,
        knee_angle: result.knee_angle,
        bat_hip_distance: result.bat_hip_distance,
        correct_angles: result.correct_angles,
        incorrect_angles: result.incorrect_angles,
      }));

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

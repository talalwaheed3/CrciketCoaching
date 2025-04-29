import ViewUserTable from "../tables/ViewUserTable";

const ViewCoach = () => {
  return <ViewUserTable body={{role: "coach"}} endpoint="/manager/list_all_users" />
};

export default ViewCoach;

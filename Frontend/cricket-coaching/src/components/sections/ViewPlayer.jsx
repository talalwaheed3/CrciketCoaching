import ViewUserTable from "../tables/ViewUserTable";

const ViewPlayer = () => {
  return <ViewUserTable body={{role:"player"}} endpoint="/manager/list_all_users"/>
}

export default ViewPlayer

import UserForm from "./UserForm";

const AddPlayerForm = () => {
  return <UserForm roleType="player" apiEndpoint="/manager/add_player" />;
};

export default AddPlayerForm;

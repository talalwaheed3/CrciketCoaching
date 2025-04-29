import UserForm from "./UserForm";

const AddCoachForm = () => {
  return <UserForm roleType="coach" apiEndpoint="/manager/add_coach" />;
};

export default AddCoachForm;

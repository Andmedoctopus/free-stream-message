import { ErrorMessage, Field, Form, Formik } from "formik";
import * as Yup from "yup";

const SignupSchema = Yup.object().shape({
  firstName: Yup.string()
    .min(2, "Too short")
    .max(50, "Too long")
    .required("required"),
  lastName: Yup.string()
    .min(2, "Too short")
    .max(50, "Too long")
    .required("Required"),
  email: Yup.string().email("Invalid email address").required("Required"),
  password: Yup.string()
    .required("Required")
    .min(8, "Too short")
    .max(50, "Too long")
    .matches(
      /[a-zA-Z]/,
      "Password require at least one lowercase letter and one uppercase letter!"
    )
    .matches(/[0-9]/, "Password require at least one number!")
    .matches(/[^\w]/, "Password require at least one symbol!"),
  confirmPassword: Yup.string()
    .required("Required")
    .oneOf([Yup.ref("password")], "Must match `password` field value"),
});

export const RegistrationForm = () => {
  return (
    <div className="loginFormContainer">
      <div>
        <h1>Get Started Now</h1>
      </div>
      <div>
        <Formik
          initialValues={{
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            confirmPassword: "",
          }}
          validationSchema={SignupSchema}
          onSubmit={(values: any) => {
            const formattedString = `
            First Name: ${values.firstName},
            Last Name: ${values.lastName},
            Email: ${values.email},
            Password: ${values.password},
            Confirm Password: ${values.confirmPassword},`;
            alert(formattedString);
          }}
        >
          {({ errors, touched }) => (
            <Form>
              <div>
                <ErrorMessage name="firstName" />
              </div>
              <label htmlFor="firstName">First Name</label>
              <Field
                name="firstName"
                type="text"
                placeholder="Enter your name"
              ></Field>
              <div>
                <ErrorMessage name="lastName" />
              </div>
              <label htmlFor="lastName">Last Name</label>
              <Field
                name="lastName"
                type="text"
                placeholder="Enter your last name"
              ></Field>
              <div>
                <ErrorMessage name="email" />
              </div>
              <label htmlFor="email"></label>
              <Field
                name="email"
                type="text"
                placeholder="Enter your email"
              ></Field>
              <div>
                <ErrorMessage name="password" />
              </div>
              <label htmlFor="password">Password</label>
              <Field
                name="password"
                type="password"
                placeholder="Enter your password"
              ></Field>
              <div>
                <ErrorMessage name="confirmPassword" />
              </div>
              <label htmlFor="confirmPassword">Password conformation</label>
              <Field
                name="confirmPassword"
                type="password"
                placeholder="Confirm your password"
              ></Field>
              <button type="submit">Signup</button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

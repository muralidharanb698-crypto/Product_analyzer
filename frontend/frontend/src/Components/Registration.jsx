import React, { useState } from "react";
import '../Styles/Register.css'
import { useNavigate,Link } from "react-router-dom";
export default function Registration() {
  const navigate=useNavigate()
const [data, setData] = useState({
        name: "",
        phone: "",
        email: "",
        password: "",
        confirmPassword: ""
})


  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    setData({
      ...data,
      [e.target.name]: e.target.value
    });
  };

  const validate = () => {
    let newErrors = {};

    if (!data.name.trim()) {
      newErrors.name = "Name is required";
    } else if (data.name.length < 3) {
      newErrors.name = "Name must be at least 3 characters";
    }


    if (!/^[0-9]{10}$/.test(data.phone)) {
      newErrors.phone = "Phone must be 10 digits";
    }


    if (!/\S+@\S+\.\S+/.test(data.email)) {
      newErrors.email = "Invalid email";
    }

    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

    if (!passwordRegex.test(data.password)) {
      newErrors.password =
        "Password must contain 8 chars, uppercase, lowercase, number, special char";
    }

    if (data.password !== data.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

const handleSubmit = (e) => {
  e.preventDefault();

  if (validate()) {
    localStorage.setItem("userData", JSON.stringify(data)); 
    setData({
      name: "",
      phone: "",
      email: "",
      password: "",
      confirmPassword: ""
    });
    navigate('/')
  }
};

  return (
    <div className="container">
      <form className="form-box" onSubmit={handleSubmit}>
        <h2>Registration Form</h2>

        <input
          type="text"
          name="name"
          placeholder="Enter Name"
          value={data.name}
          onChange={handleChange}
        />
        <span>{errors.name}</span>

        <input
          type="text"
          name="phone"
          placeholder="Enter Phone"
          value={data.phone}
          onChange={handleChange}
        />
        <span>{errors.phone}</span>

        <input
          type="email"
          name="email"
          placeholder="Enter Email"
          value={data.email}
          onChange={handleChange}
        />
        <span>{errors.email}</span>

        <input
          type="password"
          name="password"
          placeholder="Enter Password"
          value={data.password}
          onChange={handleChange}
        />
        <span>{errors.password}</span>

        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={data.confirmPassword}
          onChange={handleChange}
        />
        <span>{errors.confirmPassword}</span>

        <button type="submit" >
          Register
        </button>
        <h2>Or</h2>
        <h3>Already Have a Account <Link to='/'>Login</Link></h3>
      </form>
    </div>
  );
}
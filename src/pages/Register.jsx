import React, { useState } from "react";
import httpClient from "../httpClient"; 

export const Register = (props) => {
    const [email, setEmail] = useState('');
    const [password, setPass] = useState('');

    const registerUser = async () => {
        const resp = await httpClient.post("//localhost:5000/register", {
            email,
            password,
            });

        console.log(resp.data);
    };

    // const [mobile, setPhone] = useState('');
    // const [username, setUsrName] = useState('');
    // const [address_line1, setAddress1] = useState('');
    // const [city, setCity] = useState('');
    // const [state, setState] = useState('');
    // const [zip, setZip] = useState('');
    

    // const handleSubmit = (e) => {
    //     e.preventDefault();
    //     console.log(email);

    return (
        <div className="auth-form-container">
            <h2>Register</h2>
        <form className="register-form">
            {/* <label htmlFor="username">Username</label>
            <input value={username} name="username" onChange={(e) => setUsrName(e.target.value)} id="username" placeholder="User Name" /> */}
            <label htmlFor="email">Email</label>
            <input value={email} onChange={(e) => setEmail(e.target.value)}type="email" placeholder="youremail@gmail.com" id="email" name="email" />
            <label htmlFor="password">Password</label>
            <input value={password} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
            {/* <label htmlFor="mobile">Phone Number</label>
            <input value={mobile} onChange={(e) => setPhone(e.target.value)} type="mobile" placeholder="Enter your phone number" id="mobile" name="mobile" />
            <label htmlFor="address_line1">Address Line 1</label>
            <input value={address_line1} onChange={(e) => setAddress1(e.target.value)} type="address_line1" placeholder="Enter you Address line 1" id="address_line1" name="address_line1" />
            <label htmlFor="city">City</label>
            <input value={city} onChange={(e) => setCity(e.target.value)} type="city" placeholder="Enter your City" id="city" name="city" />
            <label htmlFor="state">State</label>
            <input value={state} onChange={(e) => setState(e.target.value)} type="state" placeholder="Enter your State" id="state" name="state" />
            <label htmlFor="zip">Zip</label>
            <input value={zip} onChange={(e) => setZip(e.target.value)} type="zip" placeholder="Enter your Zip Code" id="zip" name="zip" /> */}
            <button type="button" onClick={() => registerUser()}>Register</button>
        </form>
        <button className="link-btn" onClick={() => props.onFormSwitch('login')}>Already have an account? Login here.</button>
    </div>
    )
}
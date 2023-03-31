import React, { useState } from "react";
import httpClient from "../httpClient";
//import { Helmet } from "react-helmet";


export const Login = (props) => {
    const [email, setEmail] = useState('');
    const [password, setPass] = useState('');

    
    const logInUser = async () => {
        console.log(email, password);
    
        const resp = await httpClient.post("//localhost:5000/login", {
            email,
            password,
            });

        console.log(resp.data);
    };

    return (
        <div className="auth-form-container">
            <h2>Login</h2>
            <form className="login-form" >
                <label htmlFor="email">Email</label>
                <input value={email} onChange={(e) => setEmail(e.target.value)}type="email" placeholder="youremail@gmail.com" id="email" name="email" />
                <label htmlFor="password">Password</label>
                <input value={password} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
                <button type="button" onClick={() => logInUser()}>Log In</button>
            </form>
            <button className="link-btn" onClick={() => props.onFormSwitch('register')}>Don't have an account? Register here.</button>
        </div>
   
    )
}
import React, { useState, useEffect } from "react";
import axios from "axios";

export const Login = (props) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  useEffect(() => {
    if (msg === 'You have successfully logged in!') {
      window.location.replace('//localhost:3000/landing');
    }
  }, [msg]);

  const logInUser = async () => {
    console.log(email, password);

    try {
        const resp = await axios.post("//localhost:5000/home", {
          email,
          password,
        });
        setMsg(resp.data.msg);
      
        console.log(resp.data);
      
      } catch (err) {
        console.log(err);
      }
      
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    logInUser();
  };

  return (
    <div className='container-fluid py-5'>
      <div className='row justify-content-center'>
        <div className="col-lg-7">
          <h6 className="text-primary text-uppercase font-weight-bold">Register Here</h6>
          <h1 className="mb-4">Your Contact Information</h1>
          <div className="contact-form bg-secondary" style={{ padding: "30px" }}>
            <div id="success"></div>
            <form onSubmit={handleSubmit}>
            {msg && <div className='alert alert-danger'>{msg}</div>}
              <div className="form-group">
                <select
                  className="custom-select border-0 px-4"
                  style={{ height: "47px" }}
                >
                  <option selected>User Type</option>
                  <option value="1">Admin</option>
                  <option value="2">Client</option>
                  <option value="3">Driver</option>
                </select>
              </div>

              <div className='control-group'>
                <label htmlFor='floatingInput'>Email address</label>
                <input type='email' className='form-control border-0 p-4' id='floatingInput' placeholder='name@example.com' value={email} onChange={(e) => setEmail(e.target.value)} required />
              </div>

              <div className='control-group'>
                <label htmlFor='floatingPassword'>Password</label>
                <input type='password' className='form-control border-0 p-4' id='floatingPassword' placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)} required />
              </div>

              <div className='control-group'>
                <button className='w-100 btn btn-lg btn-primary' type='submit' style={{ padding: "15px" }}>
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

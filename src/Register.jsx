import React, { useState } from 'react';
import axios from 'axios';


function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [mobile, setMobile] = useState('');
  const [address, setAddress] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [zip, setZip] = useState('');
  const [msg, setMsg] = useState('');
  const [userType, setUserType] = useState('User Type');

  const handleUserTypeChange = (e) => {
    setUserType(e.target.value);
  }

  const handleRegister = (e) => {
    e.preventDefault();
    const data = {
      name: name,
      email: email,
      password: password,
      mobile: mobile,
      address_line1: address,
      city: city,
      state: state,
      zip: zip,
    };

    axios
      .post('http://localhost:5000/register', data)
      .then((res) => {
        setMsg(res.data.msg);
        setName('');
        setEmail('');
        setPassword('');
        setMobile('');
        setAddress('');
        setCity('');
        setState('');
        setZip('');
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div className='container-fluid py-5'>
       
      <div className='row justify-content-center'>
        <div className="col-lg-7">
        <h6 className="text-primary text-uppercase font-weight-bold">Register Here</h6>
          <h1 className="mb-4">Your Contact Information</h1>
          <div className="contact-form bg-secondary" style={{ padding: "30px" }}>
          <div id="success"></div>
          <form onSubmit={handleRegister}>
          {msg && <div className='alert alert-success'>{msg}</div>}

          <div className="form-group">
            <select
              className="custom-select border-0 px-4"
              style={{ height: "47px" }}
              value={userType}
              onChange={handleUserTypeChange}
            >
              <option value="User Type">User Type</option>
              <option value="1">Admin</option>
              <option value="2">Client</option>
              <option value="3">Driver</option>
            </select>
          </div>

            <div className='control-group'>
            <label htmlFor='floatingInput'>Name</label>
              <input type='text' className='form-control border-0 p-4' id='floatingInput' placeholder='Name' value={name} onChange={(e) => setName(e.target.value)} required />
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
            <label htmlFor='floatingInput'>Mobile</label>
              <input type='text' className='form-control border-0 p-4' id='floatingInput' placeholder='Mobile' value={mobile} onChange={(e) => setMobile(e.target.value)} required />
            </div>

            <div className='control-group'>
            <label htmlFor='floatingInput'>Address</label>
              <input type='text' className='form-control border-0 p-4' id='floatingInput' placeholder='Address' value={address} onChange={(e) => setAddress(e.target.value)} required />
            </div>

            <div className='control-group'>
            <label htmlFor='floatingInput'>City</label>
              <input
                type='text' className='form-control border-0 p-4' id='floatingInput' placeholder='City' value={city} onChange={(e) => setCity(e.target.value)} required />
            </div>

            <div className='control-group'>
            <label htmlFor='floatingInput'>State</label>
                <input type='text' className='form-control border-0 p-4' id='floatingInput' placeholder='State' value={state} onChange={(e) => setState(e.target.value)} required />
            </div>

            <div className='control-group'>
            <label htmlFor='floatingInput'>Zip</label>
                <input type='text' className='form-control border-0 p-4' id='floatingInput' placeholder='Zip' value={zip} onChange={(e) => setZip(e.target.value)} required />
            </div>
            <div className='control-group'>
            <button className='w-100 btn btn-lg btn-primary' type='submit' style={{ padding: "15px" }}>
                Register
            </button>
            </div>
            </form>
        </div>
        </div>
        </div>
    </div>
    );
}

export default Register;

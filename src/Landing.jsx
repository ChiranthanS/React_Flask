import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import aboutimage from '../img/about.jpg';
//import axios from 'axios';


function Landing(){

    const navigate = useNavigate();
    const [showMenu, setShowMenu] = useState(false);

    function handleClick() {
        navigate("/login")
      }
    
      function handleDrop(){
        navigate("/login")
      }


    return(
        <body>
    {/* <!-- Topbar Start --> */}
    <div className="container-fluid bg-dark">
        <div className="row py-2 px-lg-5">
            <div className="col-lg-6 text-center text-lg-left mb-2 mb-lg-0">
                <div className="d-inline-flex align-items-center text-white">
                    <small><i className="fa fa-phone-alt mr-2"></i>+1 (812)-553-1234</small>
                    <small className="px-3">|</small>
                    <small><i className="fa fa-envelope mr-2"></i>team8@iu.edu</small>
                </div>
            </div>
            <div className="col-lg-6 text-center text-lg-right">
                <div className="d-inline-flex align-items-center">
                    <a className="text-white px-2" href="">
                        <i className="fab fa-facebook-f"></i>
                    </a>
                    <a className="text-white px-2" href="">
                        <i className="fab fa-twitter"></i>
                    </a>
                    <a className="text-white px-2" href="">
                        <i className="fab fa-linkedin-in"></i>
                    </a>
                    <a className="text-white px-2" href="">
                        <i className="fab fa-instagram"></i>
                    </a>
                    <a className="text-white pl-2" href="">
                        <i className="fab fa-youtube"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
    {/* <!-- Topbar End --> */}

    {/* <!-- Navbar Start --> */}
    <div className="container-fluid p-0">
        <nav className="navbar navbar-expand-lg bg-light navbar-light py-3 py-lg-0 px-lg-5">
            <a href="#" className="navbar-brand ml-lg-3" onClick={handleClick}>
                <h1 className="m-0 display-5 text-uppercase text-primary"><i className="fa fa-truck mr-2"></i>Knock Knock</h1>
            </a>
            <button type="button" className="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse justify-content-between px-lg-3" id="navbarCollapse">
                <div className="navbar-nav m-auto py-0">
                    <a href="#" class="nav-item nav-link active" onClick={handleClick}>Home</a>
                    <a href="#" class="nav-item nav-link" onClick={handleClick}>About</a>
                    <a href="#" class="nav-item nav-link" onClick={handleClick}>Service</a>
                    <a href="#" class="nav-item nav-link" onClick={handleClick}>Price</a>
                    <div className="nav-item dropdown">
                    <a href="#" className="nav-link dropdown-toggle" onClick={() => setShowMenu(!showMenu)}>
                        Pages
                    </a>
                    <div className={`dropdown-menu rounded-0 m-0${showMenu ? ' show' : ''}`}>
                        <a href="#" className="dropdown-item" onClick={handleDrop}>
                        Blog Grid
                        </a>
                        <a href="#" className="dropdown-item" onClick={handleDrop}>
                        Blog Detail
                        </a>
                    </div>
                    </div>
                    <a href="#" className="nav-item nav-link" onClick={handleClick}>Contact</a>
                </div>
                <a href="#" className="btn btn-primary py-2 px-4 d-none d-lg-block" onClick={handleClick}>Login Here</a>
            </div>
        </nav>
    </div>
    {/* <!-- Navbar End --> */}

    {/* <!-- Header Start --> */}
    <div className="jumbotron jumbotron-fluid mb-5">
        <div className="container text-center py-5">
            <h1 className="text-primary mb-4">Safe & Faster</h1>
            <h1 className="text-white display-3 mb-5">Logistics Services</h1>
            <div className="mx-auto" style={{width: "100%", maxWidth: "600px"}}>
                <div className="input-group">
                    <input type="text" className="form-control border-light" style={{padding:"30px"}} placeholder="Tracking Id"/>
                    <div className="input-group-append">
                        <button className="btn btn-primary px-3">Track & Trace</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {/* <!-- Header End --> */}

    {/* <!-- About Start --> */}
    <div className="container-fluid py-5">
        <div className="container">
            <div className="row align-items-center">
                <div className="col-lg-5 pb-4 pb-lg-0">
                    <img className="img-fluid w-100" src={aboutimage} alt=""/>
                    <div className="bg-primary text-dark text-center p-4">
                        <h3 className="m-0">25+ Years Experience</h3>
                    </div>
                </div>
                <div className="col-lg-7">
                    <h6 className="text-primary text-uppercase font-weight-bold">About Us</h6>
                    <h1 className="mb-4">Opening doors to seamless deliveries, Trust Knock Knock</h1>
                    <p className="mb-4">Knock Knock offers personalized, reliable, and cost-effective logistic delivery services with advanced tracking and monitoring systems. Our commitment to minimizing our carbon footprint positively impacts the environment and communities we serve. With our innovative approach and customer satisfaction focus, we can take your business to the next level.</p>
                </div>
            </div>
        </div>

    {/* <!--  Quote Request Start --> */}
    <div className="container-fluid bg-secondary my-5">
        <div className="container">
            <div className="row align-items-center">
                <div className="col-lg-7 py-5 py-lg-0">
                    <h6 class="text-primary text-uppercase font-weight-bold">Get A Quote</h6>
                    <h1 class="mb-4">Request A Free Quote</h1>
                    <p class="mb-4">Streamline your logistics and transport operations with Knock Knock. Request a free quote today on our website and discover personalized solutions tailored to your needs. With our commitment to customer satisfaction, innovation, and efficiency, we're confident we can provide the reliable and cost-effective logistics solutions you need to succeed. Don't wait, get your free quote now and experience the Knock Knock difference!</p>
                    <div class="row">
                        <div class="col-sm-4">
                            <h1 class="text-primary mb-2" data-toggle="counter-up">225</h1>
                            <h6 class="font-weight-bold mb-4">SKilled Experts</h6>
                        </div>
                        <div class="col-sm-4">
                            <h1 class="text-primary mb-2" data-toggle="counter-up">1050</h1>
                            <h6 class="font-weight-bold mb-4">Happy Clients</h6>
                        </div>
                        <div class="col-sm-4">
                            <h1 class="text-primary mb-2" data-toggle="counter-up">2500</h1>
                            <h6 class="font-weight-bold mb-4">Complete Projects</h6>
                        </div>
                    </div>
                </div>
                <div class="col-lg-5">
                    <div class="bg-primary py-5 px-4 px-sm-5">
                        <form class="py-5">
                            <div class="form-group">
                                <input type="text" class="form-control border-0 p-4" placeholder="Your Name" required="required" />
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control border-0 p-4" placeholder="Your Email" required="required" />
                            </div>
                            <div className="form-group">
                                <select className="custom-select border-0 px-4" style={{ height: "47px" }}>
                                    <option selected>User Type</option>
                                    <option value="1">Admin</option>
                                    <option value="2">Client</option>
                                    <option value="3">Driver</option>
                                </select>
                            </div>
                            <div>
                                <button class="btn btn-dark btn-block border-0 py-3" type="submit">Get A Quote</button>
                            </div>
                            {/* <a href="#" class="btn btn-primary mt-3 py-2 px-4" onClick={handleClick}>Login</a> */}
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
    {/* <!-- Quote Request Start --> one extra div tag added here*/}
    </body>

    )
 
};

export default Landing;
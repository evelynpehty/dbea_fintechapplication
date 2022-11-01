<template>
    <div class="container-fluid" id="team">
        <div class="row mt-5 d-flex justify-content-center">
            <div class="col-md-6">
                <h1>Meet Our Team</h1>
                <h6>OUR HIGHLY QUALIFIED AND SKILLED TEAM</h6>
                <h6 class="mb-3">Meet the team that made all these possible.</h6>
            </div>
        </div>

        <div class="row d-flex justify-content-center">
            <div class="col-xl-2 col-lg-3 col-md-4 col-sm-4">
                <div class="member">
                    <div class="member-img">
                        <img src="../assets/evelyn.jpg" class="img-fluid" alt="">
                    </div>
                    <div class="member-info">
                        <h4>Evelyn Peh</h4>
                        <span class="text-white">Member</span>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a href="#"><i class="fab fa-pinterest-p"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-xl-2 col-lg-3 col-md-4 col-sm-4">
                <div class="member">
                    <div class="member-img">
                        <img src="../assets/pei.png" class="img-fluid" alt="">
                    </div>
                    <div class="member-info">
                        <h4>Koh Pei Ling</h4>
                        <span class="text-white">Member</span>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a href="#"><i class="fab fa-pinterest-p"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-xl-2 col-lg-3 col-md-4 col-sm-4">
                <div class="member">
                    <div class="member-img">
                        <img src="../assets/jay.jpg" class="img-fluid" alt="">
                    </div>
                    <div class="member-info">
                        <h4>Too Min Jay</h4>
                        <span class="text-white">Member</span>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a href="#"><i class="fab fa-pinterest-p"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row d-flex justify-content-center">
            <div class="col-xl-2 col-lg-3 col-md-4 col-sm-4">
                <div class="member">
                    <div class="member-img">
                        <img src="../assets/wanxin.png" class="img-fluid" alt="">
                    </div>
                    <div class="member-info">
                        <h4>Wan Xin</h4>
                        <span class="text-white">Member</span>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a href="#"><i class="fab fa-pinterest-p"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-xl-2 col-lg-3 col-md-4 col-sm-4">
                <div class="member">
                    <div class="member-img">
                        <img src="../assets/genevieve.png" class="img-fluid" alt="">
                    </div>
                    <div class="member-info">
                        <h4>Genevieve Tai</h4>
                        <span class="text-white">Member</span>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a href="#"><i class="fab fa-pinterest-p"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-xl-2 col-lg-3 col-md-4 col-sm-4">
                <div class="member">
                    <div class="member-img">
                        <img src="../assets/ruixin.jpg" class="img-fluid" alt="">
                    </div>
                    <div class="member-info">
                        <h4>Teo Rui Xin</h4>
                        <span class="text-white">Member</span>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a href="#"><i class="fab fa-pinterest-p"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  
</template>

<style scoped>
#team {
    text-align: center;
}
#team h2 {
    position: relative;
    padding: 0px 0px 15px;
}
#team p {
    font-size: 15px;
    font-style: italic;
    padding: 0px;
    margin: 25px 0px 40px;
}
#team .member {
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    background-color: #ffffff;
    padding: 10px;
    border-radius: 15px 0px 15px 0px;
    box-shadow: 0px 1px 6px 0px rgba(0, 0, 0, 0.4);
}
#team .member .member-info {
    display: block;
    position: absolute;
    bottom: 0px;
    left: -200px;
    transition: 0.4s;
    padding: 15px 0;
    background: rgba(0, 0, 0, 0.4);
}
#team .member:hover .member-info {
    left: 0px;
    right: 0px;
}
#team .member h4 {
    font-weight: 700;
    margin-bottom: 2px;
    font-size: 18px;
    color: #fff;
}
#team .member span {
    font-style: italic;
    display: block;
    font-size: 13px;
}
#team .member .social-links {
    margin-top: 15px;
}
#team .member .social-links a {
    transition: none;
    color: #fff;
}
#team .member .social-links a:hover {
    color: #ffc107;
}
#team .member .social-links i {
    font-size: 18px;
    margin: 0 4px;
}
.site-footer {
    background-color: #015A06;
}   
.site-footer a {
    color: lightgray;
    text-decoration: none;
}
.site-footer a:hover {
    color: white;
}
.btn:hover {
  background-color: #93b895;
}
</style>
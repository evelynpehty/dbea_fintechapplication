<template>
    <nav class="navbar navbar-expand-md navbar-light fixed-top bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="/"><img src="../assets/Simplifi.png" height="40" width="50" /></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <a class="nav-link mx-2" aria-current="page" href="/#about">About Us</a>
            </li>
            <li class="nav-item">
              <a class="nav-link mx-2" href="/#contact">Contact Us</a>
            </li>
            <li class="nav-item">
              <a class="nav-link mx-2" href="/OurTeam">Our Team</a>
            </li>
          </ul>
          <div class="d-flex">
            <a class="btn btn-outline-success" href="/LoginPage" >Login</a>
          </div>
        </div>
      </div>
    </nav>
  </template>
    
    <script>
  
    
    export default {
      name: "MainNavigation",
     
    }
    
    </script>
    
    <style scoped>
      /* Show it is fixed to the top */
      .btn {
        margin: 10px;
      }
    </style>
     
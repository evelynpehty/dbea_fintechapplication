<template>
  <div class="container-fluid p-0">
    <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="../assets/banner.jpg" class="d-block w-100" alt="...">
          <div class="carousel-caption d-none d-md-block">
            <h1>Trading has never been easier</h1>
            <p>Start trading with us now</p>
          </div>
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <div id="about" class="container-fluid">
      <div class="row my-5">
        <div class="col-md-6 ps-5 my-auto d-block about">
          <h1>About Us</h1>
          <h5>SimpliFi is a trading platform that offers easy-to-use interfaces where investors can purchase and sell stocks. Beyond that, it includes features that enable investors to make well-informed decisions about their investments, such as real-time quotes, business and financial news feeds, as well as technical analysis tools which provide investors with suggestions on how they can optimise their current portfolio.</h5>
        </div>
        <div class="col-md-6">
          <img src="../assets/about-us.jpg" class="rounded mx-auto d-block img-fluid" alt="..." />
        </div>
      </div>
    </div>

    <div id="contact" class="container-fluid"></div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss" scoped>
h1 {
  color: white !important;
}

.about h1{
  color: var(--purple) !important;
}
</style>
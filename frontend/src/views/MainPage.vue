<template>
  <div class="container-fluid p-0">
    <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="../assets/banner.jpg" class="d-block w-100" alt="...">
          <div class="carousel-caption d-none d-md-block">
            <h1>Trading has never been easier</h1>
            <p>Start trading with us now</p>
          </div>
        </div>
        <div class="carousel-item">
          <img src="../assets/banner.jpg" class="d-block w-100" alt="...">
          <div class="carousel-caption d-none d-md-block">
            <h5>Second slide label</h5>
            <p>Some representative placeholder content for the second slide.</p>
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
          <h5>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis dictum mauris mollis, ullamcorper magna rhoncus, ullamcorper lacus. Etiam enim libero, rutrum eget commodo sit amet, sollicitudin et lorem. Cras placerat tortor erat, at convallis massa malesuada quis. Duis nec eleifend sapien. Pellentesque ultricies risus ac ex feugiat dictum. Nulla feugiat enim ac eros ultrices pharetra. Quisque tempor urna tellus, ut iaculis diam lobortis sit amet.</h5>
        </div>
        <div class="col-md-6">
          <img src="../assets/about-us.jpg" class="rounded mx-auto d-block" alt="..." />
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
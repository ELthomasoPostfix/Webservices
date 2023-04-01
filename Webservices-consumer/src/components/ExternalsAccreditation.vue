<script setup lang="ts">
/** A collection of the required accreditations for external services. */

import TMDBLogo from './logos/TMDBLogo.vue';
</script>

<template>
  <div class="credit-container">
    <!-- TMDB accreditation -->
    <TMDBLogo/>
    <!-- Credit notice -->
    <p class="credit-text">
      <b>This product uses the TMDB API but is not endorsed or certified by TMDB.</b>
    </p>
    <br>
  </div>

</template>

<style setup>
.credit-container {
  margin-top: 1rem;
}

.credit-text {
  display: inline;
}
</style>
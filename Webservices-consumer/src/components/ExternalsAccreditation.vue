<script setup lang="ts">
/** A collection of the required accreditations for external services. */

import TMDBLogo from './logos/TMDBLogo.vue';
</script>

<template>

  <!-- TMDB accreditation -->
  <TMDBLogo/>
  <!-- Credit notice -->
  <p class="credit-text">
    <b>This product uses the TMDB API but is not endorsed or certified by TMDB.</b>
  </p>
  <br>

</template>

<style setup>
.credit-text {
  display: inline;
}
</style>
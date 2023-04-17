<script setup lang="ts">
import MainContentHeader from '@/components/MainContentHeader.vue';
</script>

<template>
  <main>
    <MainContentHeader title="Webservices Consumer" />
    <p>
      This application consumes the <em>Webservices API</em>, that partially acts as a proxy for the TMDB API.
      The Webservices API also provides several functions that do not utilize the TMDB API.
      The like/un-like functionality globally marks or unmarks a movie as 'liked', which is stored in the API backend itself.
      The delete functionality removes a movie from any and all Webservices API results, which is also stored in the API backend itself.
      The plot functionality utilizes the quickchart API in addition to the TMDB API.
    </p>
    <p>
      Any mention of the Webservices API, or a <b>/api/...</b> Webservices endpoint specifically, refers to the implementation of the RESTful API backend described in the project requirements.
    </p>
  </main>
</template>

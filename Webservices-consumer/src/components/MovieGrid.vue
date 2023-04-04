<script setup lang="ts">
/** A grid of movie representation cards, divided into more columns, up to three columns, as screen width expands */

import type { Movie } from '@/code/interfaces';

import MovieCard from './MovieCard.vue';

defineProps<{
    /** The movie data to display inside individual movie cards. */
    movies_data: Array<Movie>;
}>();
</script>

<template>
    <div class="movie-grid">
      <div v-for="(movie) in movies_data" :key="movie.title">
        <MovieCard class="grid-element" :movie="movie"/>
      </div>
    </div>
</template>

<style scoped>
.grid-element {
  height: 100%;   /** Force movie cards on the same row to be equally tall */
}

.movie-grid {
  display: grid;
  grid-template-columns: 1fr;   /** Default one column of 1 fraction of 100% space */
  grid-template-rows: 1fr;      /** Default 1 row of 1 fraction of 100% space */
  column-gap: 1rem;
  row-gap: 1rem;
}

@media (min-width: 512px) {
  .movie-grid {
    grid-template-columns: 1fr 1fr;   /** If available space wide enough, 2 columns of 1 fraction of 100% each, meaning 50% each */
  }
}

@media (min-width: 1280px) {
  .movie-grid {
    grid-template-columns: 1fr 1fr 1fr;   /** If available space wide enough, 3 columns of 1 fraction of 100% each, meaning 33.33% each */
  }
}
</style>
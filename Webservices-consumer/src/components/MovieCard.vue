<script setup lang="ts">
import type { Movie } from '../code/interfaces';

defineProps<{
    /** The movie to display */
    movie: Movie;
}>();
</script>

<template>
  <div class="movie-card">
    <!-- Card header -->
    <h6 class="movie-card-title">
      <div>
        {{ movie.title }}
      </div>
    </h6>
    <!-- Card content -->
    <div class="movie-card-body ">
      <p>
        Movie ID: {{ movie.id }}
      </p>
      <p v-if="movie.runtime !== undefined">
        Runtime: {{ movie.runtime }}
      </p>
      <p v-if="movie.genre_ids !== undefined">
        Genre IDs: {{ movie.genre_ids.join(", ") }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.movie-card {
  border: 2px solid;
  border-radius: 10px;
  display: grid;
}

.movie-card-title {
  margin: 10px;
}

.movie-card-body {
  margin-bottom: 5px;
}

p {
  margin-left: 1rem;
  margin-bottom: 0rem;
}
</style>
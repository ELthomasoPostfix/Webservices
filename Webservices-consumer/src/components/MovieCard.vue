<script setup lang="ts">
import type { Movie } from '../code/interfaces';
defineProps<{
    /** The movie to display */
    movie: Movie
}>();
</script>

<template>
    <div class="movie-card">
        <h6 class="movie-card-title">
            {{ movie.title }}
        </h6>
    </div>
</template>

<style scoped>
.movie-card {
  border: 2px solid;
  border-radius: 10px;
  display: grid;
}

.movie-card-title {
  padding: 20px;
}
</style>
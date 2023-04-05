<script setup lang="ts">
import { reactive } from "vue";

import MovieCard from './MovieCard.vue';

/** The props should take into account that the represented movie is an invalid TMDB resource.
 *
 * A user of this component would normally only be able to provide limited information, such
 * as the movie's TMDB id.
 */
const props = defineProps<{
    /** The movie TMDB id */
    movieId: number
}>();

/** The '404 Not Found' representation of the movie data */
const movie = reactive({
    title: "Movie Not Found",
    id: props.movieId
});
</script>

<template>
    <MovieCard class="movie-404-card" :movie="movie" v-bind="$attrs"/>
</template>

<style scoped>
.movie-404-card {
    border-color: red;
}
</style>
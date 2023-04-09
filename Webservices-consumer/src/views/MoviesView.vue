<script setup lang="ts">
import { ref, type Ref, computed, reactive } from "vue";
import type { Movie } from "../code/interfaces";

import MainContentHeader from "@/components/MainContentHeader.vue";
import MovieGrid from "@/components/MovieGrid.vue";


/** Movies input state */
const amount: Ref<number> = ref(0);

/** Movies Webservices api results */
const movies_data: Array<Movie> = reactive([]);

/** Movies amount representation string for display purposes */
const amount_repr_string = computed(() => {
  return amount.value > 0 ? amount.value.toString() : 'X';
})

/** The response format of the `/movies` api endpoint. */
interface MoviesResponse {
  /** A message that can be displayed to the user */
  message: string;
  /** A developer/debug error message */
  error?: string;
  /** The requested movies */
  result: Array<Movie>;
}

/** Fetch the first x movies and update the state variable upon success */
function onClick() {
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies?amount=${amount.value}`, {
      credentials: "same-origin"
    })
  .then(async (response) => {
      if (response.status >= 400) {
          console.log("Failed to fetch: status", response.status);
          return;
      }
      response.json().then((response_json: MoviesResponse) => {
        const result = response_json["result"];

        /** Unpack response data */
        movies_data.splice(0);
        movies_data.push(...result);
      });
  })
  .catch((e) => {
      console.log("Error during fetch: ", e);
      return;
  })
}

/** Event handler for the 'like' event.
 *
 * Update the like status of this page's movies state.
 * @param movie The movie to update the liked state of
 */
async function onTriggerLike(movie: Movie) {
  movie.liked = !movie.liked;
}

/** Event handler for the 'delete' event.
 *
 * Update this page's movies state by removing the deleted movie.
 * @param movie The movie to remove from the page's movies state
 */
async function onTriggerDelete(movie: Movie) {
  movies_data.splice(movies_data.indexOf(movie), 1);
}
</script>

<template>
  <main>
    <!-- View header -->
    <MainContentHeader title="Movies"/>

    <!-- View content -->
    <form @submit.prevent=""
      style="margin-top: 1rem; margin-bottom: 1rem;"
    >
      <label for="input-movies" style="padding-right: 1rem;">First X movies</label>
      <input style="margin-right: 1rem; min-width: 100px; max-width: 200px;" id="input-movies" type="number" min="0" v-model="amount"/>
      <button id="button-movies" @click="onClick">Get {{ amount_repr_string }} movies</button>
    </form>

    <p v-if="movies_data.length == 0" id="results-movies">No results yet</p>
    <MovieGrid v-else
      :movies-data="movies_data"
      @delete="onTriggerDelete"
      @like="onTriggerLike"
    />
</main>
</template>

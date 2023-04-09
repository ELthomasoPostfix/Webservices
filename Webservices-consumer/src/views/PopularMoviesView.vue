<script setup lang="ts">
import { ref, type Ref, computed, reactive } from "vue";
import type { Movie } from "../code/interfaces";

import MainContentHeader from "@/components/MainContentHeader.vue";
import MovieGrid from "@/components/MovieGrid.vue";


/** Popular x input state */
const popular_x: Ref<number> = ref(0);

/** Popular x api results */
const popular_x_data: Array<Movie> = reactive([]);

/** Transformed popular x api results, suitable to be displayed */
const displayable_data = computed(() => {
  return popular_x_data.map((elem: Movie, index: number) => {
    return {
      ...elem,
      title: `${index+1}. ${elem.title}`
    }
  })
})

/** Popular x representation string for display purposes */
const popular_x_repr_string = computed(() => {
  return popular_x.value > 0 ? popular_x.value.toString() : 'X';
})

/** The response format of the `/movies/popular` api endpoint. */
interface MoviesResponse {
  /** A message that can be displayed to the user */
  message: string;
  /** A developer/debug error message */
  error?: string;
  /** The requested movies */
  result: Array<Movie>;
}

/** Fetch the first x popular movies and update the state variable upon success */
function onClick() {
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies/popular?amount=${popular_x.value}`, {
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
        popular_x_data.splice(0);
        popular_x_data.push(...result);
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
  popular_x_data[displayable_data.value.indexOf(movie)].liked = !movie.liked;
}

/** Event handler for the 'delete' event.
 *
 * Update this page's movies state by removing the deleted movie.
 * @param movie The movie to remove from the page's movies state
 */
async function onTriggerDelete(movie: Movie) {
  popular_x_data.splice(displayable_data.value.indexOf(movie), 1);
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
      <label for="input-popularX" style="padding-right: 1rem;">First X popular movies</label>
      <input style="margin-right: 1rem; min-width: 100px; max-width: 200px;" id="input-popularX" type="number" min="0" v-model="popular_x"/>
      <button id="button-popularX" @click="onClick">Get popular {{ popular_x_repr_string }}</button>
    </form>

    <p v-if="displayable_data.length == 0" id="results-popularX">No results yet</p>
    <MovieGrid v-else
      :movies-data="displayable_data"
      @delete="onTriggerDelete"
      @like="onTriggerLike"
    />
</main>
</template>

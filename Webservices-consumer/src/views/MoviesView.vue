<script setup lang="ts">
import { ref, type Ref, computed } from "vue";
import type { Movie } from "../code/interfaces";

import MainContentHeader from "@/components/MainContentHeader.vue";
import MovieCard from "../components/MovieCard.vue";


/** Popular x input state */
const popular_x = ref(0);

/** Popular x api results */
const popular_x_data: Ref<Array<{ title: string }>> = ref([]);

/** Popular x representation string for display purposes */
const popular_x_repr_string = computed(() => {
  return popular_x.value > 0 ? popular_x.value.toString() : 'X';
})

/** The response format of the movies api endpoint. */
interface MoviesResponse {
  message: string,
  error?: string,
  result: {
    popularx?: Array<Movie>
  },
}

function onClick() {
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies/?popularx=${popular_x.value}`, {
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
        if ("popularx" in result) popular_x_data.value = result.popularx!;
      });
  })
  .catch((e) => {
      console.log("Error during fetch: ", e);
      return;
  })

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

    <p v-if="popular_x_data.length == 0" id="results-popularX">No results yet</p>
    <!-- List of fetched movies -->
    <div v-else class="movie-grid">
      <div v-for="(value, index) in popular_x_data" :key="value.title">
        <MovieCard class="grid-element" :title="`${index+1}. ${value.title}`"/>
      </div>
    </div>
</main>
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

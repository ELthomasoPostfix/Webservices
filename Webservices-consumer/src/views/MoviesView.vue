<script setup lang="ts">
import { ref, type Ref, computed } from "vue";
import type { Movie } from "../code/interfaces";

import MainContentHeader from "@/components/MainContentHeader.vue";


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
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies?popularx=${popular_x.value}`, {
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
    <MainContentHeader title="Movies"/>

    <!-- Movies view content -->
    <form @submit.prevent="">
      <label style="padding-right: 1rem;" for="input-popularX">First {{ popular_x_repr_string }} popular movies</label>
      <input id="input-popularX" type="number" min="0" v-model="popular_x"/>
      <button id="button-popularX" @click="onClick">Get popular {{ popular_x_repr_string }}</button>
    </form>

    <p v-if="popular_x_data.length == 0" id="results-popularX">No results yet</p>
    <ul v-else>
      <li v-for="(value) in popular_x_data" :key="value.title">
        {{ value.title }}
      </li>
    </ul>
  </main>
</template>
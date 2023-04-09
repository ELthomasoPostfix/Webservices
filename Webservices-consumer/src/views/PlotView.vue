<script setup lang="ts">
import { ref, type Ref, computed } from "vue";

import MainContentHeader from "../components/MainContentHeader.vue";

/** The array of movie ids to plot */
const movie_ids: Ref<Set<number>> = ref(new Set());
const movie_ids_list = computed(() => {
  return [...movie_ids.value];
})

/** A potential movie id to add to the fetch */
const new_movie_id: Ref<number> = ref(0);

/** The image to display */
const image_data: Ref<Blob | undefined> = ref(undefined);
const image_object_url = computed(() => {
    return image_data.value === undefined ? undefined : URL.createObjectURL(image_data.value);
});

/** Fetch an average score barplot for the specified movie ids */
async function onClick() {
  const movie_ids_string: string = movie_ids_list.value.join(",");
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies/average-score-plot?movie_ids=${movie_ids_string}`)
  .then(async (response) => {        
      const header_ct = response.headers.get("Content-Type");

      if (response.status >= 400) return;
      if (header_ct !== "image/webp") return;

      return response.blob()
  })
  .then(async (image: Blob | undefined) => {
      image_data.value = image;
  });
}

/** Add the currently selected movie id to the plot query */
function onSelectMovie() {
  movie_ids.value.add(new_movie_id.value);
}

/** Remove a specific selected movie id from the plot query */
function onDeselectMovie(movie_id: number) {
  movie_ids.value.delete(movie_id);
}
</script>

<template>
  <main>
    <!-- View header -->
    <MainContentHeader title="Plot"/>

    <!-- Movies selection -->
    <div class="plot-input-container">
      <form @submit.prevent="">
        <label for="input-plot-ids" style="padding-right: 1rem;">Add movie to plot by TMDB id</label>
        <input style="margin-right: 1rem; min-width: 100px; max-width: 200px;" id="input-plot-ids" type="number" min="0" v-model="new_movie_id"/>
        <button id="button-plot-ids" @click="onSelectMovie">Add {{ new_movie_id }}</button>
      </form>
  
      <p style="margin-top: 1rem;">
        The following TMDB movie ids will used to construct a vote average barplot:
      </p>

      <p v-if="movie_ids_list.length === 0"
        style="padding-left: 1rem;"
      >
        Selection is empty ...
      </p>
      <div v-else>
        <button v-for="(movie_id) in movie_ids"
          class="movies-selection-btn"
          :key="movie_id"
          @click="onDeselectMovie(movie_id)"
        >
          {{ movie_id }}
        </button>
      </div>
    </div>
    
    <!-- Plot retrieval -->
    <h4>Plot</h4>
    <div>
      <button
        @click="onClick"
      >
          Get Plot
      </button>
      <div>
        <img v-if="image_object_url !== undefined"
          :src="image_object_url"
          :alt="`Average score barplot for TMDB movie ids: ${movie_ids.size > 0 ? movie_ids_list.join(', ') : 'no ids chosen'}`"
        >
        <p v-else
          style="padding-left: 1rem; margin-top: 1em;"
        >
          No plot yet ...
        </p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.plot-input-container {
  margin-bottom: 1rem;
}

.movies-selection-btn {
  margin-right: 2px;
}

@media (hover: hover) {
  .movies-selection-btn:focus {
    background-color: red;
  }
  .movies-selection-btn:hover {
    background-color: red;
  }
}
</style>
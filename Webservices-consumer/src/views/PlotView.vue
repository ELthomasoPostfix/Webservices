<script setup lang="ts">
import { ref, type Ref, computed } from "vue";
import { isNumeric } from "@/code/utils";

import MainContentHeader from "../components/MainContentHeader.vue";

/** The array of movie ids to plot */
const movie_ids: Ref<Set<number>> = ref(new Set());
const movie_ids_list_repr = computed(() => {
  return [...movie_ids.value];
})

/** The movie ids that have been rejected by the Webservices API */
const movie_ids_rejected: Ref<Set<number>> = ref(new Set());

/** A potential movie id to add to the fetch */
const new_movie_id: Ref<number> = ref(0);

/** The image to display */
const image_data: Ref<Blob | undefined> = ref(undefined);
const image_object_url = computed(() => {
    return image_data.value === undefined ? undefined : URL.createObjectURL(image_data.value);
});

/** Fetch an average score barplot for the specified movie ids */
async function onClick() {
  const movie_ids_string: string = movie_ids_list_repr.value.join(",");
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies/average-score-plot?movie_ids=${movie_ids_string}`)
  .then(async (response) => {        
      const header_ct = response.headers.get("Content-Type");
      const header_emi = response.headers.get("Excluded-Movie-IDs");

      if (response.status >= 400) return;
      if (header_ct !== "image/webp") return;

      if (header_emi !== null) {
        const excluded_ids = header_emi.split(',');
        excluded_ids.forEach((rejected_id: string) => {
          if (!isNumeric(rejected_id)) return;
          const rejected_id_num: number = parseInt(rejected_id);

          movie_ids_rejected.value.add(rejected_id_num);
          movie_ids.value.delete(rejected_id_num);
        })
      }

      return response.blob()
  })
  .then(async (image: Blob | undefined) => {
      image_data.value = image;
  });
}

/** Add the currently selected movie id to the plot query */
function onSelectMovie() {
  if (movie_ids_rejected.value.has(new_movie_id.value)) return;

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
    <MainContentHeader title="Average Score Plot"/>

    <p>
      This page consumes the <b>/api/movies/average-score-plot</b> Webservices endpoint, which represents a plot of the TMDB vote average values of the specified movies.
      The Webservices API does this by calling the TMDB API to collect the vite averages and then the quickchart API to generate the plot.
    </p>

    <p>
      The <b>/api/movies/average-score-plot</b> Webservices endpoint <em>is</em> part of the project requirements.
    </p>

    <!-- Movies selection -->
    <div class="plot-input-container">
      <form @submit.prevent="">
        <label for="input-plot-ids" style="padding-right: 1rem;">Add movie to plot by TMDB id</label>
        <input style="margin-right: 1rem; min-width: 100px; max-width: 200px;" id="input-plot-ids" type="number" min="0" v-model="new_movie_id"/>
        <button id="button-plot-ids" @click="onSelectMovie">Add {{ new_movie_id }}</button>
      </form>
  
      <!-- Selected movie ids -->
      <p style="margin-top: 1rem;">
        The following TMDB movie ids will used to construct a vote average barplot:
      </p>

      <p v-if="movie_ids_list_repr.length === 0"
        style="padding-left: 1rem;"
      >
        Selection is empty ...
      </p>
      <div v-else>
        <button v-for="(movie_id) in movie_ids"
          class="movies-selection-btn-list movies-selection-btn"
          :key="movie_id"
          @click="onDeselectMovie(movie_id)"
        >
          {{ movie_id }}
        </button>
      </div>
    
      <!-- Rejected movie ids -->
      <div v-if="movie_ids_rejected.size > 0">
        <p style="margin-top: 1rem;">
          The following TMDB movie ids have been rejected by the Webservices API. They are either deleted or don't exist:
        </p>

        <button v-for="(movie_id) in movie_ids_rejected"
          disabled
          class="movies-selection-btn-list"
          :key="movie_id"
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
          :alt="`Average score barplot for TMDB movie ids: ${movie_ids.size > 0 ? movie_ids_list_repr.join(', ') : 'no ids chosen'}`"
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

.movies-selection-btn-list {
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
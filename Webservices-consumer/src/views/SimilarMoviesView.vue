<script setup lang="ts">
import { ref, type Ref, computed } from "vue";
import { isNumber } from "../code/utils";
import type { Movie } from "../code/interfaces";

import MainContentHeader from "@/components/MainContentHeader.vue";
import HourglassLogo from "@/components/logos/HourglassLogo.vue"
import MovieCard from "@/components/MovieCard.vue";
import Movie404Card from "@/components/Movie404Card.vue";
import MoviePlacedolderCard from "@/components/MoviePlaceholderCard.vue";
import MovieGrid from "@/components/MovieGrid.vue";


/** Similar movies input state */
const movie_id: Ref<number> = ref(0);
const amount = ref(0);

const matching_genres: Ref<boolean> = ref(false);
const overlapping_actors: Ref<boolean> = ref(false);
const similar_runtime: Ref<boolean> = ref(false);

/** Similar movies api results */
const similar_movies_data: Ref<Array<Movie>> = ref([]);

/** Similar movies reference movie api result */
const reference_movie_data: Ref<Movie | undefined> = ref(undefined);

/** Similar movies api response code */
const similar_response_code: Ref<number> = ref(0);

/** The number of similar movies that are missing a runtime to fetch the runtime for */
const runtime_fetch_amount: Ref<number> = ref(10);
const is_updating_runtime: Ref<boolean> = ref(false);

const runtime_updater_class = computed(() => {
  return is_updating_runtime.value ? "runtime-updater-running" : "runtime-updater-idle"
})

/** The response format of the `/movies/<mov_id>/similar` api endpoint. */
interface SimilarMoviesResponse {
  message: string;
  error?: string;
  result: Array<Movie>;
  reference_movie: {
    title: string,
    id: number,
    genres: Array<{ id: number }>,
    runtime: number | undefined
  };
}

/** The response format of the `/movies/<mov_id>` api endpoint. */
interface MoviesResponse {
  message: string;
  error?: string;
  result: Movie;
}

/** Fetch the first x similar movies and update the state variable upon success */
function onClick() {
  if (!isNumber(movie_id.value)) return;
  similar_response_code.value = 0;
  similar_movies_data.value = [];
  reference_movie_data.value = undefined;

  let query_string: string = "";
  if (matching_genres.value) query_string += "&matching_genres";
  if (overlapping_actors.value) query_string += "&overlapping_actors";
  if (similar_runtime.value) query_string += "&similar_runtime";

  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies/${movie_id.value}/similar/?amount=${amount.value}${query_string}`, {
      credentials: "same-origin"
    })
  .then(async (response) => {
      similar_response_code.value = response.status;
      if (response.status >= 400) {
          console.log("Failed to fetch: status", response.status);
          return;
      }
      response.json().then((response_json: SimilarMoviesResponse) => {
        similar_movies_data.value = response_json["result"];

        const reference_movie_json = response_json["reference_movie"];
        reference_movie_data.value = {
          title: reference_movie_json["title"],
          id: reference_movie_json["id"],
          runtime: reference_movie_json["runtime"] === null ? undefined : reference_movie_json["runtime"],
          genre_ids: reference_movie_json["genres"].map((genre: { id: number }) => {
            return genre.id;
          })
        };
      });
  })
  .catch((e) => {
      console.log("Error during fetch: ", e);
      return;
  })

}

/** Fetch the primary movie info for X movies that are missing their runtime, to update their runtime */
async function onClickRuntime() {
  if (is_updating_runtime.value) return;

  is_updating_runtime.value = true;
  let updates_remaining: number = runtime_fetch_amount.value;

  for (let index = 0; updates_remaining > 0 && index < similar_movies_data.value.length; index += 1) {
    const movie: Movie = similar_movies_data.value[index];

    if (movie.runtime !== undefined) continue;

    await fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies/${movie.id}`, {
        credentials: "same-origin"
      })
    .then(async (response) => {
        response.json().then((response_json: MoviesResponse) => {
          movie.runtime = response_json["result"].runtime;
        });
        updates_remaining -= 1;
    })
    .catch((e) => {
        console.log("Error during fetch: ", e);
        return;
    })
  }

  is_updating_runtime.value = false;
}
</script>

<template>
  <main>
    <!-- View header -->
    <MainContentHeader title="Similar"/>  

    <div>
      <label for="input-similar-nav" style="padding-right: 1rem;">Selected movie is {{ movie_id }}. Select new movie</label>
      <input style="margin-right: 1rem; min-width: 100px; max-width: 200px;" id="input-similar-nav" type="number" min="0" v-model="movie_id"/>
    </div>

    <!-- View content -->
    <!-- Invalid movie id, fallthrough content -->
    <div v-if="movie_id === undefined">
      <p>Invalid movie id: {{ $route.params.mov_id }}</p>
    </div>
    <!-- Valid movie id, happy day content -->
    <div v-else>
      <!-- Select amount of similar movies to fetch -->
      <form @submit.prevent=""
        style="margin-top: 1rem; margin-bottom: 1rem;"
      >
        <label for="input-similar-amount" style="padding-right: 1rem;">First X similar movies</label>
        <input style="margin-right: 1rem; min-width: 100px; max-width: 200px;" id="input-similar-amount" type="number" min="0" v-model="amount"/>
        <button id="button-similar-amount" @click="onClick">Get similar {{ amount }}</button>
      </form>

      <!-- Select the similarity keywords to modify the TMDB query -->
      <div style="margin-bottom: 1rem;">
        <input id="input-matching-genres" type="checkbox" v-model="matching_genres">
        <label for="input-matching-genres" style="padding-left: 1rem;"
          title="Every fetched movie must have exactly the same genres as the reference movie, no less and no more"
        >Require exactly matching genres</label>
        <br>

        <input id="input-overlapping-actors" type="checkbox" v-model="overlapping_actors">
        <label for="input-overlapping-actors" style="padding-left: 1rem;"
          title="Every fetched movie must have at least the first two actors in the reference movie's cast as part of their cast as well"
        >Require overlapping actors</label>
        <br>

        <input id="input-similar-runtime" type="checkbox" v-model="similar_runtime">
        <label for="input-similar-runtime" style="padding-left: 1rem;"
          title="Every fetched movie must be similar in runtime compared to the reference movie"
        >Require similar runtime</label>
      </div>

      <!-- Display the referenced movie -->
      <h4>Reference Movie</h4>
      <div class="movie-card-reference">
        <Movie404Card v-if="similar_response_code === 404" :movie-id="movie_id"/>
        <MoviePlacedolderCard v-else-if="reference_movie_data === undefined"/>
        <MovieCard v-else :movie="reference_movie_data"/>
      </div>

      <!-- Display the fetched movies -->
      <h4>
        Similar Movies
        <!-- Fetch missing runtime values -->
        <HourglassLogo :class="runtime_updater_class"
          :title="`Fetch the next ${runtime_fetch_amount} missing runtime values`"
          @click="onClickRuntime"
        />
      </h4>
      <p v-if="similar_movies_data.length == 0" id="results-popularX">No results yet</p>
      <MovieGrid v-else :movies-data="similar_movies_data"/>
    </div>
  </main>
</template>

<style scoped>
.movie-card-reference {
  margin-bottom: 1rem;
}


.runtime-updater-running {
  animation-name: spin;
  animation-duration: 5000ms;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}

@keyframes spin {
  from {
      transform:rotate(0deg);
  }
  
  to {
      transform:rotate(360deg);
  }
}

@media (hover: hover) {
  .runtime-updater-idle:hover {
    cursor: pointer;
  }
}
</style>
<script setup lang="ts">
import { computed } from "vue";
import { ref, type Ref } from "vue";
import type { Movie } from "@/code/interfaces"

import MovieCard from './MovieCard.vue';
import ThumbsUpLogo from './logos/ThumbsUpLogo.vue';
import TrashcanLogo from "./logos/TrashcanLogo.vue";

const props = defineProps<{
    /** The movie to display */
    movie: Movie;
}>();

const emit = defineEmits<{
    /** The like action has been triggered */
    (e: "like", movie: Movie): void;
    /** The delete action has been triggered */
    (e: "delete", movie: Movie): void;
}>();

/** Whether a 'like' call is in progress */
const is_liking: Ref<boolean> = ref(false);
const class_like = computed(() => {
  return is_liking.value ? "" : "icon-like"
});

/** Whether a 'delete' call is in progress */
const is_deleting: Ref<boolean> = ref(false);
  const class_delete = computed(() => {
  return is_deleting.value ? "" : "icon-delete"
});

/** The color of the like icon, based on movie like status */
const like_icon_fill = computed(() => {
    return (props.movie.liked !== undefined && props.movie.liked === true) ? "fill: green;" : "";
})

/** The like/unlike functionality event trigger */
async function onClickLike() {
  if (props.movie.liked === undefined) return;
  if (is_liking.value) return;

  is_liking.value = true;
  const method: string = props.movie.liked ? "DELETE" : "PUT";
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/likes/${props.movie.id}`, {
    method: method,
    credentials: "same-origin"
  })
  .then(async (response) => {
    if (response.status >= 400) {
      is_liking.value = false;
      return;
    }

    emit("like", props.movie);
    is_liking.value = false;
  }).catch(() => {
    is_liking.value = false;
  });
}

/** The delete functionality event trigger */
async function onClickDelete() {
  if (is_deleting.value) return;

  is_deleting.value = true;
  fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/movies/${props.movie.id}`, {
    method: "DELETE",
    credentials: "same-origin"
  })
  .then(async (response) => {
    if (response.status >= 400) {
      is_deleting.value = false;
      return;
    }

    emit("delete", props.movie);
    is_deleting.value = false;
  })
  .catch(() => {
    is_deleting.value = false;
  });
}
</script>

<template>
  <MovieCard :movie="movie">
    <template v-slot:middle>
        <!-- Icons to provide extra functionality -->
        <div class="movie-card-icons">
        <ThumbsUpLogo :class="class_like"
          :style="like_icon_fill"
          @click="onClickLike"
        />
        <TrashcanLogo style="margin-left: 1rem;" :class="class_delete"
          @click="onClickDelete"
        />
        </div>
    </template>
  </MovieCard>
</template>

<style scoped>
.movie-card-icons {
  margin-left: 1rem;
  margin-right: 1rem;
}

@media (hover: hover) {
    .icon-delete:hover {
        fill: red;
        cursor: pointer;
    }

    .icon-like:hover {
        cursor: pointer;
    }
}
</style>
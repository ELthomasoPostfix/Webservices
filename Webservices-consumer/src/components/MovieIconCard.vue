<script setup lang="ts">
import { computed } from "vue";
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

/** The color of the like icon, based on movie like status */
const like_icon_fill = computed(() => {
    return (props.movie.liked !== undefined && props.movie.liked === true) ? "fill: green;" : "";
})

/** The like/unlike functionality event trigger */
async function onClickLike() {
  if (props.movie.liked === undefined) return;
  emit("like", props.movie);
}

/** The delete functionality event trigger */
async function onClickDelete() {
  emit("delete", props.movie);
}
</script>

<template>
  <MovieCard :movie="movie">
    <template v-slot:middle>
        <!-- Icons to provide extra functionality -->
        <div class="movie-card-icons">
        <ThumbsUpLogo class="icon-like"
          :style="like_icon_fill"
          @click="onClickLike"
        />
        <TrashcanLogo class="icon-delete"
          @click="onClickDelete"
        />
        </div>
    </template>
  </MovieCard>
</template>

<style scoped>
.icon-delete {
    margin-left: 1rem;
}

.movie-card-icons {
  margin-left: 1rem;
  margin-right: 1rem;
}

@media (hover: hover) {
    .icon-delete:hover {
        fill: red;
        cursor: pointer;
    }

    .icon-like {
        cursor: pointer;
    }
}
</style>
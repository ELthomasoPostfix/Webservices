<script setup lang="ts">
import { computed } from "vue";

import PlaceholderRect from './PlaceholderRect.vue';

const props = defineProps<{
  /**  */
  width: Number;
}>();

const width_style = computed(() => {
  return `max-width: ${props.width}px`;
})
</script>

<template>
  <div class="movie-card" :style="width_style">
    <!-- Card header -->
    <h6 class="movie-card-title">
      <PlaceholderRect :width="70" :height="20"/>
    </h6>
    <!-- Card content -->
    <div class="movie-card-body" style="margin-left: 1rem;">
      <PlaceholderRect :width="30" :height="10"/>
      <PlaceholderRect style="margin-left: 1rem;" :width="10" :height="10"/>
      <br>
      <PlaceholderRect :width="45" :height="10"/>
    </div>
  </div>
</template>

<style scoped>
.movie-card {
  border: 2px solid;
  border-radius: 10px;
  display: grid;
}

.movie-card-title {
  margin: 10px;
}

.movie-card-body {
  margin-bottom: 5px;
}
</style>
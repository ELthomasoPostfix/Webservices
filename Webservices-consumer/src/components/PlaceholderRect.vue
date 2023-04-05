<script setup lang="ts">
defineProps<{
    /** The width of the placeholder rect as a percentage,
     * e.g. width="30" will take up 30% of available width
     */
    width: number;
    /** The height of the placeholder rect in pixels,
     * e.g. height="30" will be 30px high
     */
     height: number;
}>();
</script>

<template>
  <svg :width="`${width}%`" :height="`${height}px`" class="placeholder-rect">
    <rect width="100%" height="100%" />
  </svg>
</template>

<style scoped>
.placeholder-rect {
  fill: rgb(179, 173, 173);
  stroke-width: 3;
  border-radius: 1rem;

  margin: 0;
}
</style>
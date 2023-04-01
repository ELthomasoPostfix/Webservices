<script setup lang="ts">
defineProps<{
    /** The movie's title */
    title: String
}>();
</script>

<template>
    <div class="movie-card">
        <h6 class="movie-card-title">
            {{ title }}
        </h6>
    </div>
</template>

<style scoped>
.movie-card {
  border: 2px solid;
  border-radius: 10px;
  display: grid;
}

.movie-card-title {
  padding: 20px;
}
</style>
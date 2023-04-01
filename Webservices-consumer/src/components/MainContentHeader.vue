<script setup lang="ts">
/** A header to enforce uniformity between all views. */
defineProps<{
    /** The title of the content header */
    title: String,
}>();
</script>

<template>
    <h1>{{ title }}</h1>
    <hr>
</template>

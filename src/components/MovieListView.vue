<template>
  <div class="container mt-5">
    <h2 class="mb-4">Movie List</h2>
    <div class="row">
      <div class="col-md-6 col-lg-4 mb-4" v-for="movie in movies" :key="movie.id">
        <div class="card shadow-sm rounded">
          <img
            v-if="movie.poster"
            :src="getPosterUrl(movie.poster)"
            class="card-img-top"
            :alt="movie.title"
          />
          <div class="card-body">
            <h5 class="card-title" v-html="movie.title"></h5>
            <p class="card-text">{{ movie.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const movies = ref([]);

onMounted(async () => {
  try {
    const response = await fetch('/api/v1/movies');
    movies.value = await response.json();
  } catch (error) {
    console.error('Failed to load movies:', error);
  }
});

const getPosterUrl = (filename) => {
  return `/api/v1/posters/${filename}`;
};
</script>

<style scoped>
.card-img-top {
  max-height: 300px;
  object-fit: cover;
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
}

.card-text {
  font-size: 0.95rem;
}

h2 {
  font-size: 2.25rem;
  font-weight: bold;
}
</style>
<template>
  <div class="container mt-5">
    <!-- Alert Message -->
    <div
      v-if="successMessage"
      :class="[success ? 'alert alert-success' : 'alert alert-danger']"
      role="alert"
    >
      <div class="fs-6" v-html="successMessage"></div>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie">
      <!-- Movie Title -->
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input
          type="text"
          v-model="title"
          name="title"
          class="form-control"
          placeholder="Enter movie title"
        />
      </div>

      <!-- Description -->
      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          v-model="description"
          name="description"
          class="form-control"
          placeholder="Enter movie description"
        ></textarea>
      </div>

      <!-- Poster Upload -->
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Poster</label>
        <input
          type="file"
          @change="updatePoster"
          class="form-control"
          id="poster"
        />
        <small v-if="poster" class="text-muted mt-1 d-block">
          Selected file: {{ poster.name }}
        </small>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const title = ref('');
const description = ref('');
const poster = ref(null);
const csrf_token = ref('');
const successMessage = ref('');
const success = ref(false);

// Fetch CSRF token when component is mounted
onMounted(() => {
  getCsrfToken();
});

const getCsrfToken = () => {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      if (data.csrf_token) {
        csrf_token.value = data.csrf_token;
      }
    })
    .catch((error) => {
      console.error('CSRF token fetch failed:', error);
    });
};

const updatePoster = (event) => {
  poster.value = event.target.files[0];
};

const saveMovie = () => {
  const form_data = new FormData();
  form_data.append('title', title.value);
  form_data.append('description', description.value);
  form_data.append('poster', poster.value);

  fetch('/api/v1/movies', {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then((response) => {
      success.value = response.ok;
      return response.json();
    })
    .then((data) => {
      if (success.value) {
        successMessage.value = 'Movie added successfully.';
        title.value = '';
        description.value = '';
        poster.value = null;
      } else {
        if (data.errors) {
          successMessage.value = '';
          for (let i = 0; i < data.errors.length; i++) {
            successMessage.value += `<li>${data.errors[i]}</li>`;
          }
        } else {
          successMessage.value = 'Failed to add movie.';
        }
      }
    })
    .catch((error) => {
      success.value = false;
      successMessage.value = 'An unexpected error occurred.';
      console.error('Submit error:', error);
    });
};
</script>

<style scoped>
/* Optional customization for file input */
input[type="file"] {
  padding: 8px;
  background-color: #f8f9fa;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 0.95rem;
}
</style>
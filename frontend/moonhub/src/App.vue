<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="full-size">
    <header>
      <nav>
        <RouterLink to="/">Inventory</RouterLink>
        <RouterLink to="/add">Add Product</RouterLink>
      </nav>
    </header>

    <RouterView />
  </div>
</template>

<style scoped>
.full-size {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}

#app {
  height: inherit;
  width: inherit;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  height: 60px; /* Adjusted for a more suitable size in the header */
}

nav {
  display: flex;
  gap: 1rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #333;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

nav a:hover {
  background-color: #e7e7e7;
}

@media (min-width: 1024px) {
  nav {
    gap: 2rem;
  }
}
</style>

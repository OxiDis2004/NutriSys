<script setup lang="ts">
import { RouterLink } from 'vue-router'

import { ref } from 'vue'
import StartView from '@/views/StartView.vue'
import RecommendedView from '@/views/RecommendedView.vue'

const isOpen = ref(false)

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <header>
    <nav>
      <!-- Mobile toggle button -->
      <button class="menu-toggle" @click="toggleMenu">☰ Menu</button>

      <!-- Links -->
      <div :class="['nav-links', { open: isOpen }]">
        <RouterLink to="/#start">Start</RouterLink>
        <RouterLink to="/#recommendation">Recommendation</RouterLink>
        <RouterLink to="/#food-statistic">Food statistic</RouterLink>
        <RouterLink to="/#water-statistic">Water statistic</RouterLink>
        <RouterLink to="/#food-history">Food history</RouterLink>
        <RouterLink to="/#settings">Settings</RouterLink>
      </div>
    </nav>
  </header>

  <main>
    <StartView />
    <RecommendedView />
  </main>
</template>

<style scoped>
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

main {
  width: 1120px;
  top: 0;
  left: 0;
}

nav {
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;
}

/* Toggle button (hidden on desktop) */
.menu-toggle {
  display: none;
  width: 100%;
  padding: 1rem;
  font-size: 1.2rem;
  background: none;
  border: none;
  cursor: pointer;
}

/* Links container */
.nav-links {
  display: flex;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

/* Desktop */
@media (min-width: 777px) {
  .nav-links {
    flex-direction: row;
    justify-content: center;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}

/* Mobile */
@media (max-width: 776px) {
  .menu-toggle {
    display: block;
    color: var(--color-text);
  }

  .nav-links {
    display: none;
    flex-direction: column;
    width: 100%;
    text-align: center;
    background: var(--color-background);
  }

  .nav-links.open {
    display: flex;
  }

  .nav-links a {
    margin: 0;
    padding: 1.2rem;
    border-top: 1px solid var(--color-border);
  }

  main {
    width: 100%;
    position: fixed;
    padding-top: 60px;
  }
}
</style>

<template>
  <a-layout class="layout">
    <a-layout-header class="layout__header">
      <h2>Ultra Chat</h2>
    </a-layout-header>
    <a-layout-content class="layout__content">
      <div class="layout__content-container">
        <AppChat />
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import AppChat from '@/components/AppChat.vue'
</script>

<style lang="scss">
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;

  &__header {
    background-color: #0057b8 !important;
    text-align: center;

    h2 {
      color: #fff;
    }
  }

  &__content {
    background-color: #dddedf;
    flex-grow: 1;
    height: 100%;
    padding: 1rem;

    &-container {
      overflow: hidden;
      border-radius: 1rem;
      background-color: #fff;
      height: 100%;
    }
  }
}
</style>

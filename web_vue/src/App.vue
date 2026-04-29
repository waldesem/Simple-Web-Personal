<script setup lang="ts">
</script>

<template>
  <UApp>
    <LayoutView>
      <router-view v-slot="{ Component }">
        <Transition name="fade">
          <KeepAlive include="IndexView" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </router-view>
    </LayoutView>
  </UApp>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

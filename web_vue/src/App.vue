<script setup lang="ts"></script>

<template>
  <UApp>
    <router-view v-slot="{ Component }">
      <Transition name="fade">
        <LayoutView>
          <KeepAlive include="IndexView" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </LayoutView>
      </Transition>
    </router-view>
  </UApp>
</template>

<style>
.fade-enter-from {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}
.fade-enter-active {
  transition: opacity 0.3s ease;
}

.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active {
  transition: opacity 0.3s ease;
}
</style>

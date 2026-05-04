<script setup lang="ts"></script>

<template>
  <UApp>
    <router-view v-slot="{ Component }">
      <Transition mode="out-in" name="fade">
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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

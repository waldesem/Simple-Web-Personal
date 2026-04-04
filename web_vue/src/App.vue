<template>
  <UApp>
    <Transition name="fade">
      <router-view v-slot="{ Component }">
        <KeepAlive include="IndexView" :max="1">
          <component :is="Component" />
        </KeepAlive>
      </router-view>
    </Transition>
  </UApp>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

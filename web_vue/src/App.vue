<template>
  <UApp>
    <template>
      <Transition name="fade">
        <div>
          <router-view />
        </div>
      </Transition>
    </template>
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

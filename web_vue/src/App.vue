<template>
  <UApp>
    <router-view v-slot="{ Component }">
      <LayoutView>
        <Transition mode="out-in" name="fade">
          <KeepAlive include="IndexView" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </LayoutView>
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

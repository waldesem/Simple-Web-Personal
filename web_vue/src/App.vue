<template>
  <NUApp>
    <RouterView v-slot="{ Component }">
      <LayoutView>
        <Transition mode="out-in" name="fade">
          <KeepAlive include="HomePage" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </LayoutView>
    </RouterView>
  </NUApp>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

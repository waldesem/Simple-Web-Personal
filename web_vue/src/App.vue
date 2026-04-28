<template>
  <UApp>
    <UPage>
      <UHeader v-once to="/">
        <template #title>
          <div class="inline-flex items-center text-xl font-bold space-x-1">
            <div class="text-blue-600">КАДРОВАЯ</div>
            <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
          </div>
        </template>
      </UHeader>
      <UMain class="pt-16 pb-4">
        <router-view v-slot="{ Component }">
          <Transition name="fade">
            <KeepAlive include="IndexView" :max="1">
              <component :is="Component" />
            </KeepAlive>
          </Transition>
        </router-view>
      </UMain>
      <UFooter v-once />
    </UPage>
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

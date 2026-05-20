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

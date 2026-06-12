<template>
  <UApp>
    <RouterView v-slot="{ Component }">
      <LayoutView>
        <Transition mode="out-in" name="fade">
          <KeepAlive include="HomePage" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </LayoutView>
    </RouterView>
  </UApp>
</template>

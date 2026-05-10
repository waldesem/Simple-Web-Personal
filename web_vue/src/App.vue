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
/* Начальное состояние при появлении */
.fade-enter-from {
  opacity: 0;
}
/* Конечное состояние при появлении */
.fade-enter-to {
  opacity: 1;
}
/* Промежуточный класс для самого перехода */
.fade-enter-active {
  transition: opacity 0.3s ease;
}

/* Начальное состояние при исчезновении */
.fade-leave-from {
  opacity: 1;
}
/* Конечное состояние при исчезновении */
.fade-leave-to {
  opacity: 0;
}
/* Промежуточный класс для исчезновения */
.fade-leave-active {
  transition: opacity 0.3s ease;
}
</style>

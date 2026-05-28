<script setup lang="ts">
// import ky from "ky";
// import { watch } from "vue";
// import { useAsyncState, useDocumentVisibility } from "@vueuse/core";
import { session } from "@/state";
// import type { Session } from "@/types";

// const visibility = useDocumentVisibility();

// const { execute } = useAsyncState<Session>(
//   async () => await ky.get("/routes/session").json(),
//   {} as Session,
//   {
//     onSuccess(data) {
//       session.value = data;
//     },
//   }
// );

// watch(visibility, async () => {
//   if (visibility.value === "visible") await execute();
// });
</script>

<template>
  <UPage>
    <UHeader v-once to="/">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-blue-600">КАДРОВАЯ</div>
          <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
      <template #default>
        <UNavigationMenu
          :items="[
            {
              label: 'Пользователи',
              icon: 'i-lucide-users',
              to: '/users',
            },
          ]"
          variant="link"
        />
      </template>
      <template #right>
        <UAvatar :alt="session?.fullname ?? 'БКБ'" size="md" />
      </template>
    </UHeader>
    <UMain>
      <slot />
    </UMain>
    <UFooter v-once />
  </UPage>
</template>

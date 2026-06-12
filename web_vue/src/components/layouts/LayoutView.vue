<script setup lang="ts">
import ky from "ky";
import { useAsyncState } from "@vueuse/core";
import { session } from "@/state";
import type { Session } from "@/types";

const { state } = useAsyncState<Session>(
  async () => await ky.get("/api/auth/session").json(),
  {} as Session,
  {
    onSuccess(data) {
      session.value = data;
    },
  },
);
</script>

<template>
  <UPage>
    <UHeader to="/">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-blue-600">КАДРОВАЯ</div>
          <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
      <template #default>
        <ULink to="/users" :replace="false" class="font-bold">
          Пользователи
        </ULink>
      </template>
      <template #right>
        <UAvatar
          v-if="state.fullname"
          :alt="state.fullname"
          :chip="{ inset: true, color: 'success' }"
          size="md"
        />
        <UAvatar
          v-else
          icon="i-mi-ban"
          color="error"
          size="md"
        />
      </template>
    </UHeader>
    <UMain>
      <slot />
    </UMain>
    <UFooter v-once />
  </UPage>
</template>

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
        <div class="inline-flex items-center text-xl text-gray-600 space-x-1">
          <div>КАДРОВАЯ</div>
          <div>БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
      <template #right>
        <UAvatar
          v-if="state.fullname"
          :alt="state.fullname"
          :chip="{ inset: true, color: 'warning' }"
          size="md"
        />
        <UAvatar v-else icon="i-mi-ban" color="error" size="md" />
      </template>
    </UHeader>
    <UMain>
      <slot />
    </UMain>
    <UFooter v-once />
  </UPage>
</template>

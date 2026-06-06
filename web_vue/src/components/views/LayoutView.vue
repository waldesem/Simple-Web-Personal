<script setup lang="ts">
import ky from "ky";
import { useAsyncState } from "@vueuse/core";
import { useRouter } from "vue-router";
import { session } from "@/state";
import type { Session } from "@/types";

const { state } = useAsyncState<Session>(
  async () => await ky.get("/api/auth/session").json(),
  {} as Session,
  {
    onSuccess(data) {
      session.value = data;
    },
    onError() {
      const router = useRouter();
      router.replace({
        name: "error",
        params: {
          statusCode: 400,
          statusMessage: "Ошибка авторизации, обратитесь к администратору",
        },
      });
    },
  },
);
</script>

<template>
  <NUPage>
    <NUHeader to="/">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-blue-600">КАДРОВАЯ</div>
          <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
      <template #default>
        <NULink to="/users" :replace="false" class="font-bold">
          Пользователи
        </NULink>
      </template>
      <template #right>
        <NUAvatar :alt="state.fullname ?? '?'" size="md" />
      </template>
    </NUHeader>
    <NUMain>
      <slot />
    </NUMain>
    <NUFooter v-once />
  </NUPage>
</template>

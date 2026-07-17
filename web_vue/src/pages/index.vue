<script setup lang="ts">
import { defineAsyncComponent, inject, onMounted } from "vue";
import { useRouter } from "vue-router";
import { KyInstance } from "ky";
import { session } from "@/state";
import type { Session } from "@/types";

const BrandHead = defineAsyncComponent(
  () => import("@/components/content/BrandHead.vue"),
);

const router = useRouter();

const api = inject("api") as KyInstance;

onMounted(async () => {
  try {
    session.value = await api.get("auth/session").json<Session>();
    router.replace("/persons");
  } catch (error) {
    console.error(error);
    router.replace("/login");
  }
});
</script>

<template>
  <div>
    <UPageBody class="flex flex-col items-center justify-center h-screen">
      <BrandHead :animated="true" size="text-7xl" />
    </UPageBody>
  </div>
</template>

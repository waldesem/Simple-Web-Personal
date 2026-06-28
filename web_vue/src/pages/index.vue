<script setup lang="ts">
import { inject, onMounted } from "vue";
import { useRouter } from "vue-router";
import { KyInstance } from "ky";
import { session } from "@/state";
import type { Session } from "@/types";

const router = useRouter();

const api = inject("api") as KyInstance;

onMounted(async () => {
  try {
    session.value = await api.get("/api/auth/session").json<Session>();
    router.push("/persons");
  } catch (error) {
    console.error(error);
    router.replace("/login");
  }
});
</script>

<template>
  <div>
    <UContainer>
      <UEmpty title="Redirecting..." description="Please wait..." />
    </UContainer>
  </div>
</template>

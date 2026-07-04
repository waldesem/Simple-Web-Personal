<script setup lang="ts">
import { inject, onBeforeMount, ref } from "vue";
import { useRouter } from "vue-router";
import { KyInstance } from "ky";
import { session } from "@/state";
import type { Session } from "@/types";

const router = useRouter();

const api = inject("api") as KyInstance;

const value = ref(null);

onBeforeMount(async () => {
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
    <UPageCard class="w-full max-w-md m-auto my-[20vh]">
      <UEmpty title="Redirecting..." description="Please wait...">
        <template #body>
          <UProgress animation="swing" v-model="value" />
        </template>
      </UEmpty>
    </UPageCard>
  </div>
</template>

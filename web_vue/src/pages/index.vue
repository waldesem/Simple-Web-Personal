<script setup lang="ts">
import { useRouter } from "vue-router";

definePage({ meta: { layout: "UserLayout" } });

const router = useRouter();

router.push("/persons");
</script>

<template>
  <div>
    <UContainer>
      <UEmpty title="Redirecting..." description="Please wait..." />
    </UContainer>
  </div>
</template>

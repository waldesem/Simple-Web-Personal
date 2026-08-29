<script setup lang="ts">
import { inject, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { KyInstance } from 'ky';
import { session } from '@/state';

const router = useRouter();

const api = inject('api') as KyInstance;

onMounted(async () => {
  try {
    session.value = await api.get('auth/session').json();
    router.replace('/persons');
  } catch (e) {
    console.error(e);
    router.replace('/login');
  }
});
</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <UProgress class="w-1/3" color="error" animation="swing" />
  </div>
</template>

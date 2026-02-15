<script setup lang="ts">
import { useRoute } from "vue-router";
import { ofetch } from "ofetch";
import type { Person } from "@/types";
import { onBeforeMount, computed, provide, ref } from "vue";

// Получаем данные id кандидата из URL
const route = useRoute();

const candId = computed(() => route.params.id as string);
provide("candId", candId);

const edit = ref(false);
provide("edit", edit);

const data = ref({} as Person);
const status = ref("");

// Определяем функцию для получения данных из API
onBeforeMount(() => getPerson());

async function getPerson() {
  data.value = await ofetch<Person>("/routes/persons/" + candId.value);
}
provide("person", data);
</script>

<template>
  <LayoutView>
    <UContainer>
      <UPageHeader
        :title="`${data.surname} ${data.firstname} ${data.patronymic ?? ''}`"
      >
        <template #links>
          <UButton
            variant="outline"
            :loading="status === 'pending'"
            :color="edit ? 'error' : 'primary'"
            :label="edit ? 'Откл.Редакт.' : 'Вкл.Редакт.'"
            @click="edit = !edit"
          />
        </template>
      </UPageHeader>
      <TabsView @update="getPerson" />
    </UContainer>
  </LayoutView>
</template>

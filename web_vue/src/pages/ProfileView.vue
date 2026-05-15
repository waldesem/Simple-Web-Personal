<script setup lang="ts">
import { computed, onMounted, shallowRef } from "vue";
import { useRoute } from "vue-router";
import { ofetch } from "ofetch";
import { flag } from "@/utils";
import type { Items, Person } from "@/types";

// Получаем данные id кандидата из URL
const candId = computed(() => useRoute().params.id as string);

const data = shallowRef({} as Person);

onMounted(() => getPerson());

// Определяем функцию для получения данных из API
async function getPerson() {
  data.value = await ofetch<Person>("/routes/persons/" + candId.value);
}

const fullname = computed(() => {
  return `${data.value.surname ?? ""} ${data.value.firstname ?? ""} ${
    data.value.patronymic ?? ""
  }`;
});

const anketa = { label: "Анкета", slot: "anketa" as const };

const subjects = [
  { label: "Проверки", slot: "checks" as const },
  { label: "Полиграф", slot: "poligrafs" as const },
  { label: "Расследования", slot: "investigations" as const },
  { label: "Запросы", slot: "inquiries" as const },
] as { label: string; slot: keyof Items }[];

// Определяем массив элементов аккордеона
const accordion = [
  { label: "Должности", slot: "staffs" as const },
  { label: "Образование", slot: "educations" as const },
  { label: "Места работы", slot: "workplaces" as const },
  { label: "Документы", slot: "documents" as const },
  { label: "Адреса", slot: "addresses" as const },
  { label: "Контакты", slot: "contacts" as const },
  { label: "Изменения имени", slot: "previous" as const },
  { label: "Аффилированность", slot: "affilations" as const },
] as { label: string; slot: keyof Items }[];
</script>

<template>
  <UContainer>
    <UPageHeader :title="fullname">
      <template #links>
        <UButton
          :icon="flag ? 'i-lucide-pencil' : 'i-lucide-pencil-off'"
          :color="flag ? 'success' : 'error'"
          :title="flag ? 'Откл.Редакт.' : 'Вкл.Редакт.'"
          @click="flag = !flag"
        />
      </template>
    </UPageHeader>

    <UTabs
      :items="[anketa, ...subjects]"
      :unmount-on-hide="false"
      variant="pill"
      class="mt-4"
    >
      <!-- Слот вкладки для отображения анкеты -->
      <template #anketa>
        <div class="mt-4">
          <PersonView :person="data" @update="getPerson" />
        </div>
        <USeparator />
        <!-- Aккордеон с данными staffs, educations и т.д. -->
        <UAccordion :items="accordion" :unmount-on-hide="false">
          <template
            v-for="accord in accordion"
            #[accord.slot]
            :key="accord.slot"
          >
            <ItemView
              :view="accord.slot as keyof Items"
              :title="accord.label"
              :cand-id="candId"
            />
          </template>
        </UAccordion>
      </template>

      <!-- Вкладки проверки, полиграф и др. -->
      <template v-for="tab in subjects" #[tab.slot] :key="tab.slot">
        <div class="mt-2">
          <ItemView :view="tab.slot" :title="tab.label" :cand-id="candId" />
        </div>
      </template>
    </UTabs>
  </UContainer>
</template>

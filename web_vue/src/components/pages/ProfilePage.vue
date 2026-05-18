<script setup lang="ts">
import { computed, onMounted, ref, shallowRef } from "vue";
import { useRoute } from "vue-router";
import { ofetch } from "ofetch";
import { divsPerson } from "@/schema/persona";
import type { Items, Person } from "@/types";

// Получаем данные id кандидата из URL
const candId = computed(() => useRoute().params.id as string);

const data = shallowRef({} as Person);
const flag = ref(false);
const loading = ref(false); // ← триггер для анимации

onMounted(() => getPerson());

// Определяем функцию для получения данных из API
async function getPerson() {
  loading.value = true;
  data.value = await ofetch<Person>("/routes/persons/" + candId.value);
  loading.value = false;
}

const fullname = computed(
  () =>
    `${data.value.surname ?? ""} ${data.value.firstname ?? ""} ${
      data.value.patronymic ?? ""
    }`,
);

const anketa = { label: "Анкета", slot: "anketa" as const };

const tabs = [
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
  <UContainer class="pt-16">
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

    <UPageBody>
      <UTabs
        :items="[anketa, ...tabs]"
        :unmount-on-hide="false"
        variant="pill"
        class="mt-4"
      >
        <!-- Слот вкладки для отображения анкеты -->
        <template #anketa>
          <SkeletDivs v-if="loading && !data" :rows="divsPerson.length" />
          <PersonView
            v-else
            :class="{ 'animate-pulse': loading }"
            :person="data"
            :flag="flag"
            @update="getPerson"
          />
          <USeparator />

          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <UAccordion :items="accordion" :unmount-on-hide="false">
            <template
              v-for="accord in accordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ItemView
                :flag="flag"
                :view="accord.slot"
                :title="accord.label"
                :cand-id="candId"
              />
            </template>
          </UAccordion>
        </template>

        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in tabs" #[tab.slot] :key="tab.slot">
          <div class="mt-2">
            <ItemView
              :flag="flag"
              :view="tab.slot"
              :title="tab.label"
              :cand-id="candId"
            />
          </div>
        </template>
      </UTabs>
    </UPageBody>
  </UContainer>
</template>

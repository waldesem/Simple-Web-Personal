<script setup lang="ts">
import { computed, onMounted, ref, shallowRef } from "vue";
import { useRoute } from "vue-router";
import { ofetch } from "ofetch";
import { itemsFields } from "@/schema/items";
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

const anketa = { label: "Анкета", slot: "person" as keyof Items };

const tabs = [
  { label: "Проверки", slot: "checks" },
  { label: "Полиграф", slot: "poligrafs" },
  { label: "Расследования", slot: "investigations" },
  { label: "Запросы", slot: "inquiries" },
] as { label: string; slot: keyof Items }[];

// Определяем массив элементов аккордеона
const accordion = [
  { label: "Должности", slot: "staffs" },
  { label: "Образование", slot: "educations" },
  { label: "Места работы", slot: "workplaces" },
  { label: "Документы", slot: "documents" },
  { label: "Адреса", slot: "addresses" },
  { label: "Контакты", slot: "contacts" },
  { label: "Изменения имени", slot: "previous" },
  { label: "Аффилированность", slot: "affilations" },
] as { label: string; slot: keyof Items }[];
</script>

<template>
  <UContainer class="pt-16">
    <UPageHeader :title="fullname">
      <template #links>
        <UButton
          :color="flag ? 'success' : 'error'"
          :icon="flag ? 'i-lucide-pencil' : 'i-lucide-pencil-off'"
          :title="flag ? 'Откл.Редакт.' : 'Вкл.Редакт.'"
          @click="flag = !flag"
        />
      </template>
    </UPageHeader>

    <UPageBody>
      <UTabs :items="[anketa, ...tabs]" :unmount-on-hide="false" variant="pill">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <SkeletDivs v-if="loading" :rows="itemsFields.person.length" />
          <PersonView v-else :flag="flag" :person="data" @update="getPerson" />

          <USeparator />

          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <UAccordion :items="accordion" :unmount-on-hide="false">
            <template
              v-for="accord in accordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ItemView
                :cand-id="candId"
                :flag="flag"
                :title="accord.label"
                :view="accord.slot"
              />
            </template>
          </UAccordion>
        </template>

        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in tabs" #[tab.slot] :key="tab.slot">
          <ItemView
            :cand-id="candId"
            :flag="flag"
            :title="tab.label"
            :view="tab.slot"
          />
        </template>
      </UTabs>
    </UPageBody>
  </UContainer>
</template>

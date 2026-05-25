<script setup lang="ts">
import ky from "ky";
import { ref, watch, shallowRef } from "vue";
import { refDebounced } from "@vueuse/core";
import { useRouter } from "vue-router";
import { tableCols } from "@/schema/elements";
import { itemsForms } from "@/schema/forms";
import type { Person } from "@/types";

const data = shallowRef([] as Person[]);
const modal = ref(false); // Состояние модального окна
const hasNext = ref(false); // Состояние наличия следующей страницы
const limit = ref(10); // Количество записей на странице
const loading = ref(false); // Состояние загрузки
const page = ref(0); // Страница таблицы
const search = ref(""); // Поисковый запрос
const updated = ref(""); // Время обновления

const debounced = refDebounced(search, 1000); // Дебаунс поиска

const router = useRouter();

watch([debounced, limit], async () => {
  if (page.value === 0) await getItem();
  else page.value = 0;
});

watch(
  page,
  async () => {
    await getItem();
    window.scrollTo({ top: 0, behavior: "smooth" });
  },
  { immediate: true },
);

async function getItem() {
  loading.value = true;
  const response = await ky
    .get<Person[]>("/routes/candidates", {
      searchParams: {
        limit: limit.value,
        page: page.value,
        search: debounced.value,
      },
    })
    .json();
  data.value = response.slice(0, limit.value);
  hasNext.value = response.length > limit.value;
  loading.value = false;
  updated.value = new Date().toLocaleTimeString();
}

// Обработчик результата загрузки данных
async function submitPerson(form: Person) {
  loading.value = true;
  modal.value = false;
  const resp = await ky.post("/routes/persons", {
    method: "POST",
    json: form,
  });
  loading.value = false;
  if (resp.status === 201) {
    const json = (await resp.json()) as { person_id: string };
    if (json?.person_id) {
      router.push({ name: "profile", params: { id: json.person_id } });
    } else {
      alert("Анкета уже существует!");
    }
  } else {
    alert("Невозможно выполнить действие!");
  }
}
</script>

<template>
  <UContainer>
    <UPageHeader title="КАНДИДАТЫ">
      <template #links>
        <!-- Модальное окно для добавления анкеты -->
        <UModal
          v-model:open="modal"
          description="Введите анкетные данные"
          title="Анкета"
        >
          <UButton
            icon="i-lucide-user-plus"
            size="xl"
            title="Добавить анкету"
            variant="ghost"
            :loading="loading"
            @click="modal = true"
          />
          <template #body>
            <FormDiv :fields="itemsForms.person" @submit="submitPerson" />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <!-- Строка поиска -->
    <UPageBody>
      <UInput
        id="search"
        icon="i-lucide-search"
        v-model.trim="search"
        :loading="loading"
        type="search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />

      <!-- Таблица с данными кандидатов -->
      <TableDiv
        :class="{ 'animate-pulse': loading }"
        :cols="tableCols"
        :data="data"
        @select="
          (row: Person) =>
            router.push({ name: 'profile', params: { id: row.id } })
        "
      />

      <UEmpty
        v-if="!data"
        size="sm"
        title="Данные отсутствуют"
        variant="naked"
      />

      <!-- Время последнего обновления -->
      <UButton
        icon="i-lucide-refresh-cw"
        :label="`Последнее обновление в: ${updated}`"
        :loading="loading"
        size="sm"
        title="Обновить"
        variant="ghost"
        @click="getItem"
      />

      <!-- Пагинация -->
      <div
        v-show="data"
        class="flex justify-center border-t border-default pt-8 pb-2"
      >
        <UButton
          class="me-2 rounded-full"
          :disabled="!page || loading"
          icon="i-lucide-arrow-left"
          title="Вперед"
          @click="page--"
        />
        <USelect
          v-model="limit"
          :items="[10, 50, 100]"
          title="Количество записей"
        />
        <UButton
          class="ms-2 rounded-full"
          :disabled="!hasNext || loading"
          icon="i-lucide-arrow-right"
          title="Назад"
          @click="page++"
        />
      </div>
    </UPageBody>
  </UContainer>
</template>

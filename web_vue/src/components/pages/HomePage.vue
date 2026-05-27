<script setup lang="ts">
import ky from "ky";
import { ref, watch } from "vue";
import { refDebounced, useAsyncState } from "@vueuse/core";
import { useRouter } from "vue-router";
import { tableCols } from "@/schema/elements";
import { itemsForms } from "@/schema/forms";
import type { Person } from "@/types";

const router = useRouter();

const hasNext = ref(false); // Состояние наличия следующей страницы
const limit = ref(10); // Количество записей на странице
const modal = ref(false); // Состояние модального окна
const page = ref(0); // Страница таблицы
const search = ref(""); // Поисковый запрос
const updated = ref(""); // Время обновления

const debounced = refDebounced(search, 1000); // Дебаунс поиска

const { execute, isLoading, state } = useAsyncState<Person[]>(
  async () =>
    await ky
      .get("/routes/candidates", {
        searchParams: {
          limit: limit.value,
          page: page.value,
          search: debounced.value,
        },
      })
      .json(),
  [],
  {
    onSuccess(data) {
      hasNext.value = data.length > limit.value;
      data = hasNext.value ? data.slice(0, limit.value) : data;
      updated.value = new Date().toLocaleTimeString();
    },
    onError(e) {
      alert(e);
    },
  },
);

watch([debounced, limit], async () => {
  if (page.value === 0) await execute();
  else page.value = 0;
});

watch(page, async () => {
  await execute();
});

// Обработчик результата загрузки данных
async function submit(form: Person) {
  modal.value = false;
  const resp = await ky.post("/routes/persons", {
    method: "POST",
    json: form,
  });
  if (resp.status === 201) {
    const { person_id } = (await resp.json()) as { person_id: string | null };
    if (person_id) router.push({ name: "profile", params: { id: person_id } });
    else alert("Анкета уже существует!");
  } else alert("Невозможно выполнить действие!");
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
            :loading="isLoading"
            @click="modal = true"
          />
          <template #body>
            <FormDiv :fields="itemsForms.person" @submit="submit" />
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
        :loading="isLoading"
        type="search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />

      <!-- Таблица с данными кандидатов -->
      <TableDiv
        :class="{ 'animate-pulse': isLoading }"
        :cols="tableCols"
        :data="state"
        @select="
          (row: Person) =>
            router.push({ name: 'profile', params: { id: row.id } })
        "
      />

      <UEmpty
        v-if="!state"
        icon="i-lucide-octagon-x"
        size="sm"
        title="Данные отсутствуют"
        variant="naked"
      />

      <!-- Время последнего обновления -->
      <UButton
        icon="i-lucide-refresh-cw"
        :label="`Последнее обновление в: ${updated}`"
        :loading="isLoading"
        size="sm"
        title="Обновить"
        variant="ghost"
        @click="execute()"
      />

      <!-- Пагинация -->
      <div
        v-show="state"
        class="flex justify-center border-t border-default pt-8 pb-2"
      >
        <UButton
          class="me-2 rounded-full"
          :disabled="!page || isLoading"
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
          :disabled="!hasNext || isLoading"
          icon="i-lucide-arrow-right"
          title="Назад"
          @click="page++"
        />
      </div>
    </UPageBody>
  </UContainer>
</template>

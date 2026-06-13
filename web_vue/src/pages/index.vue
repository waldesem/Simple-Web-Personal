<script setup lang="ts">
import ky from "ky";
import { shallowRef, watch } from "vue";
import { refDebounced, useAsyncState } from "@vueuse/core";
import { useRouter } from "vue-router";
import { personCols } from "@/schema/elems";
import { person as PersonForm } from "@/schema/forms";
import type { Person } from "@/types";

definePage({ meta: { layout: "UserLayout" } });

const router = useRouter();

const hasNext = shallowRef(false); // Состояние наличия следующей страницы
const limit = shallowRef(10); // Количество записей на странице
const modal = shallowRef(false); // Состояние модального окна
const page = shallowRef(0); // Страница таблицы
const search = shallowRef(""); // Поисковый запрос

const debounced = refDebounced(search, 1000); // Дебаунс поиска

const { execute, isLoading, state } = useAsyncState<Person[]>(
  async () =>
    await ky
      .get("/api/candidates", {
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
  const resp = await ky.post("/api/persons/", { json: form });
  if (resp.status === 201) {
    const { person_id } = (await resp.json()) as { person_id: string | null };
    if (person_id) router.push("profile/" + person_id);
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
            icon="i-mi-user-add"
            size="xl"
            title="Добавить анкету"
            variant="ghost"
            :loading="isLoading"
            @click="modal = true"
          />
          <template #body>
            <FormDiv :fields="PersonForm" @submit="submit" />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <!-- Строка поиска -->
    <UPageBody>
      <UInput
        id="search"
        icon="i-mi-search"
        v-model.trim="search"
        :loading="isLoading"
        type="search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />

      <!-- Таблица с данными кандидатов -->
      <Transition name="fade">
        <TableDiv
          v-if="state.length"
          :cols="personCols"
          :data="state"
          @select="(row: Person) => router.push('/profile/' + row.id)"
        >
        </TableDiv>
      </Transition>

      <UEmpty
        v-if="!isLoading && !state.length"
        icon="i-mi-warning"
        size="sm"
        title="Данные отсутствуют"
        variant="naked"
      />

      <!-- Время последнего обновления -->
      <UButton
        v-show="state.length"
        icon="i-mi-refresh"
        label="Обновить"
        :loading="isLoading"
        size="sm"
        title="Обновить"
        variant="ghost"
        @click="execute()"
      />

      <!-- Пагинация -->
      <div
        v-show="state.length"
        class="flex justify-center border-t border-default pt-8 pb-2"
      >
        <UButton
          class="me-2 rounded-full"
          :disabled="!page || isLoading"
          icon="i-mi-arrow-left"
          title="Вперед"
          @click="page--"
        />
        <USelect
          v-model="limit"
          :items="[10, 50, 100]"
          title="Количество записей"
          :ui="{
            base: 'w-auto',
          }"
        />
        <UButton
          class="ms-2 rounded-full"
          :disabled="!hasNext || isLoading"
          icon="i-mi-arrow-right"
          title="Назад"
          @click="page++"
        />
      </div>
    </UPageBody>
  </UContainer>
</template>

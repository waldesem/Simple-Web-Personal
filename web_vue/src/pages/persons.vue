<script setup lang="ts">
import { KyInstance } from "ky";
import { inject, ref, watch } from "vue";
import { refDebounced, useAsyncState, useFileDialog } from "@vueuse/core";
import { useRouter } from "vue-router";
import { TableColumn, TableRow } from "@nuxt/ui";
import { useToasts } from "@/composables";
import { localStr, timeAgoStr } from "@/utils";
import { person as PersonForm } from "@/schema/forms";
import type { Person } from "@/types";

definePage({ meta: { layout: "UserLayout" } });

const router = useRouter();

const toast = useToast();

const { create } = useToasts(toast);

const api = inject("api") as KyInstance;

const hasNext = ref(false); // Состояние наличия следующей страницы
const limit = ref(10); // Количество записей на странице
const modal = ref(false); // Состояние модального окна
const page = ref(0); // Страница таблицы
const search = ref(""); // Поисковый запрос

const debounced = refDebounced(search, 1000); // Дебаунс поиска

const { open, onChange } = useFileDialog({
  accept: "*.json",
  multiple: false,
});

const columns: TableColumn<Person>[] = [
  { accessorKey: "id", header: "#" },
  { accessorKey: "surname", header: "Фамилия" },
  { accessorKey: "firstname", header: "Имя" },
  { accessorKey: "patronymic", header: "Отчество" },
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => localStr(row.original.birthday),
  },
  {
    accessorKey: "created",
    header: "Обновлено",
    cell: ({ row }) => timeAgoStr(row.original.created),
  },
];

const { execute, isLoading, state } = useAsyncState<Person[]>(
  async () =>
    await api
      .get("/candidates", {
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
    onError() {
      create();
    },
  },
);

watch([debounced, limit], async () => {
  console.log("debounced, limit");
  if (page.value === 0) await execute();
  else page.value = 0;
});

watch(page, async () => {
  console.log("page");
  await execute();
});

function addToast(person_id: string | null) {
  if (person_id) {
    create("success", "Анкета успешно добавлена!");
    router.push("profile/" + person_id);
  } else create("secondary", "Возможно, анкета уже существует!");
}

// Обработчик результата загрузки данных
async function submit(form: Person) {
  modal.value = false;
  const resp = await api.post("/persons/", { json: form });
  if (resp.ok) {
    const { person_id } = (await resp.json()) as { person_id: string | null };
    addToast(person_id);
  } else create();
}

onChange(async (files) => {
  if (files) {
    const str = (await files?.[0].text()) as string;
    const resp = await api.post("/persons/json", {
      json: JSON.parse(str),
    });
    if (resp.ok) {
      const { person_id } = (await resp.json()) as {
        person_id: string | null;
      };
      addToast(person_id);
    } else create();
  }
});
</script>

<template>
  <UContainer>
    <UPageHeader title="КАНДИДАТЫ">
      <template #links>
        <UButton
          icon="i-mi-cloud-upload"
          size="xl"
          title="Загрузить файл"
          variant="ghost"
          :loading="isLoading"
          @click="open()"
        />
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
      <UTable
        class="flex-1"
        empty="Нет данных"
        :data="state"
        :columns="columns"
        :loading="isLoading"
        loading-animation="swing"
        loading-color="error"
        @select="
          (_, r: TableRow<Person>) => router.push(`/profile/${r.original.id}`)
        "
      />

      <!-- Время последнего обновления -->
      <UButton
        v-show="state.length"
        :loading="isLoading"
        icon="i-mi-refresh"
        label="Обновить"
        size="sm"
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

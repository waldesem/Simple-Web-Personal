<script setup lang="ts">
import { ref, watch, defineAsyncComponent, shallowRef, onMounted } from "vue";
import { refDebounced } from "@vueuse/core";
import { useRouter } from "vue-router";
import { ofetch } from "ofetch";
import { localStr, timeAgoStr } from "@/utils";
import type { Candidates, Person, TableColumns } from "@/types";

const FormResume = defineAsyncComponent(
  () => import("@/components/forms/ResumeForm.vue"),
);

const router = useRouter();

const data = shallowRef({ has_next: false, candidates: [] } as Candidates);
const modal = ref(false); // Состояние модального окна
const page = ref(0); // Страница таблицы
const search = ref(""); // Поисковый запрос
const loading = ref(false);
const updated = ref(new Date().toLocaleTimeString());
const debounced = refDebounced(search, 1000);

watch(debounced, async () => {
  page.value = 0;
  await getItem();
});

watch(page, async () => {
  await getItem();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

onMounted(async () => {
  await getItem();
});

async function getItem() {
  loading.value = true;
  data.value = await ofetch<Candidates>("/routes/candidates", {
    query: {
      search: debounced.value,
      page: page.value,
    },
  });
  loading.value = false;
  updated.value = new Date().toLocaleTimeString();
}

// Обработчик результата загрузки данных
async function submitPerson(form: Person) {
  modal.value = false;
  const resp = await ofetch.raw("/routes/persons", {
    method: "POST",
    body: { ...form, created: new Date().toISOString() },
  });
  if (resp.status === 201) {
    if (resp._data.person_id) {
      router.push({ name: "profile", params: { id: resp._data.person_id } });
    } else {
      alert("Анкета уже существует!");
    }
  } else {
    alert("Невозможно выполнить действие.");
  }
}

const cols: TableColumns<Person>[] = [
  {
    name: "id",
    header: "#",
  },
  {
    name: "surname",
    header: "Фамилия",
  },
  {
    name: "firstname",
    header: "Имя",
  },
  {
    name: "patronymic",
    header: "Отчество",
  },
  {
    name: "birthday",
    header: "Дата рождения",
    cell: (row) => {
      return localStr(row.birthday);
    },
  },
  {
    name: "created",
    header: "Обновлено",
    cell: (row) => {
      return timeAgoStr(row.created);
    },
  },
];
</script>

<template>
  <UContainer>
    <UPageHeader title="КАНДИДАТЫ">
      <template #links>
        <!-- Модальное окно для добавления анкеты -->
        <UModal
          v-model:open="modal"
          title="Анкета"
          description="Введите анкетные данные"
        >
          <UButton
            icon="i-lucide-user-plus"
            title="Добавить анкету"
            variant="ghost"
            size="xl"
            @click="modal = true"
          />
          <template #body>
            <FormResume @update="submitPerson" />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <!-- Строка поиска -->
    <div class="my-6">
      <UInput
        id="search"
        v-model.trim="search"
        icon="i-lucide-search"
        type="search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />
    </div>

    <!-- Таблица с данными кандидатов -->
    <TableDiv
      :cols="cols"
      :data="data.candidates"
      @select="
        (id: any) => router.push({ name: 'profile', params: { id: id } })
      "
    />
    <div
      v-if="loading"
      class="absolute inset-0 bg-white/60 flex flex-col items-center justify-center gap-4"
    >
      <div
        class="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"
      ></div>
      <div class="font-medium">Обновление данных...</div>
    </div>
    <UEmpty
      v-if="!data.candidates.length"
      title="Данные отсутствуют"
      size="sm"
      variant="naked"
    />

    <!-- Время последнего обновления -->
    <UButton
      :loading="loading"
      class="mt-2"
      variant="ghost"
      size="sm"
      icon="i-lucide-refresh-cw"
      :label="`Последнее обновление в: ${updated}`"
      title="Обновить"
      @click="getItem"
    />

    <!-- Пагинация -->
    <div
      v-show="data.candidates && (page || data.has_next)"
      class="flex justify-center border-t border-default space-x-2 mt-4 py-4"
    >
      <UButton
        icon="i-lucide-arrow-left"
        title="Вперед"
        :disabled="!page || loading"
        class="me-2 rounded-full"
        @click="page--"
      />
      <UButton
        icon="i-lucide-arrow-right"
        title="Назад"
        :disabled="!data.has_next || loading"
        class="ms-2 rounded-full"
        @click="page++"
      />
    </div>
  </UContainer>
</template>

<script setup lang="ts">
import { watchEffect, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { refDebounced, useTimeAgoIntl } from "@vueuse/core";
import { ofetch } from "ofetch";
import { useToast } from "@nuxt/ui/composables";
import { localStr } from "@/utils";
import type { Candidates, Person } from "@/types";

const toast = useToast();

const router = useRouter();

export interface TableColumns<T> {
  name: keyof T;
  header: string;
  cell?: (row: T) => string;
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
      return useTimeAgoIntl(row.created).value;
    },
  },
];

const data = ref({ has_next: false, candidates: [] } as Candidates);
const modal = ref(false); // Состояние модального окна
const page = ref(0); // Страница таблицы
const search = ref(""); // Поисковый запрос
const updated = ref(new Date().toLocaleTimeString());

const debounced = refDebounced(search, 1000);

watch(debounced, () => {
  page.value = 0;
});

watchEffect(async () => {
  data.value = await ofetch<Candidates>("/routes/candidates", {
    query: {
      search: debounced.value,
      page: page.value,
    },
  });
});

watch(data, () => (updated.value = new Date().toLocaleTimeString()));

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
      toast.add({
        title: "Внимание",
        description: "Анкета уже существует!",
        color: "info",
      });
    }
  } else {
    toast.add({
      title: "Ошибка",
      description: "Невозможно выполнить действие.",
      color: "error",
    });
  }
}
</script>

<template>
  <LayoutView>
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
              <ResumeForm @update="submitPerson" />
            </template>
          </UModal>
        </template>
      </UPageHeader>

      <!-- Строка поиска -->
      <div class="my-6">
        <UInput
          id="search"
          v-model.trim="search"
          type="search"
          placeholder="поиск по фаимилии, имени, отчеству"
        />
      </div>

      <!-- Таблица с данными кандидатов -->
      <div class="relative overflow-auto">
        <table class="table-fixed min-w-full overflow-clip">
          <thead class="relative">
            <tr>
              <th
                v-for="(row, index) in cols"
                :key="index"
                class="p-4 text-sm text-highlighted text-left"
              >
                {{ row.header }}
              </th>
            </tr>
          </thead>
          <tbody class="isolate divide-y divide-default">
            <tr
              v-for="(candidate, index) in data.candidates"
              :key="index"
              class="hover:bg-gray-100 cursor-pointer"
              @click="
                router.push({ name: 'profile', params: { id: candidate.id } })
              "
            >
              <td
                v-for="(row, idx) in cols"
                :key="idx"
                class="p-4 text-sm text-muted whitespace-nowrap"
              >
                {{ row.cell ? row.cell(candidate) : candidate[row.name] }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <UEmpty
        v-if="!data.candidates"
        title="Данные отсутствуют"
        size="sm"
        variant="naked"
      />

      <!-- Время последнего обновления -->
      <div class="text-sm text-muted mt-4">
        Последнее обновление: {{ updated }}
      </div>

      <!-- Пагинация -->
      <div class="flex justify-center border-t border-default space-x-2 py-4">
        <UButton
          icon="i-lucide-arrow-left"
          title="Вперед"
          :disabled="!page"
          class="me-2 rounded-full"
          @click="page--"
        />
        <UButton
          icon="i-lucide-arrow-right"
          title="Назад"
          :disabled="!data.has_next"
          class="ms-2 rounded-full"
          @click="page++"
        />
      </div>
    </UContainer>
  </LayoutView>
</template>

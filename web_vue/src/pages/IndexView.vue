<script setup lang="ts">
import useToast from "@nuxt/ui"
import type { Candidates, Person, TableColumns } from "@/types";
import { refDebounced, useTimeAgoIntl } from "@vueuse/core";
import { onBeforeMount, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { ofetch } from "ofetch";

const toast = useToast();
const router = useRouter();

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
      return new Date(row.birthday).toLocaleDateString();
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

// Объявляем переменные для работы с данными
const data = ref({ has_next: false, candidates: [] } as Candidates);
const modal = ref(false); // Состояние модального окна
const page = ref(0); // Страница таблицы
const search = ref(""); // Поисковый запрос
const status = ref("string");

onBeforeMount(() => getCandidates());

// Определяем функцию для получения списка кандидатов из API
async function getCandidates() {
  data.value = await ofetch<Candidates>("/routes/candidates/" + page.value, {
    query: {
      search: search.value,
    },
  })
}

// Наблюдаем: поиск
watch(refDebounced(search, 1000), async () => {
  if (page.value === 0) {
    await getCandidates();
  } else {
    page.value = 0;
  }
});

watch(page, async () => await getCandidates())

// Обработчик результата загрузки данных
function submitPerson(person_id: string, exists: boolean) {
  modal.value = false;
  status.value = "success";
  if (exists) {
    toast.add({
      title: "Информация",
      description: "Анкета уже была загружена ранее.",
      color: "info",
    });
  }
  return router.push("/profile/" + person_id);
}
</script>

<template>
  <LayoutsView>
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
              title="Добавить анкету"
              variant="ghost"
              icon="i-lucide-user-plus"
              :loading="status === 'pending'"
              @click="modal = true"
            />
            <template #body>
              <FormsResumeForm @update="submitPerson" />
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
              @click="router.push('/profile/' + candidate.id)"
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
        v-if="!data.candidates.length"
        title="Данные отсутствуют"
        size="sm"
        variant="naked"
      />

      <!-- Кнопка обновления -->
      <div class="py-3">
        <UButton
          variant="outline"
          label="Обновить данные"
          :loading="status === 'pending'"
          size="sm"
          @click="getCandidates()"
        />
      </div>

      <!-- Пагинация -->
      <div class="flex justify-center border-t border-default space-x-2 py-4">
        <UButton
          title="Предыдущая страница"
          icon="i-lucide-arrow-left"
          :disabled="!page || status == 'pending'"
          class="me-2 rounded-full"
          @click="page--"
        />
        <UButton
          title="Следующая страница"
          icon="i-lucide-arrow-right"
          :disabled="!data.has_next || status == 'pending'"
          class="ms-2 rounded-full"
          @click="page++"
        />
      </div>
    </UContainer>
  </LayoutsView>
</template>

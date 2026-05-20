<script setup lang="ts">
import { ref, watch, shallowRef, onMounted } from "vue";
import { refDebounced } from "@vueuse/core";
import { useRouter } from "vue-router";
import { ofetch } from "ofetch";
import { localStr, timeAgoStr } from "@/utils";
import { itemsForms } from "@/schema/forms";
import type { Person, TableColumns } from "@/types";

const router = useRouter();

const data = shallowRef([] as Person[]);
const page = ref(0); // Страница таблицы
const limit = ref(10); // Количество записей на странице
const search = ref(""); // Поисковый запрос
const updated = ref(""); // Время обновления
const modal = ref(false); // Состояние модального окна
const hasNext = ref(false); // Состояние наличия следующей страницы
const loading = ref(false); // Состояние загрузки
const debounced = refDebounced(search, 1000); // Дебаунс поиска

onMounted(() => getItem());

watch(debounced, async () => {
  page.value = 0;
  await getItem();
});

watch(page, async () => {
  await getItem();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

async function getItem() {
  loading.value = true;
  const response = await ofetch<Person[]>("/routes/candidates", {
    query: {
      limit: limit.value,
      search: debounced.value,
      page: page.value,
    },
  });
  hasNext.value = response.length > limit.value;
  data.value = response.slice(0, limit.value);
  updated.value = new Date().toLocaleTimeString();
  loading.value = false;
}

// Обработчик результата загрузки данных
async function submitPerson(form: Person) {
  modal.value = false;
  loading.value = true;
  const resp = await ofetch.raw("/routes/persons", {
    method: "POST",
    body: form,
  });
  loading.value = false;
  if (resp.status === 201) {
    if (resp._data.person_id) {
      router.push({ name: "profile", params: { id: resp._data.person_id } });
    } else {
      alert("Анкета уже существует!");
    }
  } else {
    alert("Невозможно выполнить действие!");
  }
}

const tableColumns: TableColumns<Person>[] = [
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
    cell: (row) => localStr(row.birthday),
  },
  {
    name: "created",
    header: "Обновлено",
    cell: (row) => timeAgoStr(row.created),
  },
];
</script>

<template>
  <UContainer class="pt-16">
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
        v-model.trim="search"
        :loading="loading"
        icon="i-lucide-search"
        type="search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />

      <!-- Таблица с данными кандидатов -->
      <TableDiv
        :class="{ 'animate-pulse': loading }"
        :cols="tableColumns"
        :data="data"
        @select="
          (id: any) => router.push({ name: 'profile', params: { id: id } })
        "
      />

      <UEmpty
        v-if="!data"
        title="Данные отсутствуют"
        size="sm"
        variant="naked"
      />

      <!-- Время последнего обновления -->
      <UButton
        :loading="loading"
        variant="ghost"
        size="sm"
        icon="i-lucide-refresh-cw"
        :label="`Последнее обновление в: ${updated}`"
        title="Обновить"
        @click="getItem"
      />

      <!-- Пагинация -->
      <div
        v-show="data"
        class="flex justify-center border-t border-default py-4"
      >
        <UButton
          icon="i-lucide-arrow-left"
          title="Вперед"
          :disabled="!page || loading"
          class="me-2 rounded-full"
          @click="page--"
        />
        <USelect
          v-model="limit"
          :items="[10, 50, 100]"
          title="Количество записей"
          @change="getItem"
        />
        <UButton
          icon="i-lucide-arrow-right"
          title="Назад"
          :disabled="!hasNext || loading"
          class="ms-2 rounded-full"
          @click="page++"
        />
      </div>
    </UPageBody>
  </UContainer>
</template>

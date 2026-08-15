<script setup lang="ts">
import { KyInstance } from 'ky';
import { inject, ref, watch } from 'vue';
import { refDebounced, useAsyncState, useFileDialog } from '@vueuse/core';
import { useRouter } from 'vue-router';
import { TableRow } from '@nuxt/ui';
import { useToasts } from '@/composables';
import { session } from '@/state';
import { columns } from '@/schema/items';
import { person as personForm } from '@/schema/forms';
import { Roles, type Person, type PersonId } from '@/types';

definePage({ meta: { layout: 'user' } });

const router = useRouter();

const toast = useToast();

const { create } = useToasts(toast);

const api = inject('api') as KyInstance;

const hasNext = ref(false); // Состояние наличия следующей страницы
const limit = ref(10); // Количество записей на странице
const modal = ref(false); // Состояние модального окна
const page = ref(0); // Страница таблицы
const search = ref(''); // Поисковый запрос
const check = ref(false); // Полнотекстовый поиск

const debounced = refDebounced(search, 1000); // Дебаунс поиска

const { open, onChange } = useFileDialog({
  accept: '*.json',
  multiple: false,
});

const { execute, isLoading, state } = useAsyncState<Person[]>(
  async () =>
    await api
      .get(`candidates/${check.value ? 'fts' : 'ts'}`, {
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
  }
);

watch([debounced, limit], async () => {
  if (page.value === 0) await execute();
  else page.value = 0;
});

watch(page, async () => await execute());

function addToast(person_id: string | null) {
  if (person_id) {
    create('success', 'Анкета успешно добавлена!');
    router.push('profile/' + person_id);
  } else create('warning', 'Возможно, анкета уже существует!');
}

// Обработчик результата загрузки данных
async function submit(form: Person) {
  modal.value = false;
  const resp = await api.post('persons/', { json: form });
  if (resp.ok) {
    const { person_id } = await resp.json<PersonId>();
    addToast(person_id);
  } else create();
}

onChange(async (files) => {
  if (files) {
    const str = (await files?.[0].text()) as string;
    const resp = await api.post('persons/json', {
      json: JSON.parse(str),
    });
    if (resp.ok) {
      const { person_id } = await resp.json<PersonId>();
      addToast(person_id);
    } else create();
  }
});
</script>

<template>
  <UContainer>
    <UPage>
      <UPageHeader title="КАНДИДАТЫ">
        <template #links v-if="session.role === Roles.user">
          <UButton
            icon="i-lucide-upload"
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
              icon="i-lucide-user-plus"
              size="xl"
              title="Добавить анкету"
              variant="ghost"
              :loading="isLoading"
            />
            <template #body>
              <FormDiv :fields="personForm" @submit="submit" />
            </template>
          </UModal>
        </template>
      </UPageHeader>

      <UPageBody>
        <!-- Строка поиска -->
        <div class="flex items-center space-x-2">
          <UInput
            id="search"
            icon="i-lucide-search"
            v-model.trim="search"
            :loading="isLoading"
            type="search"
            placeholder="поиск по фаимилии, имени, отчеству"
          />
          <UCheckbox v-model="check" title="Полнотекстовый поиск" />
        </div>
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
            (_, { original }: TableRow<Person>) =>
              router.push(`/profile/${original.id}`)
          "
        />

        <!-- Кнопка обновления -->
        <UButton
          v-show="state.length"
          :loading="isLoading"
          icon="i-lucide-refresh-cw"
          label="Обновить"
          size="sm"
          variant="ghost"
          @click="execute()"
        />

        <!-- Пагинация -->
        <div
          v-show="state.length"
          class="flex justify-center border-t border-default pt-8"
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
            :items="[10, 30, 50]"
            title="Количество записей"
            :ui="{
              base: 'w-auto',
            }"
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
    </UPage>
  </UContainer>
</template>

<style scoped>
.tbody {
  opacity: v-bind("isLoading ? '0.5': '1'");
}
</style>

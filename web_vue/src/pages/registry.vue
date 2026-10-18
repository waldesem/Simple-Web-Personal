<script setup lang="ts">
import { KyInstance } from 'ky';
import { h, inject, ref, resolveComponent, watch } from 'vue';
import { refDebounced, useAsyncState, useFileDialog } from '@vueuse/core';
import { useRouter } from 'vue-router';
import { TableColumn, TableRow } from '@nuxt/ui';
import { useToasts } from '@/composables';
import { session } from '@/state';
import { registr as regItem } from '@/schema/items';
import { regForm } from '@/schema/forms';
import { localStr, timeAgoStr } from '@/utilities';
import { Roles, type Registry, type PersonId } from '@/types';

definePage({ meta: { layout: 'user' } });

const toast = useToast();

const router = useRouter();

const UButton = resolveComponent('UButton');

const { create } = useToasts(toast);

const api = inject('api') as KyInstance;

const hasNext = ref(false); // Состояние наличия следующей страницы
const limit = ref(10); // Количество записей на странице
const modal = ref(false); // Состояние модального окна
const method = ref<'POST' | 'PATCH'>('POST');
const page = ref(0); // Страница таблицы
const search = ref('');
const expanded = ref({ 1: true });
const item = ref({} as Registry);

const debounced = refDebounced(search, 1000); // Дебаунс поиска

const columns: TableColumn<Registry>[] = [
  {
    id: 'expand',
    cell: ({ row }) =>
      h(UButton, {
        color: 'neutral',
        variant: 'ghost',
        icon: 'i-lucide-chevron-down',
        square: true,
        'aria-label': 'Expand',
        ui: {
          leadingIcon: [
            'transition-transform',
            row.getIsExpanded() ? 'duration-200 rotate-180' : '',
          ],
        },
        onClick: () => row.toggleExpanded(),
      }),
  },
  {
    accessorKey: 'id',
    header: '#',
    meta: { class: { th: 'w-2/23' } },
  },
  {
    accessorKey: 'fullname',
    header: 'Фамилия Имя Отчество',
    meta: { class: { th: 'w-5/23' } },
  },
  {
    accessorKey: 'birthday',
    header: 'Дата рождения',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) => localStr(row.original.birthday),
  },
  {
    accessorKey: 'incomes',
    header: 'Поступил',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) => timeAgoStr(row.original.incomes),
  },
  {
    accessorKey: 'user',
    header: 'Сотрудник',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) => row.original.officer.split(' ')[0],
  },
  {
    accessorKey: 'conclusion',
    header: 'Результат',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) => {
      const color =
        row.original.results === 'СОГЛАСОВАНО'
          ? 'bg-green-500'
          : row.original.results === 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
            ? 'bg-gray-500'
            : row.original.results === 'СНЯТ С ПРОВЕРКИ'
              ? 'bg-yellow-500'
              : row.original.results === 'НА ПРОВЕРКЕ'
                ? 'bg-blue-500'
                : 'bg-red-500';
      return h(
        'span',
        {
          class: [
            'flex inline-flex Items-center py-1 px-2 rounded-md text-sm text-white',
            color,
          ],
        },
        row.original.results
      );
    },
  },
  {
    accessorKey: 'outcomes',
    header: 'Согласован',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) =>
      row.original.outcomes ? timeAgoStr(row.original.outcomes) : '',
  },
];

const { open, onChange } = useFileDialog({
  accept: '*.json',
  multiple: false,
});

const { execute, isLoading, state } = useAsyncState<Registry[]>(
  async () =>
    await api
      .get('registry/', {
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

watch([limit, page, debounced], async () => await execute());

function addToast(person_id: string | null) {
  if (person_id) {
    create('success', 'Анкета успешно добавлена!');
  } else create('warning', 'Возможно, анкета уже существует!');
}

// Обработчик результата загрузки данных
async function submit(form: Registry) {
  console.log(form);
  modal.value = false;
  const url =
    method.value === 'POST' ? 'registry/' : `registry/${item.value.id}`;
  const resp = await api(url, { method: method.value, json: form });
  if (resp.ok) {
    const { person_id } = await resp.json<PersonId>();
    addToast(person_id);
  } else create();
  item.value = {} as Registry;
  method.value = 'POST';
  await execute();
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

async function deleteRow(id: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const resp = await api.delete(`registry/${id}`);
  if (resp.ok) {
    await execute();
  } else create();
}

function openPerson(_: Event, row: TableRow<Registry>) {
  router.push(`/profile/${row.original.id}`);
}
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
              <FormDiv :fields="regForm" :item="item" @submit="submit" />
            </template>
          </UModal>
        </template>
      </UPageHeader>

      <UPageBody>
        <!-- Строка поиска -->
        <UInput
          id="search"
          icon="i-lucide-search"
          v-model.trim="search"
          :loading="isLoading"
          type="search"
          placeholder="поиск по реестру"
        />

        <!-- Таблица с данными кандидатов -->
        <UTable
          v-model:expanded="expanded"
          class="flex-1"
          empty="Нет данных"
          :data="state"
          :columns="columns"
          :loading="isLoading"
          loading-animation="swing"
          loading-color="error"
          @select="openPerson"
        >
          <template #expanded="{ row }">
            <ItemDiv
              :item="row.original"
              :fields="regItem"
              @delete="deleteRow(row.original.id)"
              @update="
                item = row.original;
                modal = true;
                method = 'PATCH';
              "
            />
          </template>
        </UTable>

        <div class="flex justify-between">
          <UButton
            v-show="state.length"
            :loading="isLoading"
            icon="i-lucide-refresh-cw"
            label="Обновить"
            size="sm"
            variant="ghost"
            @click="execute()"
          />
        </div>

        <!-- Пагинация -->
        <SwitchPage
          :page="page"
          :has-next="hasNext"
          :is-loading="isLoading"
          :limit="limit"
          :state-length="state.length"
          @limit="limit = limit"
          @next="page++"
          @previous="page--"
        />
      </UPageBody>
    </UPage>
  </UContainer>
</template>

<style scoped>
.tbody {
  opacity: v-bind("isLoading ? '0.5': '1'");
}
</style>

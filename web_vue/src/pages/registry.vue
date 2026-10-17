<script setup lang="ts">
import { KyInstance } from 'ky';
import { h, inject, ref, resolveComponent, shallowRef, watch } from 'vue';
import { refDebounced, useAsyncState, useFileDialog } from '@vueuse/core';
import { TableColumn, TableRow } from '@nuxt/ui';
import { useToasts } from '@/composables';
import { session } from '@/state';
import { localStr, registr as regItem, timeAgoStr } from '@/schema/items';
import { registr as regForm } from '@/schema/forms';
import { Roles, type Registry, type PersonId } from '@/types';

definePage({ meta: { layout: 'user' } });

const toast = useToast();

const { create } = useToasts(toast);

const api = inject('api') as KyInstance;

const hasNext = ref(false); // Состояние наличия следующей страницы
const limit = ref(10); // Количество записей на странице
const modal = ref(false); // Состояние модального окна
const method = shallowRef<'POST' | 'PATCH'>('POST');
const page = ref(0); // Страница таблицы
const search = ref(''); // Поисковый запрос
const expanded = ref({ 1: true });
const item = shallowRef({} as Registry);
const UButton = resolveComponent('UButton');

const columnsReg: TableColumn<Registry>[] = [
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
    accessorKey: 'officer',
    header: 'Сотрудник',
    meta: { class: { th: 'w-3/23' } },
  },
  {
    accessorKey: 'results',
    header: 'Результат',
    meta: { class: { th: 'w-3/23' } },
  },
  {
    accessorKey: 'outcomes',
    header: 'Согласован',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) => timeAgoStr(row.original.outcomes ?? ''),
  },
];

const debounced = refDebounced(search, 1000); // Дебаунс поиска

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
    window.open(`/profile/${person_id}`, '_blank');
  } else create('warning', 'Возможно, анкета уже существует!');
}

// Обработчик результата загрузки данных
async function submit(form: Registry) {
  modal.value = false;
  const url = 'persons/registry';
  const resp = await api.post(
    method.value === 'POST' ? url : url + '/' + item.value.id,
    { method: method.value, json: form }
  );
  item.value = {} as Registry;
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

async function deleteItem(id: string) {
  const resp = await api.delete(`registry/${id}`);
  if (resp.ok) {
    await execute();
  } else create();
}

function openPerson(_: Event, row: TableRow<Registry>) {
  window.open(`/profile/${row.original.person_id}`, '_blank');
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
          placeholder="полнотекстовый поиск"
        />

        <!-- Таблица с данными кандидатов -->
        <UTable
          v-model:expanded="expanded"
          class="flex-1"
          empty="Нет данных"
          :data="state"
          :columns="columnsReg"
          :loading="isLoading"
          loading-animation="swing"
          loading-color="error"
          @select="openPerson"
        >
          <template #expanded="{ row }">
            <ItemDiv
              :item="row.original"
              :fields="regItem"
              @delete="deleteItem(row.original.id)"
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

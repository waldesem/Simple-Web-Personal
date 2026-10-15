<script setup lang="ts">
import { KyInstance } from 'ky';
import { inject, ref, watch } from 'vue';
import { refDebounced, useAsyncState } from '@vueuse/core';
import { TableRow } from '@nuxt/ui';
import { columnsDB } from '@/schema/items';
import { type Person } from '@/types';
import SwitchPage from '@/components/content/SwitchPage.vue';

definePage({ meta: { layout: 'user' } });

const api = inject('api') as KyInstance;

const hasNext = ref(false); // Состояние наличия следующей страницы
const limit = ref(10); // Количество записей на странице
const page = ref(0); // Страница таблицы
const search = ref(''); // Поисковый запрос

const debounced = refDebounced(search, 1000); // Дебаунс поиска

const { execute, isLoading, state } = useAsyncState<Person[]>(
  async () =>
    await api
      .get('index/', {
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

function openPerson(_: Event, row: TableRow<Person>) {
  window.open(`/profile/${row.original.id}`, '_blank');
}
</script>

<template>
  <UContainer>
    <UPage>
      <UPageHeader title="БАЗА ДАННЫХ" />
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
          class="flex-1"
          empty="Нет данных"
          :data="state"
          :columns="columnsDB"
          :loading="isLoading"
          loading-animation="swing"
          loading-color="error"
          @select="openPerson"
        />

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

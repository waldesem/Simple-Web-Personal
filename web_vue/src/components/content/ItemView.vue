<script setup lang="ts">
import { KyInstance } from "ky";
import { inject, type PropType, shallowRef } from "vue";
import { useAsyncState } from "@vueuse/core";
import { useToasts } from "@/composables";
import { itemsFields } from "@/schema/items";
import { itemsForms } from "@/schema/forms";
import { Roles, type Items } from "@/types";
import { session } from "@/state";

// Определяем данные которые передаются из родительского компонента
const { candId, title, view } = defineProps({
  candId: { type: String, required: true },
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
});

const toast = useToast();

const { create } = useToasts(toast);

const api = inject("api") as KyInstance;

const { execute, state, isLoading } = useAsyncState<Items[keyof Items][]>(
  async () => await api.get(`items/${view}/${candId}`).json(),
  [],
);

const item = shallowRef({} as Items[keyof Items]);
const method = shallowRef<"POST" | "PATCH">("POST");
const modal = shallowRef(false); // Флаг для открытия модального окна
const visible = shallowRef(false);

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  isLoading.value = true;
  const url = `items/${view}/${candId}`;
  const { ok } = await api(
    method.value === "POST" ? url : url + "/" + item.value.id,
    {
      method: method.value,
      json: { comparator: view, ...form },
    },
  );
  await execute();
  item.value = {} as typeof item.value;
  if (!ok) create();
  else if (method.value === "POST") {
    create("success", "Запись успешно добавлена!");
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else {
    create("info", "Запись обновлена!");
  }
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string, index: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { ok } = await api.delete(`items/${view}/${itemId}`);
  if (ok) {
    create("success", "Запись удалена!");
    state.value.splice(index, 1);
  } else create();
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty
    v-if="!state.length"
    size="sm"
    title="Нет данных"
    variant="naked"
    class="no-print"
  >
    <template #body>
      <UButton
        v-if="session.role === Roles.user"
        :leading="isLoading"
        label="Добавить запись"
        size="sm"
        variant="outline"
        @click="
          modal = true;
          method = 'POST';
        "
      />
    </template>
  </UEmpty>

  <div @mouseover="visible = true" @mouseleave="visible = false">
    <div
      v-for="(content, index) in state"
      :key="index"
      :class="{ 'animate-pulse': isLoading }"
      class="my-2"
    >
      <!-- Выводим элемент данных -->
      <ItemDiv
        :item="content"
        :fields="itemsFields[view]"
        @delete="deleteItem(content.id, index)"
        @update="
          item = content;
          modal = true;
          method = 'PATCH';
        "
      />
      <USeparator v-if="index + 1 < state.length" />
    </div>

    <!-- Модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      :description="
        method === 'POST' ? 'Добавить данные' : 'Редактировать данные'
      "
      :title="title"
    >
      <Transition name="slide-down">
        <UButton
          v-if="state.length && visible && session.role === Roles.user"
          block
          class="my-2"
          color="neutral"
          icon="i-lucide-plus"
          title="Добавить запись"
          size="sm"
          variant="outline"
          @click="method = 'POST'"
        />
      </Transition>
      <template #body>
        <FormDiv :item="item" :fields="itemsForms[view]" @submit="submitItem" />
      </template>
    </UModal>
  </div>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition:
    transform 0.3s ease,
    opacity 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: scaleY(0);
  opacity: 0;
}
</style>
